from aws_cdk import core as cdk
from aws_cdk import (
    core,
    aws_ec2 as _ec2
)


class vpc_tier_stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Create VPC for 3 tier app
        self.vpc = _ec2.Vpc(
            self,
            "customID",
            cidr="10.10.0.0/16",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet", cidr_mask=24,
                    subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet", cidr_mask=24,
                    subnet_type=_ec2.SubnetType.PRIVATE
                ),
                _ec2.SubnetConfiguration(
                    name="dbSubnet", cidr_mask=24,
                    subnet_type=_ec2.SubnetType.ISOLATED
                )
            ]
        )

        #Cloudformation stack output
        core.CfnOutput(
            self,
            "customVPCoutput",
            value=self.vpc.vpc_id,
            export_name="VpcId"
        )
        