# greengrassHelloWorldCounter.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send a hello world message along with the
# platform information to the topic 'hello/world/counter' along with a counter to keep track of invocations.
#
# This Lambda function requires the AWS Greengrass SDK to run on Greengrass devices.
# This can be found on the AWS IoT Console.

import json
import logging
import platform
import sys
import time
import boto3
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")
s3 = boto3.client('s3')

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()

# Counter to keep track of invocations of the function_handler
my_counter = 0


def function_handler(event, context):
    # global my_counter
    timeOfFlight = event['tof']
    Bolt_Distance = timeOfFlight * 3250 / 2  # m
    Bolt_Distance = round(Bolt_Distance, 4)
    bucket = 'bucket-promet-example'
    filename ='example1'

    data = {'distance': (Bolt_Distance)}


    try:
        if not my_platform:
            client.publish(
                topic="promet/getMeasurement",
                queueFullPolicy="AllOrException",
                payload=json.dumps(
                    {"Measurement": "{}".format(Bolt_Distance)}
                ),
            )
            s3.put_object(Bucket=bucket,
                          Key=filename,
                          Body=json.dumps(data).encode('UTF-8')
                          )

        else:
            client.publish(
                topic="promet/getMeasurement",
                queueFullPolicy="AllOrException",
                payload=json.dumps(
                    {
                        "Measurement": "{}".format(Bolt_Distance)
                    }
                ),
            )

            s3.put_object(Bucket=bucket,
                          Key=filename,
                          Body=json.dumps(data).encode('UTF-8')
                          )

    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))
    time.sleep(20)
    return
