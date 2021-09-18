#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core

from aws_cdk_static_website.aws_cdk_static_website_stack import AwsCdkStaticWebsiteStack


app = core.App()
AwsCdkStaticWebsiteStack(app, "AwsCdkStaticWebsiteStack"
    )

app.synth()
