#!/usr/bin/bash
#
# Sample basic monitoring functionality; Tested on Amazon Linux 2
#
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
#PUBLIC_IP=$(curl -s http://196.254.169.254/latest/meta-data/local-ipv4)
MEMORYUSAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
UPTIME=$(uptime |awk '{ print $3 $4 }')
PROCESSES=$(expr $(ps -A | grep -c .) - 1)
HTTPD_PROCESSES=$(ps -A | grep -c httpd)


echo "Instance ID: $INSTANCE_ID"
#echo "Public Ip: $PUBLIC_IP"
echo "Uptime: $UPTIME"
echo "Memory utilisation: $MEMORYUSAGE"
echo "No of processes: $PROCESSES"
if [ $HTTPD_PROCESSES -ge 1 ]
then
    echo "Web server is running"
else
    echo "Web server is NOT running"
fi

