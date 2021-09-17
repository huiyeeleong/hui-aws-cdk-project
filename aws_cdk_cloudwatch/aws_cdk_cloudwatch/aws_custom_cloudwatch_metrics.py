from aws_cdk import core as cdk
from aws_cdk import (
    core,
    aws_cloudwatch as _cloudwatch,
    aws_lambda as _lambda,
    aws_logs as _logs

)


class AwsCloudwatchCustomMetrics(core.Stack):

    def __init__(self, scope: core.Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Read my local lambda code
        try:
            with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_cloudwatch/aws_cdk_cloudwatch/hui_example_lambda.py", mode="r") as f:
                hui_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        # create lambda function
        hui_fn = _lambda.Function(self,
                                  "huiFunction",
                                  function_name="hui_function",
                                  runtime=_lambda.Runtime.PYTHON_3_7,
                                  handler="index.lambda_handler",
                                  code=_lambda.InlineCode(
                                      hui_fn_code),
                                  timeout=core.Duration.seconds(
                                      3),
                                  reserved_concurrent_executions=1,
                                  environment={
                                      "LOG_LEVEL": "INFO",
                                      "PERCENTAGE_ERRORS": "75"
                                  }
                                  )

        # create custom log group
        # /aws/lambda/function-name
        hui_custome_metric_lg = _logs.LogGroup(self,
                                                   "konstoneLoggroup",
                                                   log_group_name=f"/aws/lambda/{hui_fn.function_name}",
                                                   removal_policy=core.RemovalPolicy.DESTROY,
                                                   retention=_logs.RetentionDays.ONE_DAY,
                                                   )

        # Create Custom Metric Namespace 
        hui_error_metric = _cloudwatch.Metric(
            namespace=f"third-party-error-metric",
            metric_name="third_party_error_metric",
            label="Total No. of Third Party API Errors",
            #period=core.Duration.minutes(1),
            statistic="Sum"
        )

        # Create Custom Metric Log Filter
        hui_error_metric_filter = _logs.MetricFilter(self,
                                                             "thirdPartyApiErrorMetricFilter",
                                                             filter_pattern=_logs.FilterPattern.boolean_value(
                                                                 "$.third_party_api_error", True),
                                                             log_group=hui_custome_metric_lg,
                                                             metric_namespace=hui_error_metric.namespace,
                                                             metric_name=hui_error_metric.metric_name,
                                                             default_value=0,
                                                             metric_value="1"
                                                             )

        # Create Cloudwatch Error Alarm
        third_party_error_alarm = _cloudwatch.Alarm(
            self,
            "thirdPartyApiErrorAlarm",
            alarm_description="Alert if 3rd party API has more than 2 errors in the last two minutes",
            alarm_name="third-party-api-alarm",
            metric=hui_error_metric,
            comparison_operator=_cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            threshold=2,
            evaluation_periods=2,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(1),
            treat_missing_data=_cloudwatch.TreatMissingData.NOT_BREACHING
        )
