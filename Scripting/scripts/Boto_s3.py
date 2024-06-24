import boto3 # boto3 is the python SDK for AWS

# create a session with boto3
session = boto3.session(
    aws_access_key_id='Your Access Key ID',
    aws_secret_access_key='Your Secret access key'
)

# creating s3 resource from the session
s3 = boto3.resource('s3')

# Method 1
# key -> name of the file/folder
copy_source = {
    'Bucket':'mybucket',
    'key':'mykey'
}

bucket = s3.Bucket('otherbucket') # name of other bucket
bucket.copy(copy_source,'otherkey') # name of the  new file where you want to store


# Method 2
# choose the source and destination buckets and move everything there is present
srcbucket = s3.bucket('source_bucket')
destbucket = s3.bucket('dest_bucket')

# Iterate over all the objects inside the bucket
for file in srcbucket.objects.all():
    copy_source = {
        'Bucket':'mybucket',
        'key':'mykey'
    }

    destbucket.copy(copy_source,'mykey')
    print(f"'mykey' + is copied")

    #to delete the file after copying   
    file.delete()