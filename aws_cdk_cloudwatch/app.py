#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

#import stack
from aws_cdk_cloudwatch.aws_cdk_cloudwatch_stack import AwsCdkCloudwatchStack
from aws_cdk_cloudwatch.aws_custom_cloudwatch_metrics import AwsCloudwatchCustomMetrics
from aws_cdk_cloudwatch.aws_cdk_cloudwatch_dashboard import AwsCloudwatchLiveDashboard

app = core.App()

#stack build
AwsCdkCloudwatchStack(app, "AwsCdkCloudwatchStack")
AwsCloudwatchCustomMetrics(app, "AwsCloudwatchCustomMetrics")
AwsCloudwatchLiveDashboard(app, "AwsCloudwatchLiveDashboard")

#Tag my application
core.Tag.add(app, key="owner", value="hui")
app.synth()
