import boto3

# Create an S3 client
s3 = boto3.client("s3")

# Region Name
region_name = "us-west-2"

# Set Bucket Name
bucket_name = "jonnie-first-bucket"

# Call S3 to list current buckets
response = s3.list_buckets()

# Create a bucket and configure in specified region
s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region_name})

# Get a list of all bucket names from the response
for bucket in response["Buckets"]:
    print("BucketName:{}".format(bucket["Name"]))
