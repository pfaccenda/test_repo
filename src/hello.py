import json
import pprint
import boto3
import botocore
import os
import subprocess
import io
def parse_event_url():
    s="http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/USER_Events.html#RDS-EVENT-0078"

    t=s.split( "#")
    print t[0]
    print t[1]

def print_dict( d,tag="" ):
    print "----------- begin dict", tag, "----------- "
    for k, v in d.items():
        print tag, "--->",   k, "=", v
    print "----------- end dict", tag, "----------- "
    print ""

def print_list( mylist,tag="" ):
    print "----------- begin list", tag, "----------- "
    for i in range(len(mylist)):
        print tag, "[", i, "]","--->",   mylist[i]
    print "----------- end list", tag, "----------- "
    print ""



def demo_event_1():
    event={u'Records': [{u'EventVersion': u'1.0', u'EventSubscriptionArn': u'arn:aws:sns:us-east-1:546771319769:UpefRdsSns:b652ec5e-bc48-4e82-a5b6-dea6556bcec5', u'EventSource': u'aws:sns', u'Sns': {u'SignatureVersion': u'1', u'Timestamp': u'2018-04-05T14:09:00.674Z', u'Signature': u'U1IfO33VLBRrmGpXkHzeC2tcT15deiEOYxxpP0wBNHPX8RrovwbfsUr7homTtkhZtMExbDm5C5ObIOuzI3OOPOeuoLiy6dxwp0lkP1fTVEY1+4hJfP3auD6qPpJ/T52G4jlvVjQ56ahviHhVKY//Pi/+QGxqAdc6K/HCMW0owhDIySPzMLd/ABPK3ygoyo1RTaPNWUd0y1XBBO3sN2prGBXMKbwHlTo59dBg3B4IlbLnhkLD8eHy6fX5eBcdXAuygjw0P37Fu75sf3htnz+N/CPSTTa/7DFRoQzI1UeGO8fN+S/KXW591qvspz6imijbdFo3QI5F8qPQzYozqNiXOg==', u'SigningCertUrl': u'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem', u'MessageId': u'aa1c22e0-bf61-5e94-bc89-71a08f5dde5f', u'Message': u'{"Event Source":"db-instance","Event Time":"2018-04-05 14:04:18.082","Identifier Link":"https://console.aws.amazon.com/rds/home?region=us-east-1#dbinstance:id=upefrdsdb99","Source ID":"upefrdsdb99","Event ID":"http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/USER_Events.html#RDS-EVENT-0005","Event Message":"DB instance created"}', u'MessageAttributes': {}, u'Type': u'Notification', u'UnsubscribeUrl': u'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:546771319769:UpefRdsSns:b652ec5e-bc48-4e82-a5b6-dea6556bcec5', u'TopicArn': u'arn:aws:sns:us-east-1:546771319769:UpefRdsSns', u'Subject': u'RDS Notification Message'}}]}

    pprint.pprint(event, indent=2)

    print_dict( event, "event")
    print_dict( event['Records'][0], "event ---> Records['0']")
    print_dict(event['Records'][0]['Sns'], "event ---> ['Records'][0]['Sns']")

    smessage = event['Records'][0]['Sns']['Message']
    print type(smessage)
    print smessage
    message=json.loads(smessage)
    print_dict( message, "event ---> ['Records'][0]['Sns']['Message']")

    #print_dict( message['Trigger'], "event ---> ['Records'][0]['Sns']['Message']['Trigger']")
    #print_list( message['Trigger']['Dimensions'], "event ---> ['Records'][0]['Sns']['Message']['Trigger']['Dimensions']")
    #print_dict( message['Trigger']['Dimensions'][0], "message['Trigger']['Dimensions'][0]")

    #dimensions=message['Trigger']['Dimensions'][0]
    #print(  dimensions['name'], "=", dimensions['value'])

def demo_event_3():
    event={u'Records': [{u'EventVersion': u'1.0', u'EventSubscriptionArn': u'arn:aws:sns:us-east-1:546771319769:UpefSnsTopic:79788c7b-3c2e-40ff-92af-8c02dbe04743', u'EventSource': u'aws:sns', u'Sns': {u'SignatureVersion': u'1', u'Timestamp': u'2018-04-04T09:43:06.025Z', u'Signature': u'IG74fJfeyGNF3WwWTxZJ1AjVYBJAPg4D/7lDkWtgZb/v/YLntDYWvLyVBGruhYu/Ahrv7dnhH1kUEtjQ7Yv//vjhQP42r/BfRtLDkZuF3Sb14P6LTqtGmOq6Lwxudx/mUs1HCWOlYtx2ES6r+qEk2PqWe3OVy/bbQQS0/rHsbXgqVuaGUR5PW3A+GQTupjdzxhTy5zMoQXcg7wamHj2ZMbNt7uNn6dj9N4MlnCyAZjHbgzf1muWhAiqQfA5mT2rWMbha1osvxSWXMYJwSYjYhoEAk+qlYx/lyezHCptr8KrZgE77lSErLQZr5ixd7dDPPoEEZ2SlTh9oSKBlBzS3aA==', u'SigningCertUrl': u'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem', u'MessageId': u'b25ab905-aeaf-5bfa-baa9-ea3b0ec50da3', u'Message': u'{"Event Source":"db-instance","Event Time":"2018-04-04 09:40:10.307","Identifier Link":"https://console.aws.amazon.com/rds/home?region=us-east-1#dbinstance:id=upefrdsdb02","Source ID":"upefrdsdb02","Event ID":"http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/USER_Events.html#RDS-EVENT-0005","Event Message":"DB instance created"}', u'MessageAttributes': {}, u'Type': u'Notification', u'UnsubscribeUrl': u'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:546771319769:UpefSnsTopic:79788c7b-3c2e-40ff-92af-8c02dbe04743', u'TopicArn': u'arn:aws:sns:us-east-1:546771319769:UpefSnsTopic', u'Subject': u'RDS Notification Message'}}]}
    pprint.pprint(event, indent=2)

    print_dict( event, "event")
    print_dict( event['Records'][0], "event ---> Records['0']")
    print_dict(event['Records'][0]['Sns'], "event ---> ['Records'][0]['Sns']")

    smessage = event['Records'][0]['Sns']['Message']
    print type(smessage)
    print smessage
    message=json.loads(smessage)
    print_dict( message, "event ---> ['Records'][0]['Sns']['Message']")
    print message['Source ID']

def demo_event_4():
    event={
    "Events": [
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb01",
            "Date": "2018-03-24T15:28:33.176Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb01"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb01",
            "Date": "2018-03-31T13:33:50.040Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb01"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb02",
            "Date": "2018-04-04T09:40:10.307Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb02"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb03",
            "Date": "2018-04-04T09:45:53.922Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb03"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb90",
            "Date": "2018-04-05T03:18:18.206Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb90"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb98",
            "Date": "2018-04-05T03:34:31.648Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb98"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb97",
            "Date": "2018-04-05T03:47:38.906Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb97"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb96",
            "Date": "2018-04-05T03:51:12.137Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb96"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb01",
            "Date": "2018-04-05T04:40:23.347Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb01"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb001",
            "Date": "2018-04-05T13:26:26.917Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb001"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb99",
            "Date": "2018-04-05T14:04:18.082Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb99"
        },
        {
            "EventCategories": [
                "creation"
            ],
            "SourceType": "db-instance",
            "SourceArn": "arn:aws:rds:us-east-1:546771319769:db:upefrdsdb88",
            "Date": "2018-04-05T14:28:10.285Z",
            "Message": "DB instance created",
            "SourceIdentifier": "upefrdsdb88"
        }
    ]
}

    pprint.pprint(event, indent=2)

    print_dict( event )
    print_list( event['Events'] )
    for i in range(len(event['Events'])):
        print event['Events'] [i]
        d =  event['Events'] [i]
        print_dict( d, "tag")


def write_text_to_s3_bucket(client, more_binary_data):
    client.put_object(Body=more_binary_data, Bucket='upefbucket', Key='mydata/filename.txt')

def does_bucket_exist( s3, bucket_name='' ):
    bucket = s3.Bucket(bucket_name)
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False
    finally:
        return exists

    s3 = boto3.resource('s3')
    if does_bucket_exist(s3, 'upefbucket') == True:
        print "upefbucket exists"
    else:
        print "upefbucket does not exist"

def s3_bucket_stuff():
    # Text to Binary
    message = "this was written by " + "upef"  # str
    binary_message = message.encode('utf-8')
    print(type(binary_message))  # bytes
    client = boto3.client('s3')
    write_text_to_s3_bucket(client, binary_message)

    message = "this was written by " + "upef --------- 2"  # str
    binary_message = message.encode('utf-8')
    print(type(binary_message))  # bytes
    client = boto3.client('s3')
    write_text_to_s3_bucket(client, binary_message)


# ------------------------------------------------------------------------

def main():
    print "Hello"
    parse_event_url()
    demo_event_1()
    #demo_event_2()
    #demo_event_3()
    demo_event_4()

    d = {   "source": [ "aws.rds", "upef"  ]}
    print_dict(d, "awsrdsevent")
    print d['source'][0]
    print_list(d['source'], "tag")
    # s3_bucket_stuff()


if __name__ == "__main__":
    ## main()
    print "hello"
    s = "Hello"
    b = bytearray(s)
    print b

    print "update bucket sss"

    s3 = boto3.resource('s3')

    fname  = "/tmp/datafile"
    f = open(fname, 'w')
    #f = io.open('/tmp/datafile', 'w', newline='\r\n')
    for i in range( 1, 16):
        f.write('hello to the world!!\r\n')
    f.close()

    s = subprocess.check_output(['/bin/ls', '-l', fname ])
    print (s)

    s = subprocess.check_output(['/bin/wc', '-l', fname])
    print (s)

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(fname, 'upefbucket', 'rdsdata_099.txt')

    s=subprocess.check_output(['/bin/ls', '-l',  fname])
    print (s)




