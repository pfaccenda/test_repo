#! /usr/bin/env python

import boto3
import os, sys
import json
import datetime
import time
import datetime

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
    print ""

def print_list( mylist,tag="" ):
    print "----------- begin list", tag, "----------- "
    for i in range(len(mylist)):
        print tag, "[", i, "]","--->",   mylist[i]
    print "----------- end list", tag, "----------- "
    print ""





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



def main():
    s = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    print(s)

    fname  = "/tmp/datafile"
    f = open(fname, 'w')
    #f = io.open('/tmp/datafile', 'w', newline='\r\n')

    describe_events(f,10820)
    f.close()

    s3 = boto3.resource('s3')
    output_file =  "database_info_" + s + ".txt"
    bucket_name = 'upefbucket'
    s3.meta.client.upload_file(fname, bucket_name, s )

    print "v2.5"
    print "created bucket " + bucket_name + " " + s

if __name__ == '__main__':
    main()
