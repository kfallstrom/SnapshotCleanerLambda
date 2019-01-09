    import boto3
    import datetime
    client = boto3.client('ec2',region_name='us-west-1')
    snapshots = client.describe_snapshots(OwnerIds=['12345678'])
    for snapshot in snapshots['Snapshots']:
       a= snapshot['StartTime']
       b=a.date()
       c=datetime.datetime.now().date()
       d=c-b
       try:
        if d.days>10:
           id = snapshot['SnapshotId']
        //   client.delete_snapshot(SnapshotId=id)
       except Exception,e:
        if 'InvalidSnapshot.InUse' in e.message:
           print "skipping this snapshot"
           continue
