import boto3

# Variables
globalVars = {}
globalVars['REGION_NAME']               = "us-west-2"
globalVars['CIDR_BLOCK']                = "10.0.0.0/16"

globalVars['AZ1']                       = "us-west-2a"
globalVars['AZ2']                       = "us-west-2b"

globalVars['AZ1_PUBLICSUBNET_CIDR']     = "10.0.1.0/24"
globalVars['AZ2_PUBLICSUBNET_CIDR']     = "10.0.3.0/24"
globalVars['AZ1_PRIVATESUBNET_CIDR']    = "10.0.2.0/24"
globalVars['AZ2_PRIVATESUBNET_CIDR']    = "10.0.4.0/24"

ec2 = boto3.resource('ec2', region_name=globalVars['REGION_NAME'])

# Create VPC
vpc = ec2.create_vpc(CidrBlock=globalVars['CIDR_BLOCK'], TagSpecifications=[
    {
        'ResourceType': 'vpc',
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'jonnie-vpc-boto3'
            },
        ]
    },
])
vpc.wait_until_available()
print(vpc.id)

# Create 2 public and 2 private subnets in 2 availability zones
public_subnet1 = ec2.create_subnet(CidrBlock=globalVars['AZ1_PUBLICSUBNET_CIDR'], VpcId=vpc.id, AvailabilityZone=globalVars['AZ1'],
                                   TagSpecifications=[
                                          {
                                           'ResourceType': 'subnet',
                                           'Tags': [
                                               {
                                                   'Key': 'Name',
                                                   'Value': 'public-subnet-1-boto3'
                                               },
                                           ]
                                       },])
public_subnet2 = ec2.create_subnet(CidrBlock=globalVars['AZ2_PUBLICSUBNET_CIDR'], VpcId=vpc.id, AvailabilityZone=globalVars['AZ2'],
                                                                      TagSpecifications=[
                                                                            {
                                                                              'ResourceType': 'subnet',
                                                                              'Tags': [
                                                                                  {
                                                                                      'Key': 'Name',
                                                                                      'Value': 'public-subnet-2-boto3'
                                                                                  },
                                                                              ]
                                                                          },])
private_subnet1 = ec2.create_subnet(CidrBlock=globalVars['AZ1_PRIVATESUBNET_CIDR'], VpcId=vpc.id, AvailabilityZone=globalVars['AZ1'],
                                    TagSpecifications=[
                                           {
                                            'ResourceType': 'subnet',
                                            'Tags': [
                                                {
                                                    'Key': 'Name',
                                                    'Value': 'private-subnet-1-boto3'
                                                },
                                            ]
                                        },])
private_subnet2 = ec2.create_subnet(CidrBlock=globalVars['AZ2_PRIVATESUBNET_CIDR'], VpcId=vpc.id, AvailabilityZone=globalVars['AZ2'],
                                                                     TagSpecifications=[
                                                                           {
                                                                            'ResourceType': 'subnet',
                                                                            'Tags': [
                                                                                {
                                                                                    'Key': 'Name',
                                                                                    'Value': 'private-subnet-2-boto3'
                                                                                },
                                                                            ]
                                                                        },])

# Create Internet Gateway and attach to VPC
internet_gateway = ec2.create_internet_gateway(TagSpecifications=[
    {
        'ResourceType': 'internet-gateway',
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'jonnie-igw-boto3'
            },
        ]
    }]
)
internet_gateway.attach_to_vpc(VpcId=vpc.id)
print(internet_gateway.id)

# Create public route table, create route to IGW, associate with public subnets
public_route_table = ec2.create_route_table(VpcId=vpc.id, TagSpecifications=[
    {
        'ResourceType': 'route-table',
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'public-rt-boto3'
            },
        ]
    }]
)
public_route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internet_gateway.id)
public_route_table.associate_with_subnet(SubnetId=public_subnet1.id)
public_route_table.associate_with_subnet(SubnetId=public_subnet2.id)

# Function to erase resources
def cleanAll(resourcesDict=None):

    internet_gateway.delete()

    # Delete subnets 
    public_subnet1.delete()
    public_subnet2.delete()
    private_subnet1.delete()
    private_subnet2.delete()
    print("Subnets deleted.")

    # Delete VPC
    vpc.delete
    print("VPC deleted.")