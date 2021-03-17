import json
import boto3


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    client = boto3.client('glue')
    response = client.start_job_run(JobName='glue-test-job')
    status = client.get_job_run(JobName='glue-test-job', RunId=response['JobRunId'])
    print(status['JobRun']['JobRunState'])
    return response