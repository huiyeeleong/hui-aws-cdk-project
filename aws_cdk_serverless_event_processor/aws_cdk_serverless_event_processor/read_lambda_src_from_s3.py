from typing_extensions import runtime
from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3
)


class ReadLambdaSrcFromS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Import S3 buckets
        hui_bucket = _s3.Bucket.from_bucket_attributes(
            self,
            "HuiBucket",
            bucket_name = "hui-demo-bucket-haha"
        )

        #Create lambda function with source code from s3 bucket
        hui_fn = _lambda.Function(self,
        "huifunction",
        function_name = "Hui_Function",
        runtime = _lambda.Runtime.PYTHON_3_7,
        handler = "index.lambda_handler",
        code = _lambda.S3Code(
            bucket = hui_bucket,
            key = "lambdaSource/hui_processor.py.zip"  
        ),
        timeout = core.Duration.seconds(3),
        reserved_concurrent_executions=1,
        environment={"Log_LEVEL": "INFO"}
        )

        #Create custom loggroup
        # /aws/lambda/function-name
        hui_log_group = _logs.LogGroup(
            self,
            "huiLog",
            log_group_name = f"/aws/lambda/{hui_fn.function_name}",
            removal_policy = core.RemovalPolicy.DESTROY,
            retention = _logs.RetentionDays.ONE_DAY
        )