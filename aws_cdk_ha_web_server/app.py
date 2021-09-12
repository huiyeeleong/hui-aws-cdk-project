#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

from aws_cdk_ha_web_server.aws_cdk_ha_web_server_stack import AwsCdkHaWebServerStack


app = core.App()

#import environment
env_dev= core.Environment(account="673569942958", region="ap-southeast-2")
AwsCdkHaWebServerStack(app, "AwsCdkHaWebServerStack", env=env_dev)


#Tag straight away
core.Tag.add(app, key="Billing", value= "HuiApplication")
app.synth()
