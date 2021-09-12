from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_s3 as _s3,
    aws_ec2 as _ec2
)


class ImportExistingResourcesVpcS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Custom VPC
        dev_configs = self.node.try_get_context("envs")["dev"]
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

        #Import existing bucket
        bucket1 = _s3.Bucket.from_bucket_name(
            self,
            "MyImportbucket1",
            "hui-demo-bucket-haha"
        )
        #S3 bucket output
        core.CfnOutput(
            self,
            "MyImportbucket",
            value=bucket1.bucket_name
        )

        vpc1= _ec2.Vpc.from_lookup(
            self,
            "importedVPC",
            #is_default=True
            vpc_id="vpc-d21e0fb0"
        )

        #VPC bucket output
        core.CfnOutput(
            self,
            "MyImportVPC",
            value=vpc1.vpc_id
        )

        #vpc peering
        peer_vpc = _ec2.CfnVPCPeeringConnection(
            "peerVPC12",
            peer_vpc_id= custom_vpc.vpc_id,
            vpc_id=vpc1.vpc_id
        )