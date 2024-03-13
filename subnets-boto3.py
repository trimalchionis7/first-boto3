import logging
import boto3
from botocore.exceptions import ClientError
import json

# Select AWS Region
AWS_REGION = 'us-west-2'

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

ec2_instance = boto3.resource('ec2', region_name=AWS_REGION)

# Create custom subnets
def create_custom_subnet(vpc_id, ip_cidr, is_public, subnet_number, availability_zone):
    subnet_type = "public" if is_public else "private"

    try:
        response = ec2_instance.create_subnet(
        AvailabilityZone=availability_zone, VpcId=vpc_id, CidrBlock=ip_cidr)

        subnet_id = response.id

        print(f'{subnet_type} subnet created in {availability_zone} with ID: {subnet_id}')

        # Add tags to the subnet
        ec2_instance.create_tags(Resources=[subnet_id], 
            Tags=[{'Key': 'Name', 'Value': f'{subnet_type}-{subnet_number}'},
            {'Key': 'Type', 'Value': {subnet_type}},
            ]
        )

    except ClientError:
        logger.exception(f'Could not create a custom subnet.')
        raise

    return subnet_id

VPC_ID = "vpc-0ea2a22424ca03472"

# Create public subnets
public_subnet_1_id = create_custom_subnet(VPC_ID, '10.0.1.0/24', is_public=True, subnet_number=1, availability_zone="us-west-2a")
public_subnet_2_id = create_custom_subnet(VPC_ID, '10.0.3.0/24', is_public=True, subnet_number=2, availability_zone="us-west-2b")

# Create private subnets
private_subnet_1_id = create_custom_subnet(VPC_ID, '10.0.2.0/24', is_public=False, subnet_number=1, availability_zone="us-west-2a")
private_subnet_2_id = create_custom_subnet(VPC_ID, '10.0.4.0/24', is_public=False, subnet_number=2, availability_zone="us-west-2b")

AZ = AWS_REGION
logger.info(f'Subnet {public_subnet_1_id} is created.')
logger.info(f'Subnet {public_subnet_2_id} is created.')
logger.info(f'Subnet {private_subnet_1_id} is created.')
logger.info(f'Subnet {private_subnet_2_id} is created.')