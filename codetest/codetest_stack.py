from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_notifications,
    core,
    aws_glue as glue,
    aws_iam as iam,
    aws_s3_deployment
)


class CodetestStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        policy_statement = iam.PolicyStatement(
            actions=['logs:*', 's3:*', 'iam:*', 'cloudwatch:*', 'glue:*']
        )

        policy_statement.add_all_resources()

        my_lambda = _lambda.Function(
            self, 'lambdaHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='handler.handler',
        )
        my_lambda_role = iam.Role(
            self,
            'my_lambda_role',
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com')
        )
        my_lambda_role.add_to_policy(
            policy_statement
        )

        my_bucket = _s3.Bucket(
            self,
            id='s3buckettest',
            bucket_name='csvconverterbv',
        )

        notification = aws_s3_notifications.LambdaDestination(my_lambda)

        my_bucket.add_event_notification(_s3.EventType.OBJECT_CREATED, notification)

        glue_job_role = iam.Role(
            self,
            'Glue-Job-Role',
            assumed_by=iam.ServicePrincipal('glue.amazonaws.com')
        )
        glue_job_role.add_to_policy(
            policy_statement
        )

        code_bucket = _s3.Bucket.from_bucket_attributes(
            self, 'CodeBucket',
            bucket_name='csvconverterbv'
        )

        aws_s3_deployment.BucketDeployment(
            self,
            'S3Deployment',
            destination_bucket=code_bucket,
            sources=[aws_s3_deployment.Source.asset('glue/')],
            destination_key_prefix='glue/'
        )


        job = glue.CfnJob(
            self,
            'glue-test-job',
            name='glue-test-job',
            role=glue_job_role.role_arn,
            allocated_capacity=10,
            command=glue.CfnJob.JobCommandProperty(
                name='glueetl',
                script_location='s3://csvconverterbv/glue/gluejob.py'
            ))

