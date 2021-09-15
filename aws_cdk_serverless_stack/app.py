#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

from aws_cdk_serverless_stack.aws_cdk_serverless_stack_stack import AwsCdkServerlessStackStack


app = core.App()
AwsCdkServerlessStackStack(app, "AwsCdkServerlessStackStack")

app.synth()
