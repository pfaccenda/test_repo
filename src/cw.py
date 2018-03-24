#! /usr/bin/env python

import boto3
import os, sys
import json
import datetime

def list_all():
    client = boto3.client('cloudwatch')
    response = client.list_metrics(Namespace='AWS/RDS')

    for index in range(len(response['Metrics'])):
        print index
        d = response['Metrics'][index]

        for k, v in d.items():
            print  k, " = ", v

        for k in d['Dimensions']:
            print k['Name'], "=", k['Value']

        print ""


def list_metric(dbinstance_name,metric_name):
    # aws cloudwatch list-metrics --namespace  "AWS/RDS"   --metric-name FreeStorageSpace --dimensions #"Name="DBInstanceIdentifier",Value=upefrdsdb01"

    dbinstance_name = 'upefrdsdb01'

    client = boto3.client('cloudwatch')
    response = client.list_metrics(
        Namespace='AWS/RDS',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': dbinstance_name
            }
        ]
    )

    for index in range(len(response['Metrics'])):
        d = response['Metrics'][index]
        for k, v in d.items():
            print  k, " = ", v

        for k in d['Dimensions']:
            print k['Name'], "=", k['Value']

        print ""


# aws cloudwatch describe-alarms-for-metric --namespace  "AWS/RDS"   --metric-name FreeStorageSpace --dimensions #"Name="DBInstanceIdentifier",Value=upefrdsdb01"

# aws cloudwatch put-metric-alarm --alarm-name upef-stack-04-FreeStorageAlarm-YQ5WMOBCU981 --alarm-description  # "upef_alarm_upefrdsdb01" --metric-name FreeStorageSpace  --namespace  "AWS/RDS"   --period 60 --evaluation-periods 2 --threshold 5 # --comparison-operator GreaterThanThreshold  --statistic Maximum

def describe_alarms( alarm_name ):
    client = boto3.client('cloudwatch')
    response = client.describe_alarms(
        AlarmNames=[
            alarm_name,
        ]
    )

    print "---------------------- BEGIN ALARM DESCRIPTION ", alarm_name, "---------------------------"
    for index in range(len( response['MetricAlarms'] )):
        d = response['MetricAlarms'][index]

        for k,v in d.items():
            print  k, "=",  v
    print "---------------------- END ALARM DESCRIPTION ", alarm_name, "---------------------------"
    print ""

def add_tag_to_resource( dbname ):

    key_value =  str(datetime.datetime.now())
    client = boto3.client('rds')
    response = client.add_tags_to_resource(
        ResourceName=dbname,
        Tags=[
            {
                'Key': 'upefKey',
                'Value': key_value

            }
        ]
    )

    print "------------------------- ", "add tag to resource", "------------------------- "
    d = response['ResponseMetadata']
    for k, v in d.items():
        print  k, "=", v
    print "------------------------- ", "add tag to resource", "------------------------- "
    print ""

def describe_dbinstance(dbname):
    client = boto3.client('rds')
    response = client.describe_db_instances( DBInstanceIdentifier=dbname )
    # print response
    print "------------------------- ", "describe_dbinstance", dbname,  "------------------------- "
    d = response
    for k, v in d.items():
        print  k, "=", v
        for dd in d['DBInstances']:
            for k,v in dd.items():
                print k, "=",v

    print "------------------------- ", "describe_dbinstance", dbname,  "------------------------- "
    print ""



def main():
    if len(sys.argv) <= 1:
        sys.exit(sys.argv[0] + "all | <dbinstance>")

    if sys.argv[1] == "all":
        list_all()
    else:
        list_metric(sys.argv[1], "FreeStorageSpace")
        list_metric(sys.argv[1], "WriteThroughput")

        alarm_list = [ "awsrds-upefrdsdb01-High-Write-IOPS",
                       'awsrds-upefrdsdb01-High-Read-IOPS-custom',
                       'awsrds-upefrdsdb01-CPU-Utilization',
                       'awsrds-upefrdsdb01-High-Write-Latency'
                     ]

        for alarm_name in alarm_list:
            describe_alarms( alarm_name )

    add_tag_to_resource( 'arn:aws:rds:us-east-1:546771319769:db:upefrdsdb01')
    describe_dbinstance( sys.argv[1] )


if __name__ == '__main__':
    main()

