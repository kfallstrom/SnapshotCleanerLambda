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
 ec2 = boto3.resource('ec2')
 client = boto3.client('ec2')
  # Get information for all running instances
 instance_snapshots = ec2.snapshots.filter(Filters=[{'Name':'tag:DeleteDate', 'Values':[getdeletedate(date.today()).isoformat()]}])
 for snapshot in instance_snapshots:
  print("this snapshot will be deleted",snapshot.id," delete date",getdeletedate(date.today()).isoformat())
  #response= client.delete_snapshot(snapshot.id)
