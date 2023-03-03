import boto3
import os
import zipfile
import sys
import shutil

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    bucket = s3.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path

def zipfolder(foldername, target_dir):            
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])

s3 = boto3.resource('s3')

readBucketName="ross-test-read-bucket"
writeBucketName="ross-test-write-bucket"
remoteDirectoryName="folder 7"

downloadDirectoryFroms3(readBucketName, remoteDirectoryName)

zipfolder(remoteDirectoryName, remoteDirectoryName) #insert your variables here

shutil.rmtree(remoteDirectoryName)

zipfilename = remoteDirectoryName+'.zip'

s3.meta.client.upload_file(zipfilename, writeBucketName, zipfilename)