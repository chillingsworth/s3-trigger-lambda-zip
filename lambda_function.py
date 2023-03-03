import json
import urllib.parse
import boto3
import os
import zipfile
import sys
import shutil

filepath = '/tmp/'

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    bucket = s3.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(filepath + obj.key)):
            os.makedirs(os.path.dirname(filepath + obj.key))
        bucket.download_file(obj.key, filepath + obj.key) # save to same path

def zipfolder(foldername, target_dir):
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    print("Zipobj Created")
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    readBucketName = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        if "/" in key:

            remoteDirectoryName = key.split("/")[0].replace("+"," ")

            writeBucketName="ross-test-write-bucket"
            
            downloadDirectoryFroms3(readBucketName, remoteDirectoryName)
            
            
            zipfolder(filepath + remoteDirectoryName, filepath + remoteDirectoryName)
            
            
            shutil.rmtree(filepath+remoteDirectoryName)
            
            zipfilename = remoteDirectoryName+'.zip'
            
            s3.meta.client.upload_file(filepath+zipfilename, writeBucketName, zipfilename)
            
        return response['ContentType']
    except Exception as e:
        print(e)
        raise e
