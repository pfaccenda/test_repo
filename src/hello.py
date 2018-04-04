import json
import pprint
import boto3
import botocore


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
    for item in mylist:
        print tag, "--->",   item
    print "----------- end list", tag, "----------- "
    print ""


def demo_event_1():
    event={u'Records': [{u'EventVersion': u'1.0', u'EventSubscriptionArn': u'arn:aws:sns:us-east-1:546771319769:UpefSnsTopic:79788c7b-3c2e-40ff-92af-8c02dbe04743', u'EventSource': u'aws:sns', u'Sns': {u'SignatureVersion': u'1', u'Timestamp': u'2018-04-03T10:35:31.001Z', u'Signature': u'dthdqgOjH/O0lhqoY1302gcx3sR/KRd2pjLY/MQ4o3zNGkWiCP0izshpNIEMkrZOlqIMzzuAELxqhvGmUQ2pWfRKK0CwGX2i/zFvuwZxoM+44LJssUkFvQ5fLO/1Oe5JkvjLpOGg2vacj0m2PhVTSdmpqTsInUidkwMcw3S7EOCCXUO1y6c2q8enDl5dDe3t7PbNZ6kvh1bh4DyvSWuK3Z7TIiF/fDbQ+dJ4/e8Nom65okFunudw6jcWTuEto45hgoHDKqPHwVJs1Y9IK6eM8c/+rZuDadihjQKq+bLV5vpRFxic+tWkjLaFEDNwvIetOZmN08Qf//JAK6deYjpS+A==', u'SigningCertUrl': u'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem', u'MessageId': u'72ebbf4b-325a-5e0c-bcc1-ec7669698abe', u'Message': u"StackId='arn:aws:cloudformation:us-east-1:546771319769:stack/upefjunkalarm/7d365610-361b-11e8-97d6-500c28604c82'\nTimestamp='2018-04-03T10:35:30.836Z'\nEventId='bb8379b0-372a-11e8-911f-50d5ca63261e'\nLogicalResourceId='upefjunkalarm'\nNamespace='546771319769'\nPhysicalResourceId='arn:aws:cloudformation:us-east-1:546771319769:stack/upefjunkalarm/7d365610-361b-11e8-97d6-500c28604c82'\nPrincipalId='546771319769'\nResourceProperties='null'\nResourceStatus='DELETE_IN_PROGRESS'\nResourceStatusReason='User Initiated'\nResourceType='AWS::CloudFormation::Stack'\nStackName='upefjunkalarm'\nClientRequestToken='Console-DeleteStack-34f6c1a5-5530-4410-b7ba-c74eae1e79b2'\n", u'MessageAttributes': {}, u'Type': u'Notification', u'UnsubscribeUrl': u'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:546771319769:UpefSnsTopic:79788c7b-3c2e-40ff-92af-8c02dbe04743', u'TopicArn': u'arn:aws:sns:us-east-1:546771319769:UpefSnsTopic', u'Subject': u'AWS CloudFormation Notification'}}]}

    pprint.pprint(event, indent=2)

    print_dict( event, "event")
    print_dict( event['Records'][0], "event ---> Records['0']")
    print_dict(event['Records'][0]['Sns'], "event ---> ['Records'][0]['Sns']")

def demo_event_2():
    event = {u'Records': [{u'EventVersion': u'1.0', u'EventSubscriptionArn': u'arn:aws:sns:us-east-1:546771319769:UpefSnsTopic:79788c7b-3c2e-40ff-92af-8c02dbe04743', u'EventSource': u'aws:sns', u'Sns': {u'SignatureVersion': u'1', u'Timestamp': u'2018-04-02T17:20:55.469Z', u'Signature': u'bzdwyjkAMnCz2MKomy2UrgIan/x+Cn4tU4zzHQUA/JtOif5/op3l0CCQ+5fa9dPX3wJbrOnyGlRx3jGVSwTuvF6vGR27yI0AOCN5axQrAOzhDpezx3bk39oK39xuJnttx3vzUsyyVSE+1LPHSg3HxNA2gGCytDizq9ryEFWtiOky7hOBUwegwXMv8H8PuZhm/fNG5spAdyjS0JezbZXP4nimWBtha4NlwLAwc7BP0bO955bE1uPF38bRAkajpUBo6S+rgJhFRVelWc05amvTbxS/kCV2KWfskawxlIan6WQ45CHf3brUxBJJX0GTkUTJgIJFHq/Ql9O68ZHkaR0bBg==', u'SigningCertUrl': u'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem', u'MessageId': u'a495dd95-42e8-5bb6-aa63-8ea92a5fa705', u'Message': u'{"AlarmName":"awsrds-upefrdsdb01-High-Write-Latency","AlarmDescription":"awsrds-upefrdsdb01-High-Write-Latency","AWSAccountId":"546771319769","NewStateValue":"ALARM","NewStateReason":"Threshold Crossed: 1 out of the last 1 datapoints [0.006189117634776799 (02/04/18 17:15:00)] was greater than or equal to the threshold (0.004) (minimum 1 datapoint for OK -> ALARM transition).","StateChangeTime":"2018-04-02T17:20:55.431+0000","Region":"US East (N. Virginia)","OldStateValue":"OK","Trigger":{"MetricName":"WriteLatency","Namespace":"AWS/RDS","StatisticType":"Statistic","Statistic":"AVERAGE","Unit":null,"Dimensions":[{"name":"DBInstanceIdentifier","value":"upefrdsdb01"}],"Period":300,"EvaluationPeriods":1,"ComparisonOperator":"GreaterThanOrEqualToThreshold","Threshold":0.004,"TreatMissingData":"","EvaluateLowSampleCountPercentile":""}}', u'MessageAttributes': {}, u'Type': u'Notification', u'UnsubscribeUrl': u'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:546771319769:UpefSnsTopic:79788c7b-3c2e-40ff-92af-8c02dbe04743', u'TopicArn': u'arn:aws:sns:us-east-1:546771319769:UpefSnsTopic', u'Subject': u'ALARM: "awsrds-upefrdsdb01-High-Write-Latency" in US East (N. Virginia)'}}]}

    pprint.pprint(event, indent=2)

    print_dict( event, "event")
    print_dict( event['Records'][0], "event ---> Records['0']")
    print_dict(event['Records'][0]['Sns'], "event ---> ['Records'][0]['Sns']")

    smessage = event['Records'][0]['Sns']['Message']
    print type(smessage)
    print smessage
    message=json.loads(smessage)
    print_dict( message, "event ---> ['Records'][0]['Sns']['Message']")

    print_dict( message['Trigger'], "event ---> ['Records'][0]['Sns']['Message']['Trigger']")
    print_list( message['Trigger']['Dimensions'], "event ---> ['Records'][0]['Sns']['Message']['Trigger']['Dimensions']")
    print_dict( message['Trigger']['Dimensions'][0], "message['Trigger']['Dimensions'][0]")

    dimensions=message['Trigger']['Dimensions'][0]
    print(  dimensions['name'], "=", dimensions['value'])

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
    demo_event_2()
    demo_event_3()

    # s3_bucket_stuff()


if __name__ == "__main__":
    main()

