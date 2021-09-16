from logging import Handler
from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_apigateway as _api
)


class AwsCdkApiGatewayStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Read lambda code from my local folder
        try:
            with open ("//Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_api_gateway/aws_cdk_api_gateway/hello_world.py"
            , mode=r"r") as f: hui_fn_code = f.read()

        except OSError:
            print("Unable to read lambda function code")

        #Create lambda function
        hui_fn = _lambda.Function(self,
        "huifunction",
        function_name = "hui_function",
        runtime = _lambda.Runtime.PYTHON_3_7,
        handler = "index.lambda_handler",
        code = _lambda.InlineCode(hui_fn_code),
        timeout = core.Duration.seconds(3),
        reserved_concurrent_executions=1,
        environment={
            "LOG_LEVEL": "INFO",
            "Environment": "DEV"}
        )

        #Create logging
        # /aws/lambda/log-groupPath
        hui_lg = _logs.LogGroup(
            self,
            "huilogGroup",
            log_group_name = f"/aws/lambda/{hui_fn.function_name}",
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = core.RemovalPolicy.DESTROY
        )

        #Add API gateway
        #This will create a default API without actually configure anything
        hui_fn_integration = _api.LambdaRestApi(
            self,
            "huiApiEndpoint",
            handler = hui_fn
        )

        #Output CFN stack
        output_cfn = core.CfnOutput(
            self,
            "apiurl",
            value = f"{hui_fn_integration.url}",
            description = "URL to access"
        )