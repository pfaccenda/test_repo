#! /usr/bin/env python

import boto3
import os, sys
import json
import datetime
import time
import calendar


def exp_rds_paginator():
    client = boto3.client('rds')
    response = client.describe_db_instances(MaxRecords=20)
    print( response )
    print_dict(response)
    print_list( response['DBInstances'])

def exp_kinesis_info():
    print "exp_kinesis_info"
    client = boto3.client('kinesis')
    response = client.list_streams(  Limit=123 )
    print response
    print_dict( response )



def exp_s3_info():
    print "########################### S3 BUCKET INFO ################################"
    # Create an S3 client
    s3 = boto3.client('s3')

    # Call S3 to list current buckets
    response = s3.list_buckets()
    print response
    print_dict( response )
    print_dict( response['Owner'] )
    print_list( response['Buckets'] )

    keywordlist = ["CreationDate"]
    for i in range(len( response['Buckets'] )):
        print_dict(  response['Buckets'][i], "S3bucket" )

        bucket_creation_time = response['Buckets'][i]['CreationDate']
        age_in_seconds = time_diff_seconds(bucket_creation_time,
                                           datetime.datetime.utcnow())
        print "bucket_age is", age_in_seconds / (60 * 60 * 24), "days"
        print "bucket_age is", age_in_seconds / (60 * 60), "hours"

        age_in_fractional_days = (age_in_seconds / (60.0 * 60.0)) / 24
        print "bucket_age_in_fractional_days =", age_in_fractional_days

    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    # Print out the bucket list
    print("Bucket List: %s" % buckets)

    # Print out bucket names
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print bucket.name, bucket.creation_date

    print "########################### S3 BUCKET INFO ################################"

def list_dynamodb_tables(f):
    print "########################### DYNAMODB TABLE INFO ################################"
    client = boto3.client('dynamodb')

    response = client.list_tables()
    print_dict( response)
    print_list(response['TableNames'])
    print type( response['TableNames'])

    keywordlist = ["CreationDateTime" ]
    for i in range(len( response['TableNames'] )):
        table_name = response['TableNames'][i]
        print "------- begin dynamodb table: " + table_name + " --------------"
        table_info = client.describe_table( TableName=table_name )
        # print_dict( table_info['Table'], "table_name" )
        for k,v in  table_info['Table'].items():
            print table_name, "--->", k, " = ", v
            # print_dict( table_info, table_name )
            if k in keywordlist:
                age_in_seconds = time_diff_seconds(table_info['Table']['CreationDateTime'],
                                  datetime.datetime.utcnow())
                print "age is", age_in_seconds / (60 * 60 * 24), "days"
                print "age is", age_in_seconds / (60 * 60), "hours"

                age_in_fractional_days = (age_in_seconds / (60.0 * 60.0)) / 24
                print "age_in_fractional_days =",age_in_fractional_days

            if k == "ProvisionedThroughput":
                print_dict( v, table_name+" --> " +  k )

            if k == "AttributeDefinitions":
                print_list( v, table_name+" --> " +  k )

            if k == "KeySchema":
                print_list( v, table_name+" --> " +  k )

        print "------- end dynamodb table: " + table_name + " --------------"
        print ""

    print "########################### END DYNAMODB TABLE INFO ################################"
    print ""



def describe_events(f, duration):
    client = boto3.client('rds')

    response = client.describe_events(
        SourceType='db-instance',
        Duration=duration,
        EventCategories=[
            'creation',
        ],
    )

    # print response

    # print_dict( response, "response" )
    # print_dict( response['ResponseMetadata'], "response --> ResponseMetadata" )
    # print_list( response['Events'], "Events" )
    for i in range( len( response['Events'])):
        # print_dict( response['Events'][i])
        d = response['Events'][i]
        describe_dbinstance(f, client, d['SourceIdentifier'])


def print_dict( d,tag="" ):
    print "----------- begin dict", tag, "----------- "
    for k, v in d.items():
        print tag, "--->",   k, "=", v
    print "----------- end dict", tag, "----------- "

def print_list( mylist,tag="" ):
    print "----------- begin list", tag, "----------- "
    for i in range(len(mylist)):
        print tag, "[", i, "]","--->",   mylist[i]
    print "----------- end list", tag, "----------- "



def time_diff_seconds( datetime1, datetime2 ):
    timestamp_1 =  calendar.timegm(datetime1.utctimetuple())
    timestamp_2 =  calendar.timegm(datetime2.utctimetuple())
    diff_seconds = timestamp_2 - timestamp_1
    return diff_seconds

def describe_dbinstance(f, client, dbname):

    # f.write("describe_dbinstance "+ dbname +"\r\n")

    try:
        response = client.describe_db_instances(DBInstanceIdentifier=dbname)
        s = "------------------------- begin describe_dbinstance  " + dbname + "------------------------- "
        print s
        f.write( unicode(s) )
        f.write('\r\n')

        keywordlist = [
                        "InstanceCreateTime",
                        "AllocatedStorage",
                        "DBInstanceClass",
                        "DBInstanceIdentifier"
                      ]

        d = response
        for k, v in d.items():
            # print type(d['DBInstances'])
            dd=(d['DBInstances'])
            # print_list(dd, "DBInstances")
            s = ""
            for i in range(len(dd)):
                #print_dict( dd[i], "DBInstanceInfo " )
                for k2, v2 in dd[i].items():
                    c = " "
                    if k2 in keywordlist:
                        c = "*** "
                    else:
                        c = "    "

                    s =  unicode(c) + unicode(k2) +  " = " + unicode(v2)
                    print s
                    s += "\r\n"
                    f.write(s)

        s = "-------------------------  end describe_dbinstance  " + dbname + "------------------------- "
        print s
        f.write( unicode(s) )
        f.write('\r\n')
        f.write('\r\n')
        print ""
    except Exception as e: # DBInstanceNotFoundFault as e:
        print dbname, "not found\n"
        print e


def main():
    s = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    print(s)

    fname  = "/tmp/datafile"
    f = open(fname, 'w')
    #f = io.open('/tmp/datafile', 'w', newline='\r\n')

    describe_events(f,10820)
    list_dynamodb_tables(f)

    exp_s3_info()
    exp_kinesis_info()

    f.close()

    s3 = boto3.resource('s3')
    output_file =  "database_info_" + s + ".txt"
    bucket_name = 'upefbucket'
    s3.meta.client.upload_file(fname, bucket_name, s )

    print "v3.0"
    print "created bucket " + bucket_name + " " + s


if __name__ == '__main__':
    main()
    try:
        upef_env = os.environ['UPEF_ENV_VAR_1']
        print "UPEF_ENV_VAR_1 =", upef_env
    except KeyError:
        pass

# experimiental=branch-001 change