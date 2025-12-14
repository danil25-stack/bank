import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy import insert
from src.database import AsyncSessionLocal
from src.transaction.models import Transaction
from datetime import date

KAFKA_BOOTSTRAP = "kafka:29092"
CONSUMER_GROUP = "transaction_group"

TOPICS = [
    "ATM",
    "BANK_TRANSFER",
    "POS",
    "SALARY",
    "COMMERCE_PAYMENTS"
]

BATCH_SIZE = 10  # оптимально для PostgreSQL


class TransactionConsumerService:
    def __init__(self):
        self.buffer_transactions = []

    async def start(self):
        print("🚀 Starting Transaction Consumer...")
        import time
        time.sleep(60)  # wait for kafka to be ready

        consumer = self._get_consumer()

        await self._start_listen(consumer)

        # try:
        while True:
            print('*'*90)
            messages = await self._get_messages(consumer)
            await self._save_message_to_buffer(messages)

            if messages:
                await self._save_to_db()

                await self._move_offset(consumer)
    # finally:
        #     await consumer.stop()

    async def stop(self):
        print("Transaction Consumer stopping...")
        self.running = False

    async def _save_message(self, topic: str, message_bytes: bytes):
        payload = self._bytes_to_dict(message_bytes)
        if not payload:
            return
        self.buffer_transactions.append(payload)

    async def _save_to_db(self):

        if not self.buffer_transactions:
            return

        for tx in self.buffer_transactions:
            self._data_conversion(tx)

        await self._add_to_db()

    @staticmethod
    def _get_consumer() -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            *TOPICS,
            bootstrap_servers=KAFKA_BOOTSTRAP,
            group_id=CONSUMER_GROUP,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            max_poll_records=BATCH_SIZE * 2,
        )

    @staticmethod
    async def _start_listen(consumer: AIOKafkaConsumer) -> None:
        await consumer.start()

    @staticmethod
    async def _get_messages(consumer: AIOKafkaConsumer) -> dict:
        return await consumer.getmany(timeout_ms=500, max_records=BATCH_SIZE)

    async def _save_message_to_buffer(self, messages: list) -> None:
        for tp, batch in messages.items():
            for msg in batch:
                await self._save_message(msg.topic, msg.value)

    def _bytes_to_dict(self, message_bytes: bytes) -> dict:
        try:
            return json.loads(message_bytes.decode("utf-8"))
        except Exception as e:
            print(f"✗ Parse error: {e}")
            return

    @staticmethod
    async def _move_offset(consumer: AIOKafkaConsumer) -> None:
        await consumer.commit()

    def _data_conversion(self, tx):
        if isinstance(tx.get("booking_date"), str):
            tx["booking_date"] = date.fromisoformat(tx["booking_date"])

        if isinstance(tx.get("value_date"), str):
            tx["value_date"] = date.fromisoformat(tx["value_date"])
        return tx

    async def _add_to_db(self):
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    await session.execute(insert(Transaction), self.buffer_transactions)
                    print(
                        f"✓ Inserted {len(self.buffer_transactions)} transactions")

                self.buffer_transactions.clear()

            except Exception as e:
                print(f"✗ DB error: {e}")
