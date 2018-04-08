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

def list_dynamodb_tables(f):
    print "list_dynamodb_tables"
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
                # print ( "****", table_info['Table']['CreationDateTime'])
                d1 =  table_info['Table']['CreationDateTime']
                # print type(d1)
                d2 = datetime.datetime.utcnow()
                naive = d1.replace(tzinfo=None)
                # print type(d2)
                age = d2 - naive
                if age.days == 0:
                    print "NEW TABLE: AGE (days): ", age.days
                else:
                    print "AGE (days): ", age.days

                dt_now= datetime.datetime.utcnow()

                print "dt_now", calendar.timegm(dt_now.utctimetuple())
                dt1 = table_info['Table']['CreationDateTime']
                print "dt1", calendar.timegm(dt1.utctimetuple())
                timestamp_table =  calendar.timegm(dt1.utctimetuple())
                timestamp_now =  calendar.timegm(dt_now.utctimetuple())
                print "timestamp_now", timestamp_now
                print "timestamp_table", timestamp_table

                age_seconds = timestamp_now -timestamp_table
                print "age is", age_seconds /(60*60*24), "days"
                print "age is", age_seconds /(60*60), "hours"

                f =  (age_seconds /(60.0*60.0))/24
                print f
                print dt1.utctimetuple()
                print dt_now.utctimetuple()
                print type(dt1.utctimetuple())
                print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

            #print type(v)
            if k == "ProvisionedThroughput":
                print_dict( v, table_name+" --> " +  k )

            if k == "AttributeDefinitions":
                print_list( v, table_name+" --> " +  k )

            if k == "KeySchema":
                print_list( v, table_name+" --> " +  k )

        print "------- end dynamodb table: " + table_name + " --------------"
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





def describe_dbinstance(f, client, dbname):

    # f.write("describe_dbinstance "+ dbname +"\r\n")

    try:
        response = client.describe_db_instances(DBInstanceIdentifier=dbname)
        s = "------------------------- begin describe_dbinstance  " + dbname + "------------------------- "
        print s
        f.write( unicode(s) )
        f.write('\r\n')

        keywordlist = [ "InstanceCreateTime", "AllocatedStorage", "DBInstanceClass", "DBInstanceIdentifier" ]

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


def time_test():
    print "xx"
    s = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M:%z")
    print "S", s
    ts = time.time()
    print "TS time.time", ts

    s = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M:%z")
    x =datetime.datetime.utcoffset( datetime.datetime.now()  )
    print "x", x

    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print "ST:", st
    # 2018-04-07 23:54:22.523000-04:00

    #d2 = datetime.datetime.utcnow()
    #naive = d1.replace(tzinfo=None)
    # print type(d2)
    datetime.datetime.utcfromtimestamp(ts)
    print ts

    utc_date = datetime.datetime.utcnow().date()
    ts = (utc_date - datetime.date(1970, 1, 1)).days * 8640
    print utc_date
    print ts

    dt = datetime.datetime.utcnow()

    import calendar

    # Converts a datetime object to UTC timestamp
    #     naive datetime will be considered UTC.
    print "XXX", calendar.timegm(dt.utctimetuple())

def main():
    s = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    print(s)

    fname  = "/tmp/datafile"
    f = open(fname, 'w')
    #f = io.open('/tmp/datafile', 'w', newline='\r\n')

    describe_events(f,10820)

    list_dynamodb_tables(f)
    f.close()

    s3 = boto3.resource('s3')
    output_file =  "database_info_" + s + ".txt"
    bucket_name = 'upefbucket'
    s3.meta.client.upload_file(fname, bucket_name, s )

    print "v2.6"
    print "created bucket " + bucket_name + " " + s


if __name__ == '__main__':
    #time_test()
    main()
