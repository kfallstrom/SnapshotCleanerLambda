    import boto3
    import datetime
    client = boto3.client('ec2', 'us-east-1'')
    ec2 = boto3.resource('ec2', 'us-east-1')
    today_date = time.strptime(today_time, '%m-%d-%Y')
    
    
def lambda_handler(event, context):                      
                          
    myAccount = boto3.client('sts').get_caller_identity()['Account']
        snapshots = client.describe_snapshots(MaxResults=1000, OwnerIds=[myAccount])['Snapshots']
            for snapshot in snapshots:
                #TODO get tags, compare deleteon tag with today_date          
                #if snapshot['Description'].find(image) > 0:
                    snap = client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    print "Deleting snapshot " + snapshot['SnapshotId']
                    print "-------------"

