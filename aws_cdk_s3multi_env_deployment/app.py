#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from aws_cdk_project_resources.aws_cdk_project_resources_stack import AwsCdkProjectResourcesStack

app = core.App()

#Get context
#env_aus = core.Environment(account=app.node.try_get_context('dev')['account'], 
#region=app.node.try_get_context('dev')['region'])

#labs
env_nonprod = core.Environment(account="673569942958", region="ap-southeast-2")

#mft-nonprod
env_prod = core.Environment(account="447302848060", region="ap-southeast-2")


AwsCdkProjectResourcesStack(app, "AwsCdkProjectResourcesStack", env=env_nonprod)
AwsCdkProjectResourcesStack(app, "AwsCdkProdProjectResourcesStack", is_prod=True, env=env_prod)

app.synth()


