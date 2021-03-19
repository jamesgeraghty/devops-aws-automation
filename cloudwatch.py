#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta
import time

cloudwatch = boto3.resource('cloudwatch')
ec2 = boto3.resource('ec2')

instid = input("Please enter instance ID: ")    # Prompt the user to enter an Instance ID
instance = ec2.Instance(instid)
instance.monitor()  # Enables detailed monitoring on instance (1-minute intervals)
time.sleep(360)     # Wait 6 minutes to ensure we have some data (can remove if not a new instance)

metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                            MetricName='CPUUtilization',
                                            Dimensions=[{'Name':'InstanceId', 'Value': instid}])

metric = list(metric_iterator)[0]    # extract first (only) element

response = metric.get_statistics(StartTime = datetime.utcnow() - timedelta(minutes=5),   # 5 minutes ago
                                 EndTime=datetime.utcnow(),                              # now
                                 Period=300,                                             # 5 min intervals
                                 Statistics=['Average'])

print ("Average CPU utilisation:", response['Datapoints'][0]['Average'], response['Datapoints'][0]['Unit'])
