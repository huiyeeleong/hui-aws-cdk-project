#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

#import stack
from aws_cdk_3tier_app.custom_3tier_vpc_stack import AwsCdk3TierVPCStack
from aws_cdk_3tier_app.aws_cdk_3tier_app_stack import AwsCdk3TierAppStack
from aws_cdk_3tier_app.rds_stack import AwsCdk3TierRDSStack

app = core.App()
app.synth()

#Set the environment
env_dev= core.Environment(account="673569942958", region="ap-southeast-2")

#Import Stack consist with Custom VPC , App Stack and DB stack
vpc_tier_stack = AwsCdk3TierVPCStack(app, "AwsCdk3VPCAppStack" )
app_tier_stack = AwsCdk3TierAppStack(app, "AwsCdk3TierAppStack", vpc=vpc_tier_stack.vpc)

db_tier_stack = AwsCdk3TierRDSStack(app, "AwsCdk3TierRDSStack",  
vpc=vpc_tier_stack,
asg_security_groups=app_tier_stack.web_server_asg.connections.security_groups,
description = "Create Custom RDS Database")








