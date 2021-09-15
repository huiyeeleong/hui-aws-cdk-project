from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_logs as _logs
)


class AwsCdkServerlessEventProcessorStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Create serverless event processor using Lambda:

        #Read lambda code #Throw exception error
        try:
            with open ("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_serverless_event_processor/aws_cdk_serverless_event_processor/hui_processor.py"
            , mode=r"r") as f: read_fn_code = f.read()

        except OSError:
            print("Unable to read lambda function code")

        read_fn = _lambda.Function(self,
        "huifunction",
        function_name = "Hui_Function",
        runtime = _lambda.Runtime.PYTHON_3_7,
        handler = "index.lambda_handler",
        code = _lambda.InlineCode(read_fn_code),
        timeout = core.Duration.seconds(3),
        reserved_concurrent_executions=1,
        environment={"Log_LEVEL": "INFO"}
        )

        #Create custom log group
        #/aws/lambda/functionname
        hui_log_group = _logs.LogGroup(
            self,
            "huiogGroup",
            log_group_name= f"/aws/lambda/{read_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY
        )
        