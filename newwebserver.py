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
#user data is used to create the apache server
user_data = '''#!/bin/bash
yum update -y
yum install httpd -y
systemctl enable httpd
systemctl start httpd'''
#creating the a new instance 
new_instance = ec2.create_instances(
  ImageId='ami-0fc970315c2d38f01',
  KeyName= 'wit41',
  MinCount=1,
  MaxCount=1,
  InstanceType='t2.nano',
  UserData=user_data,
# securitygroup = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id), 
# securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22),  
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
#prints out the instance ID to the terminal
print (new_instance[0].id)
#waits until the instance is running before  proceeding 
new_instance[0].wait_until_running()
# the Url from where the image will be taken
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
# reloads the instance to make sure there is no delays
    new_instance[0].reload()
print (new_instance[0].public_ip_address)
s3 = boto3.resource("s3")
# Creating a s3 bucket and generates a random code for the bucket name  
bucket_name = "s3-bucket-assignment" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
new_bucket = s3.create_bucket(Bucket = bucket_name, ACL= 'public-read', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
#declaring the object  name variable 
object_name ="image.jpg"
# uploads the image to the s3 bucket
try:
    response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'), ACL= 'public-read', ContentType='image/jpeg' )
    print (response)
except Exception as error:
    print (error)
new_instance
#the reload method make sure that all the data that will collected is up to date 
new_instance[0].reload()
print (new_instance[0].public_ip_address)
# adding a delay timer 
time.sleep(120)

new_instance[0].reload()

remote_cmd1 = 'echo "James Geraghty 20022946 Devops Assignment 1 " > index.html'
remote_cmd12 = 'sudo cp index.html /var/www/html'

cmd1= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " '" + remote_cmd1 + "'"
cmd2= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<br> Here is the image: <br> '  >> index.html "'''
cmd3= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<img src='https://"''' + bucket_name + '''".s3-eu-west-1.amazonaws.com/image.jpg'>' >> index.html"'''
cmd4= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<br> Private IP Address: <br>' >> index.html "'''
cmd5= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  " ' curl http:// 169.254.169.254/latest/meta-data/local-ipv4 >> index.html' "
cmd6= "ssh -o StrictHostkeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<br> Availability Zone : <br>' >> index.html "'''
cmd7= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " 'curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html'"
cmd8= "ssh -o StrictHostkeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<br> Mac Address: <br>' >> index.html "'''
cmd9= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  " ' curl http:// 169.254.169.254/latest/meta-data/mac >> index.html' "
cmd10= "ssh -o StrictHostkeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address +  ''' "echo '<br> Host Name: <br>' >> index.html "'''
cmd11= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " 'curl -s http://169.254.169.254/latest/meta-data/public-hostname >> index.html'"
cmd12= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " sudo cp index.html /var/www/html " 

print (cmd1)          # for debugging
print (cmd2)
print (cmd3)
print (cmd4)
print (cmd5)
print (cmd6)
print (cmd7)
print (cmd8)
print (cmd9)
print (cmd10)
print (cmd11)
print (cmd12)

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
repsonse = subprocess.run(cmd10, shell=True)
print (response)
repsonse = subprocess.run(cmd11, shell=True)
print (response)
repsonse = subprocess.run(cmd12, shell=True)
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

cloudwatch1= "scp -o StrictHostKeyChecking=no -i wit41.pem cloudwatch.py ec2-user@" + new_instance[0].public_ip_address + ":."
cloudwatch2= "ssh -o StrictHostKeyChecking=no -i wit41.pem ec2-user@" + new_instance[0].public_ip_address + " ' ./cloudwatch.py'"
print (cloudwatch1)
print (cloudwatch2)

try:
    response = subprocess.run(cloudwatch1, shell=True)
    print (response)
except Exception as error:
    print (error)
try:
    response = subprocess.run(cloudwatch2, shell=True)
    print (response)
except Exception as error:
    print (error)
