import logging
import boto3
from botocore.exceptions import ClientError
import json

AWS_REGION = 'us-west-2'

# logger config
logger = logging.getLogger()

custom_vpc = boto3.client("ec2", region_name = AWS_REGION)

# Delete the specified VPC
def delete_vpc(vpc_id):
    try :
        response = custom_vpc.delete_vpc(VpcId = vpc_id)
    except ClientError :
        logger.exception('Could not delete the VPC.')
        raise
    else :
        return response

if __name__ == '__main__':
    VPC_ID = 'vpc-054ee38d186c6b984'
    vpc = delete_vpc(VPC_ID)
    logger.info(f'VPC {VPC_ID} successfully deleted.')
