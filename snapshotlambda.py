import json
import boto3
from datetime import date
from datetime import timedelta
from collections import defaultdict
from dateutil import parser
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
  
def getdeletedate(thisdate):
 deletedate=None
 if thisdate in firstmondays:
  deletedate = thisdate + timedelta((6*365/12))
  print("deletedate is" + deletedate.isoformat())
 else:
  if thisdate in thisyearandnextyearmondays:
   deletedate=thisdate + timedelta(days=30)
   print("deletedate is" + deletedate.isoformat())
  else:
   deletedate=thisdate + timedelta(days=7)
   print("deletedate is"+deletedate.isoformat())
 return deletedate

def lambda_handler(event, context):
    # TODO implement
# Connect to EC2
 ec2 = boto3.resource('ec2')
 client = boto3.client('ec2')
# Get information for all running instances
 running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']},
    {'Name':'tag:Backup', 'Values':['Daily']}])

 ec2info = defaultdict()
 for instance in running_instances:
  tags = instance.tags
  tags.extend([{
           'Key': 'DeleteDate',
           'Value': getdeletedate(date.today()).isoformat()
       },{
           'Key': 'InstanceId',
           'Value': instance.id
       },{
           'Key': 'InstanceType',
           'Value': instance.instance_type
       },{
           'Key': 'InstanceInternalIp',
           'Value': instance.private_ip_address
       },{
           'Key': 'InstancePublicIp',
           'Value': instance.public_ip_address
       }])
  for volume in instance.volumes.all():
   for attachment in volume.attachments:
    tags.extend([{'Key':'MountPoint','Value':attachment.get('Device')}])
    print(tags)
   response = client.create_snapshot(
   Description='lambda snapshot for '+instance.id+' deletedate='+getdeletedate(date.today()).isoformat(),
    VolumeId=volume.id,
    TagSpecifications=[{
            'ResourceType': 'snapshot',
            'Tags': tags,
        },],)
   print(response)
