import asyncio
from src.transaction_consumer import TransactionConsumerService


async def main():
    consumer_service = TransactionConsumerService()
    await consumer_service.start()


if __name__ == "__main__":
    asyncio.run(main())
