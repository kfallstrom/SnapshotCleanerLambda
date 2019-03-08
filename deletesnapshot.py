import json
import boto3
from datetime import date

def lambda_handler(event, context):
    # TODO implement
 ec2 = boto3.resource('ec2')
 client = boto3.client('ec2')
  # Get information for all running instances
 todaydeletedate=date.today().isoformat()
 print("this run deletes snapshots with deletedate:",todaydeletedate)
 instance_snapshots = ec2.snapshots.filter(Filters=[{'Name':'tag:DeleteDate', 'Values':[todaydeletedate]}])
 for snapshot in instance_snapshots:
  print("this snapshot will be deleted",snapshot.id," delete date",date.today().isoformat())
  response=client.delete_snapshot(SnapshotId=snapshot.id)
