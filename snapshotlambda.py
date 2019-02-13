import json
import boto3
from datetime import date
from collections import defaultdict
thisyearandnextyearmondays = []
firstmondays = []
earliestmonday = None
todaydate = date.today()
#365 + 365 = 730 days
for x in range(730):
 #if date is a monday, add to list
 ordinalvalue = date.today().replace(month=1,day=1).toordinal()+x
 datevalue = date.fromordinal(ordinalvalue)
 #only Mondays
 if datevalue.weekday()==0:
  if earliestmonday is None:
   earliestmonday = datevalue
#keep earliest monday for the month
  thisyearandnextyearmondays.append(datevalue)
  if earliestmonday.month == datevalue.month and earliestmonday.year == datevalue.year and datevalue.day<earliestmonday.day:
   earliestmonday=datevalue
  elif earliestmonday.month != datevalue.month and earliestmonday.year == datevalue.year:
   firstmondays.append(earliestmonday)
   earliestmonday = datevalue
  elif earliestmonday.month != datevalue.month and earliestmonday.month==12 and earliestmonday.year != datevalue.year:
   firstmondays.append(earliestmonday)
   earliestmonday = datevalue
  else:
   continue
for x in firstmondays:
 print(x)
print("all mondays")
for x in thisyearandnextyearmondays:
 print(x)
if todaydate in thisyearandnextyearmondays:
 print("deletedate is" + todaydate + timedelta(days=7))
if todaydate in firstmondays:
 print("deletedate is" + todaydate + timedelta(months=6))
 
def lambda_handler(event, context):
    # TODO implement
# Connect to EC2
 ec2 = boto3.resource('ec2')

# Get information for all running instances
 running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']},
    {'Name':'tag:Backup', 'Values':['Daily']}])

 ec2info = defaultdict()
 for instance in running_instances:
  for tag in instance.tags:
   if 'Name'in tag['Key']:
    name = tag['Value']
    # Add instance info to a dictionary         
    ec2info[instance.id] = {
        'Name': name,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'Launch Time': instance.launch_time
        }

 attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
 for instance_id, instance in ec2info.items():
  # Get information for all running instances
  instance_snapshots = ec2.snapshots.filter(Filters=[
    {'Name':'tag:InstanceId', 'Values':[instance_id]}])
  for snapshot in instance_snapshots:
   print(instance_id,snapshot.id)
  #for key in attributes:
  # print("{0}: {1}".format(key, instance[key]))
  # print("------")
