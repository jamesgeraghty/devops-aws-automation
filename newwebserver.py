#!/usr/bin/env python3
from datetime import date
import json
import datetime 
import time
import sys
import subprocess
import boto3
import requests # to get image from the web
import shutil
ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")
user_data = '''#!/bin/bash
yum update -y
yum install httpd -y
systemctl enable httpd
systemctl start httpd'''
new_instance = ec2.create_instances(
  ImageId='ami-0fc970315c2d38f01',
  KeyName= 'wit41',
  MinCount=1,
  MaxCount=1,
  InstanceType='t2.nano',
  UserData=user_data,
  SecurityGroupIds=['sg-065ff0bcd5c101a94'],
  TagSpecifications=[
        {
            'ResourceType':'instance',
            'Tags': [
                {
                    'Key': 'NAME',
                    'Value': 'web server'
                },
            ]
        },
    ],
)

print (new_instance[0].id)
new_instance[0].wait_until_running()



image_url = "http://devops.witdemo.net/image.jpg"
filename = image_url.split("/")[-1]

r = requests.get(image_url, stream = True)


if r.status_code == 200:

    r.raw.decode_content = True
    

    with open(filename,'wb') as f:
        shutil.copyfileobj(r.raw, f)
         
    print('Image sucessfully Downloaded: ',filename)
else:
    print('Image Couldn\'t be retreived')
    new_instance[0].reload()
print (new_instance[0].public_ip_address)
s3 = boto3.resource("s3")
bucket_name = "s3-bucket-assignment" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
new_bucket = s3.create_bucket(Bucket = bucket_name, ACL= 'public-read', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
object_name ="image.jpg"
try:
    response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'), ACL= 'public-read', ContentType='image/jpeg' )
    print (response)
except Exception as error:
    print (error)
new_instance
new_instance[0].reload()
print (new_instance[0].public_ip_address)
time.sleep(120)

new_instance[0].reload()

remote_cmd1 = 'echo "James Geraghty 20022946 Devops Assignment 1 " > index.html'
remote_cmd9 = 'sudo cp index.html /var/www/html'

cmd1= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " '" + remote_cmd1 + "'"
cmd2= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<br> Here is the image: <br> '  >> index.html "'''
cmd3= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<img src='https://"''' + bucket_name + '''".s3-eu-west-1.amazonaws.com/image.jpg'>' >> index.html"'''
cmd4= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<br> Private IP Address: <br>' >> index.html "'''
cmd5= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  " ' curl http:// 169.254.169.254/latest/meta-data/local-ipv4 >> index.html' "
cmd6= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " 'curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html'"
cmd7= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  " ' curl http:// 169.254.169.254/latest/meta-data/mac >> index.html' "
cmd8= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " 'curl -s http://169.254.169.254/latest/meta-data/placement/hostname >> index.html'"
cmd9= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " sudo cp index.html /var/www/html " 

print (cmd1)          # for debugging
print (cmd2)
print (cmd3)
print (cmd4)
print (cmd5)
print (cmd6)
print (cmd7)
print (cmd8)
print (cmd9)

response = subprocess.run(cmd1, shell=True) 
print (response)            # for debugging
response = subprocess.run(cmd2, shell=True)
print (response)
response = subprocess.run(cmd3, shell=True)
print (response)
response = subprocess.run(cmd4, shell=True)
print (response)
response = subprocess.run(cmd5, shell=True)
print (response)
response = subprocess.run(cmd6, shell=True)
print (response)
response = subprocess.run(cmd7, shell=True)
print (response)
response = subprocess.run(cmd8, shell=True)
print (response)
response = subprocess.run(cmd9, shell=True)
print (response)



new_instance[0].reload()

monitor1= "scp -i wit41.pem monitor.sh ec2-user@" + new_instance[0].public_ip_address + ":."

monitor2= "ssh -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " ' ./monitor.sh'"

print (monitor1)
print (monitor2)

try:
    response = subprocess.run(monitor1, shell=True)
    print (response)
except Exception as error:
    print (error)
try:
    response = subprocess.run(monitor2, shell=True)
    print (response)
except Exception as error:
    print (error)

