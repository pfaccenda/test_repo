import json
import logging
import boto3


def lambda_handler(event, context):
    print "----- begin ----------\n"
    version_tag = "upef lambda function v13"
    print  version_tag

    print event

    eventsource = event['Records'][0]['EventSource']
    print "event source: ", eventsource, type(eventsource)
    print "-----------"

    message = event['Records'][0]['Sns']['Message']
    print "message", "=", message
    print "message type is", type(message)

    try:
        d = json.loads(message)

        for k, v in d.items():
            print "message -->  K,V -->  ", k, "=", v

        triggerinfo = d.get('Trigger')
        print "trigger", "=", triggerinfo
        for k2, v2 in triggerinfo.items():
            print "     ---->  triggerinfo -->  K,V -->  ", k2, "=", v2

        dbinstance = triggerinfo['Dimensions'][0]['value']
        print " dbinstance is  ", dbinstance

        snsinfo = event['Records'][0]['Sns']
        for k2, v2 in snsinfo.items():
            print " SNS Info K,V -->  ", k2, "=", v2

        print "### ALARM DATA:", snsinfo['Subject'], "from", snsinfo['TopicArn'], "###"
    except TypeError:
        for k, v in event['Records'][0].items():
            print "xxxxxxxxxxxxxxxxxxx event -->", k, "=", v

        d = message
        for k2, v2 in d.items():
            print "xxxxxxxxxxxxxxxxxxx message -->  K,V -->  ", k2, "=", v2
            if k2 == "Event ID":
                t = v2.split("#")
                print "##### EVENT-ID IS ", t[1]

    print "THIS SHOULD BE SENT TO THE CLOUDOPS SNS TOPIC"

    print  version_tag
    print "------ end ----------\n"

    # logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    # logger.info('got event{}'.format(event))
    # logger.info(message)

    return version_tag


def my_logging_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.error('something went wrong')
    return 'Hello from Lambda!'


def modify_dbinstance_monitoring_interval(dbname):
    client = boto3.client('rds')

    response = client.describe_db_instances(DBInstanceIdentifier=dbname)
    d = response['DBInstances'][0]
    print "Original value of MonitoringInterval for", dbname, "is", d.get('MonitoringInterval')

    response = client.modify_db_instance(DBInstanceIdentifier=dbname,
                                         MonitoringInterval=30)

    response = client.describe_db_instances(DBInstanceIdentifier=dbname)

    print "------------------------- ", "modify_dbinstance_monitoring_interval", dbname, "------------------------- "
    d = response['DBInstances']
    for index in range(len(response['DBInstances'])):
        d = response['DBInstances'][index]
        print "MonitoringInterval for ", dbname, "changed to", d.get('MonitoringInterval')
    print "------------------------- ", "modify_dbinstance_monitoring_interval", dbname, "------------------------- "

    print ""


def modify_dbinstance_allocated_storage(dbname):
    client = boto3.client('rds')

    response = client.describe_db_instances(DBInstanceIdentifier=dbname)
    d = response['DBInstances'][0]
    original_allocated_storage = d.get('AllocatedStorage')
    print "Original value of AllocatedStorage for", dbname, "is", original_allocated_storage

    new_allocated_storage = original_allocated_storage + (original_allocated_storage + 0)
    response = client.modify_db_instance(DBInstanceIdentifier=dbname,
                                         AllocatedStorage=new_allocated_storage,
                                         ApplyImmediately=True)

    response = client.describe_db_instances(DBInstanceIdentifier=dbname)

    print "------------------------- ", "modify_dbinstance_allocated_storage", dbname, "------------------------- "
    d = response['DBInstances']
    for index in range(len(response['DBInstances'])):
        d = response['DBInstances'][index]
        print "AllocatedStorage for ", dbname, "changed to", d.get('AllocatedStorage')
    print "------------------------- ", "modify_dbinstance_allocated_storage", dbname, "------------------------- "

    print ""


def describe_dbinstance(dbname):
    client = boto3.client('rds')
    response = client.describe_db_instances(DBInstanceIdentifier=dbname)
    print "------------------------- ", "describe_dbinstance", dbname, "------------------------- "
    d = response
    for k, v in d.items():
        print  k, "=", v
        for dd in d['DBInstances']:
            for k, v in dd.items():
                print k, "=", v

    print "------------------------- ", "describe_dbinstance", dbname, "------------------------- "
    print ""


