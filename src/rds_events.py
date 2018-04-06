#! /usr/bin/env python

import boto3
import os, sys
import json
import datetime


def describe_events(f):
    client = boto3.client('rds')

    response = client.describe_events(
        SourceType='db-instance',
        Duration=700,  #10280
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
        print "------------------------- ", "begin describe_dbinstance", dbname, "------------------------- "

        d = response
        for k, v in d.items():
            # print type(d['DBInstances'])
            dd=(d['DBInstances'])
            # print_list(dd, "DBInstances")
            s = ""
            for i in range(len(dd)):
                #print_dict( dd[i], "DBInstanceInfo " )
                for k2, v2 in dd[i].items():
                    #s = "DBInstanceInfo " + 'k2 + "=" +  v2
                    s =  " ->  " + unicode(k2) +  "=" + unicode(v2)
                    print s
                    s += "\r\n"
                    f.write(s)

        print "------------------------- ", "end describe_dbinstance", dbname, "------------------------- "
        print ""
    except Exception as e: # DBInstanceNotFoundFault as e:
        print dbname, "not found\n"
        print e



def main():
    fname  = "/tmp/datafile"
    f = open(fname, 'w')
    #f = io.open('/tmp/datafile', 'w', newline='\r\n')
    #for i in range( 1, 16):
    #    f.write('hello ss to the world!!\r\n')

    describe_events(f)
    f.close()

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(fname, 'upefbucket', 'rdsdata_199.txt')

    print "v2.5"


if __name__ == '__main__':
    main()
