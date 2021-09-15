from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_events as _events,
    aws_events_targets as _events_targets
)


class AWSCdkLambdaCronStack(cdk.Stack):

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

        #Run everyday at 18:00 UTC
        six_pm_cron = _events.Rule(
            self,
            "sixPmDaily",
            schedule = _events.Schedule.cron(
                minute = "0",
                hour = "18",
                month = "*",
                week_day = "MON-FRI",
                year = "*"
            )
        )
        #Cron run every 3 mins
        minute_three_cron = _events.Rule(
            self,
            "runEvery3Minutes",
            schedule = _events.Schedule.rate(core.Duration.minutes(3))
        )

        #Cloudwatch trigger rule
        six_pm_cron.add_target(_events_targets.LambdaFunction(read_fn))
        minute_three_cron.add_target(_events_targets.LambdaFunction(read_fn))
        
        