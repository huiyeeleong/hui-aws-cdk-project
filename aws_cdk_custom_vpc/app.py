#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

#from aws_cdk_custom_vpc.aws_cdk_custom_vpc_stack import AwsCdkCustomVpcStack
from aws_cdk_custom_vpc.resource_stacks.custom_vpc import HuiCustomVpcStack

app = core.App()

HuiCustomVpcStack(app, "my-custom-vpc-stack")

app.synth()
