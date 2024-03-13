import logging
import boto3
from botocore.exceptions import ClientError
import json

# Select AWS Region
AWS_REGION = "us-west-2"

# logger config
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s"
)

ec2_instance = boto3.resource("ec2", region_name=AWS_REGION)


# Create a VPC
def create_vpc(ip_cidr):
    try:
        response = ec2_instance.create_vpc(
            CidrBlock=ip_cidr,
            InstanceTenancy="default",
            TagSpecifications=[
                {
                    "ResourceType": "vpc",
                    "Tags": [{"Key": "Name", "Value": "jonnie-vpc-boto3"}],
                }
            ],
        )
    except ClientError:
        logger.exception("Could not create a custom VPC.")
        raise
    else:
        return response


if __name__ == "__main__":
    ip_cidr = "10.0.0.0/16"
    custom_vpc = create_vpc(ip_cidr)
    logger.info(f"My first VPC is created with VPC ID: {custom_vpc.id}")


# Function to create subnets
def create_subnet(vpc_id, ip_cidr, is_public, subnet_number, availability_zone):
    try:
        response = ec2_instance.create_subnet(
            CidrBlock=ip_cidr,
            VpcId=vpc_id,
            AvailabilityZone=availability_zone,
            TagSpecifications=[
                {
                    "ResourceType": "subnet",
                    "Tags": [{"Key": "Name", "Value": f"{name}"}],
                }
            ],
        )
    except ClientError:
        logger.exception("Could not create a custom subnet.")
        raise
    else:
        return response


if __name__ == "__main__":
    VPC_ID = custom_vpc.id
    ip_cidr = "10.0.1.0/24"
    # Create public subnet 1
    is_public = True
    subnet_number = 1
    availability_zone = "us-west-2a"
    name = "public-1"
    custom_subnet = create_subnet(
        VPC_ID, ip_cidr, is_public, subnet_number, availability_zone
    )
    logger.info(f"Subnet {name} is created with subnet ID: {custom_subnet.id}")

    # Create private subnet 1
    ip_cidr = "10.0.2.0/24"
    subnet_number = 2
    is_public = False
    availability_zone = "us-west-2a"
    name = "private-1"
    custom_subnet = create_subnet(
        VPC_ID, ip_cidr, is_public, subnet_number, availability_zone
    )
    logger.info(f"Subnet {name} is created with subnet ID: {custom_subnet.id}")

    # Create public subnet 2
    ip_cidr = "10.0.3.0/24"
    subnet_number = 3
    is_public = True
    availability_zone = "us-west-2b"
    name = "public-2"
    custom_subnet = create_subnet(
        VPC_ID, ip_cidr, is_public, subnet_number, availability_zone
    )
    logger.info(f"Subnet {name} is created with subnet ID: {custom_subnet.id}")

    # Create private subnet 2
    ip_cidr = "10.0.4.0/24"
    subnet_number = 4
    is_public = False
    availability_zone = "us-west-2b"
    name = "private-2"
    custom_subnet = create_subnet(
        VPC_ID, ip_cidr, is_public, subnet_number, availability_zone
    )
    logger.info(f"Subnet {name} is created with subnet ID: {custom_subnet.id}")

# Create security group with ingress rule
def create_ingress_rule(security_group_id):
    try:
        response = ec2_instance.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[{
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }, {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }])
        
    except ClientError:
        logger.exception("Could not create ingress rule.")
        raise
    else:
        return response

if __name__ == "__main__":
    security_group_id = custom_vpc.security_groups[0].id
    create_ingress_rule(security_group_id)
    logger.info(f"Ingress rule is created for security group {security_group_id}")

# Create security group with egress rule
    def create_egress_rule(security_group_id):
    try:
        response = ec2_instance.authorize_security_group_egress(
            GroupId=security_group_id,
            IpPermissions=[{
                'IpProtocol': "-1",
                'FromPort': 0,
                'ToPort': 0,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }, {
                'IpProtocol': "-1",
                'FromPort': 0,
                'ToPort': 0,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }])

    except ClientError:
        logger.exception("Could not create egress rule.")
        raise
    else:
        return response

if __name__ == "__main__":
    security_group_id = custom_vpc.security_groups[0].id
    create_egress_rule(security_group_id)
    logger.info(f"Egress rule is created for security group {security_group_id}")

# Create internet gateway
def create_igw():
    response = ec2_instance.create_internet_gateway(TagSpecifications=[
        {
            'Resource Type': 'internet-gateway',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'jonnie-igw-boto3'
                },
            ],
        }])

if __name__ == "__main__":
    create_igw()
    logger.info(f"Internet gateway is created.")

# Create public and private route tables
def create_rt(VPC_ID):
    try:
        response = ec2_instance.create_route_table(VpcId=VPC_ID, TagSpecifications=[
            {
                'Resource Type': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'jonnie-public-rt-boto3'
                    },
                ],
            },
            ])
    except ClientError:
        logger.exception("Could not create public route table.")
        raise
    else:
        return response

if __name__ == "__main__":
                                                  