#! /usr/bin/env python

import boto3
import os, sys
import json
import datetime

# list all metrics about all rds db instances
def list_all():
    client = boto3.client('cloudwatch')
    response = client.list_metrics(Namespace='AWS/RDS')

    for index in range(len(response['Metrics'])):
        print index
        d = response['Metrics'][index]

        for k in d['Dimensions']:
            print k['Name'], "=", k['Value']

        for k, v in d.items():
            print  k, " = ", v
        print ""

# list a specific metric for an rds dbinstance, e.g.
# aws cloudwatch list-metrics --namespace  "AWS/RDS"   --metric-name FreeStorageSpace --dimensions \
# "Name="DBInstanceIdentifier",Value=upefrdsdb01"
def list_metric(dbinstance_name,metric_name):
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
        for k in d['Dimensions']:
            print k['Name'], "=", k['Value']

        for k, v in d.items():
            print  k, "=", v
        print ""


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

# add a custom tag to an rds dbinstance
def add_tag_to_resource( dbname,
                         mykeyname='upefKey',
                         mykeyvalue="default"):

    if mykeyvalue == "default":
        mykeyvalue =  str(datetime.datetime.now())

    client = boto3.client('rds')
    response = client.add_tags_to_resource(
        ResourceName=dbname,
        Tags=[
            {
                'Key': mykeyname,
                'Value': mykeyvalue

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
    print "------------------------- ", "describe_dbinstance", dbname,  "------------------------- "
    d = response
    for k, v in d.items():
        print  k, "=", v
        for dd in d['DBInstances']:
            for k,v in dd.items():
                print k, "=",v

    print "------------------------- ", "describe_dbinstance", dbname,  "------------------------- "
    print ""


def modify_dbinstance_setting( dbname ):
    client = boto3.client('rds')

    response = client.describe_db_instances(DBInstanceIdentifier=dbname)
    d = response['DBInstances'][0]
    print "Original value of MonitoringInterval for", dbname, "is", d.get('MonitoringInterval')

    response = client.modify_db_instance( DBInstanceIdentifier=dbname,
                                          MonitoringInterval=30 )

    response = client.describe_db_instances( DBInstanceIdentifier=dbname )

    print "------------------------- ", "modify_dbinstance_setting", dbname,  "------------------------- "
    d = response['DBInstances']
    for index in range(len(response['DBInstances'])):
        d = response['DBInstances'][index]
        print "MonitoringInterval for ", dbname, "changed to", d.get('MonitoringInterval')
    print "------------------------- ", "modify_dbinstance_setting", dbname,  "------------------------- "

    print ""

def get_account_number():
    client = boto3.client('iam')
    response = client.get_user()
    print response

    retval = ""
    print "------------------------- ", "user info", "------------------------- "
    d =  response['User']
    for k,v in d.items():
        print k,"=",v
        if k == "Arn":
           str = v
           tokenlist = str.split(':')
           retval = tokenlist[4]

    print "------------------------- ", "user info", "------------------------- "

    return retval

def main():
    # all will lsit all metrics for all instances
    # <dbinstance> will list its metrics, get info about named alarms, add or modify a custom
    # tag for the instance, display info about the instance and modify a setting
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

        add_tag_to_resource( 'arn:aws:rds:us-east-1:546771319769:db:upefrdsdb01' )
        add_tag_to_resource( 'arn:aws:rds:us-east-1:546771319769:db:upefrdsdb01', 'upefKey-02', "hello" )

        describe_dbinstance( sys.argv[1] )
        modify_dbinstance_setting(sys.argv[1] )

        my_session = boto3.session.Session()
        my_region = my_session.region_name
        print "region:", my_region

        s = get_account_number()
        print "account number:", s

    print ""
    print "v2.4"

if __name__ == '__main__':
    main()
