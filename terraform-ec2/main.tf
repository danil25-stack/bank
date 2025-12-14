provider "aws" {
    region = "eu-central-1"
    profile = "terraform"
}

resource "aws_instance" "my_Ubuntu"{
    ami = "ami-004e960cde33f9146"
    instance_type = "t3.micro"
}



