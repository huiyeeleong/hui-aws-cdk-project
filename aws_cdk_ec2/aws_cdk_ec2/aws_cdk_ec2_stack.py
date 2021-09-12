from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_ec2 as _ec2
)


class AwsCdkEc2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Define the VPC
        vpc = _ec2.Vpc.from_lookup(
            self,
            "ImportedVPC",
            vpc_id="vpc-d21e0fb0"
        )

        #Launch ec2 instance
        hui_ec2 = _ec2.Instance(
            self,
            "huiec2id",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="HuiInstanceBuiltFromCDK",
            machine_image=_ec2.MachineImage.generic_linux(
                {"ap-southeast-2": "ami-09b446f12369c169d"}
            ),
            #Select the VPC to use
            vpc = vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC
            )        
        )
