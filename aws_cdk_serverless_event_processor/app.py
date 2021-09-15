#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

from aws_cdk_serverless_event_processor.aws_cdk_serverless_event_processor_stack import AwsCdkServerlessEventProcessorStack
from aws_cdk_serverless_event_processor.read_lambda_src_from_s3 import ReadLambdaSrcFromS3Stack

app = core.App()
AwsCdkServerlessEventProcessorStack(app, "AwsCdkServerlessEventProcessorStack")
ReadLambdaSrcFromS3Stack(app,"ReadLambdaSrcFromS3Stack")

app.synth()
