#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

#import stack dependent
from aws_cdk_3tier_stack.aws_cdk_vpc_stack import vpc_tier_stack
from aws_cdk_3tier_stack.aws_cdk_3tier_stack_stack import app_tier_stack
from aws_cdk_3tier_stack.aws_cdk_rds_stack import rds_tier_stack

#call the stack function
app = core.App()
vpc_tier = vpc_tier_stack(app, "vpc-tier-stack")
app_tier = app_tier_stack(app, "app-tier-stack", vpc=vpc_tier.vpc)
rds_tier = rds_tier_stack(app, "rds-tier-stack", vpc=vpc_tier.vpc,
rds_security_group = app_tier.web_server_asg.connections.security_groups,
description= "Create Custom RDS Stack")

app.synth()
