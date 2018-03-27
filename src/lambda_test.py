import json
import logging


def lambda_handler(event, context):
    print "upefrdslambda 007"
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

    for k, v in event['Records'][0]['Sns'].items():
        print " K,V -->  ", k, "=", v

    print "------ end ----------\n"

    # print "------ test ----------\n"
    # d = event['Records'][0]['Sns']
    # str="\n".join("{}: {}".format(k, v) for k, v in d.items())
    # print str
    # print "------ test ----------\n"

    # message = event['Records'][0]['Sns']['Message']
    # for k,v in message.items():
    #    print "MESSAGE -->",k, ":", v
    # Message:
    # {
    # "Event Source": "db-instance",
    # "Event Time": "2018-03-26 04:26:27.180",
    # "Source ID": "upefrdsdb01",
    # "Event ID": "http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/USER_Events.html#RDS-EVENT-0078",
    # "Event Message": "Monitoring Interval changed to 60"
    # }

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('got event{}'.format(event))
    logger.info(message)

    return message


def my_logging_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.error('something went wrong')
    return 'Hello from Lambda!'  