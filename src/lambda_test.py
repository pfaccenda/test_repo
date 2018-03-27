import json
import logging


def lambda_handler(event, context):
    print "--> upefrdslambda:version=12 "
    print "----- begin ----------\n"
    eventsource = event['Records'][0]['EventSource']
    print "event source:", eventsource, type(eventsource)

    message = event['Records'][0]['Sns']['Message']
    print "message", "=", message
    print "message type is ", type(message)
    d = json.loads(message)
    for k, v in d.items():
        print "message -->  K,V -->  ", k, "=", v
        if k == 'Trigger':
            trigger = v
            print "trigger", "=", v
            print "trigger type is ", type(v)
            for k2, v2 in trigger.items():
                print "     ---->  trigger -->  K,V -->  ", k2, "=", v2

            dbinstance = trigger['Dimensions'][0]['value']
            print " dbinstance is  ", dbinstance

    snsinfo = event['Records'][0]['Sns']
    for k, v in snsinfo.items():
        print " SNS Info K,V -->  ", k, "=", v

    print "INFO:", d['AlarmName'], dbinstance, trigger['MetricName'], d['AlarmDescription']
    print "### ALARM DATA:", snsinfo['Subject'], "from", snsinfo['TopicArn'], "###"
    print "THIS SHOULD BE SENT TO THE CLOUDOPS SNS TOPIC"

    print "------ end ----------\n"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('got event{}'.format(event))
    logger.info(message)

    return message


def my_logging_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.error('something went wrong')
    return 'Hello from Lambda!'  