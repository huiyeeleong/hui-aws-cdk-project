from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    aws_iam as _iam
)


class AwsCdkServerlessStackStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #create dynamodb
        hui_table = _dynamodb.Table(
            self,
            "huiDynamoDB",
            partition_key = _dynamodb.Attribute(
                name = "id",
                type = _dynamodb.AttributeType.STRING
            ),
            #only for testing us this will delet the table if it not use
            removal_policy= core.RemovalPolicy.DESTROY,
            #server_side_encryption = True
        )

        #Read Lambda Python Code
        #Throw Exception
        try:
            with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_serverless_stack/aws_cdk_serverless_stack/s3_generator.py", mode="r") as f:
                hui_fn_code = f.read()
        except OSError:
            print("Unable to read lambda code")

        #Create lambda function
        hui_fn = _lambda.Function(self,
        "huifunction",
        function_name = "Hui_Function",
        runtime = _lambda.Runtime.PYTHON_3_7,
        handler = "index.lambda_handler",
        code = _lambda.InlineCode(hui_fn_code),
        timeout = core.Duration.seconds(3),
        reserved_concurrent_executions=1,
        environment={
            "LOG_LEVEL": "INFO",
            "DDB_TABLE_NAME": f"{hui_table.table_name}"
            }
        )

        #Add S3 ReadOnly Managed Policy to Lambda
        hui_fn.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
        )

        # Add DynamoDB Write Priveleges to Lambda
        hui_table.grant_write_data(hui_fn)