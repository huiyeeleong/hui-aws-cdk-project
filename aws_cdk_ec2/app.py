#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk_ec2.aws_cdk_ec2_stack import AwsCdkEc2Stack

#Set the environment
env_dev= core.Environment(account="673569942958", region="ap-southeast-2")

app = core.App()
AwsCdkEc2Stack(app, "AwsCdkEc2Stack", env=env_dev)

app.synth()
