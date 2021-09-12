#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

#from aws_cdk_custom_vpc.aws_cdk_custom_vpc_stack import AwsCdkCustomVpcStack
from aws_cdk_custom_vpc.resource_stacks.custom_vpc import HuiCustomVpcStack

app = core.App()

HuiCustomVpcStack(app, "my-custom-vpc-stack")

#add tag for whole stack
#Reference from cdk.json
core.Tag.add(app, key="Name", value=app.node.try_get_context('envs')['dev']['name'])
#Tag straight away
core.Tag.add(app, key="owner", value="hui")


app.synth()
