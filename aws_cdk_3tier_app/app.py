#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

#import stack
from aws_cdk_3tier_app.custom_3tier_vpc_stack import AwsCdk3TierVPCStack
from aws_cdk_3tier_app.aws_cdk_3tier_app_stack import AwsCdk3TierAppStack

app = core.App()
app.synth()

#Set the environment
env_dev= core.Environment(account="673569942958", region="ap-southeast-2")

#Import Stack consist with Custom VPC , App Stack and DB stack
vpc_tier_stack = AwsCdk3TierVPCStack(app, "AwsCdk3VPCAppStack", env=env_dev)
app_tier_stack = AwsCdk3TierAppStack(app, "AwsCdk3TierAppStack", env=env_dev)








