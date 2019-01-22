import boto3
from datetime import date
client = boto3.client('ec2', 'us-east-1'')
ec2 = boto3.resource('ec2', 'us-east-1')
thisyearandnextyearmondays = []
firstmondays = []
earliestmonday = None
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
  elif earliestmonday.month < datevalue.month and earliestmonday.year == datevalue.year:
   firstmondays.append(earliestmonday)
   earliestmonday = None
  else:
   continue
for x in firstmondays:
 print(x)
print "all mondays"
for x in thisyearandnextyearmondays:
 print(x)

    
def lambda_handler(event, context):                      
                          
    myAccount = boto3.client('sts').get_caller_identity()['Account']
        snapshots = client.describe_snapshots(MaxResults=1000, OwnerIds=[myAccount])['Snapshots']
            for snapshot in snapshots:
                #TODO get tags, compare deleteon tag with today_date          
                #if snapshot['Description'].find(image) > 0:
                    snap = client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    print "Deleting snapshot " + snapshot['SnapshotId']
                    print "-------------"

