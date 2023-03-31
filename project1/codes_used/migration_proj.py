
#importing requred libraries

import requests
import boto3
import zipfile
import io


#mentioning aws credentials

AWS_ACCESS_KEY_ID = 'AKIA3ML5IGQI***********'
AWS_SECRET_ACCESS_KEY = 'nUpxEOnCawB+/mKomfGGoxn*************'


#making the client connecting to bucket 

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                  
                  )


#creating AWS S3 bucket

response = s3.create_bucket(Bucket="migration-proj",
                            CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})
print("bucket created")


BUCKET_NAME = 'migration-proj'


#from here downloading the reqired zipfile has started                  

url = 'https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip'

headers= {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
print("download started")
response = requests.get(url,headers = headers, stream= True)

f = io.BytesIO(response.content)
print("download finished")

print(response)

#the downloded zipfile put into s3 bucket

s3.put_object(Bucket=BUCKET_NAME, Key='submissions.zip', Body=f)

print("object succesfully put into s3 bucket")

#creating bucket to unzip the file

print("started")

response = s3.create_bucket(Bucket="varahi",
                            CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})
print("bucket created")

obj_key = 'submissions.zip'

#reading into memory
print ("reading into memory started")

s3_obj = s3.get_object(Bucket=BUCKET_NAME, Key=obj_key)


#from here extractting of zip file located in s3 starts unzipping.

zip_file = zipfile.ZipFile(io.BytesIO(s3_obj['Body'].read()))
bucket1='varahi'

print("extracting the file started to our destination")

 
i=0
for filename in zip_file.namelist():
           
             unzipped_content = zip_file.read(filename)

             unzipped_key = 'unzipped' + filename 
            
             s3.put_object(Bucket=bucket1, Key= unzipped_key, Body=unzipped_content)

             print("files extracted successsfully to unzipped folder")
             i=i+1
             if i==150:
                break          
print("process finished")