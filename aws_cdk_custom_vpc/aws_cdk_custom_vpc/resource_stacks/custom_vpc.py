from aws_cdk import core as cdk
from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_s3 as _s3
)


class HuiCustomVpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        dev_configs = self.node.try_get_context("envs")["dev"]
    

        #Custom VPC
        custom_vpc = _ec2.Vpc(
            self,
            "huicustomVPC",
            cidr=dev_configs['vpc_configs']['vpc_cidr'],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet", cidr_mask=dev_configs['vpc_configs']['cidr_mask'],
                    subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet", cidr_mask=dev_configs['vpc_configs']['cidr_mask'],
                    subnet_type=_ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name="dbSubnet", cidr_mask=dev_configs['vpc_configs']['cidr_mask'],
                    subnet_type=_ec2.SubnetType.ISOLATED
                )
            ]
        )

        #Tag the VPC resources
        core.Tag.add(custom_vpc, "Billing", "HuiApplication")

        huibucket = _s3.Bucket(
            self,
            "HuiBucketId"
        )

        core.Tag.add(huibucket, "Billing", "HuiBucket")

