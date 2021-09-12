from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_iam as _iam
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

        #read bootstrap script
        #read my local bootstrap file
        with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_ec2/bootstrap_scripts/install_httpd.sh", 
        mode="r") as file:
            user_data = file.read()

        #Get the latest ami - linux
        amazon_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation = _ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition = _ec2.AmazonLinuxEdition.STANDARD,
            storage = _ec2.AmazonLinuxStorage.EBS,
            virtualization = _ec2.AmazonLinuxVirt.HVM
        )

        #Get the latest ami - Windows
        windows_ami = _ec2.MachineImage.latest_windows(
            version = _ec2.WindowsVersion.WINDOWS_SERVER_1709_ENGLISH_CORE_BASE
        )

        #Launch ec2 instance
        hui_ec2 = _ec2.Instance(
            self,
            "huiec2id",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="HuiInstanceBuiltFromCDK",
            
            #Do not hard code the AMI ID
            #machine_image=_ec2.MachineImage.generic_linux(
            #    {"ap-southeast-2": "ami-09b446f12369c169d"}
            #),

            #Best Practice not to hard code AMI
            machine_image = amazon_linux_ami,

            #Select the VPC to use
            vpc = vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC
            ),            

            #run bootstrap scripts
            user_data = _ec2.UserData.custom(user_data)
        )

        #Add EBS Volume with provisioned IOPS storage
        hui_ec2.instance.add_property_override( 
            "BlockDeviceMappings", [
                {
                    "DeviceName": "/dev/sdb",
                    "EBS": {
                        "VolumeSize": "20",
                        "VolumeType": "io1",
                        "Iops": "400",
                        "DeleteOnTermination": "true"
                    }
                }
            ]
        )
        

        #instance output public ip address
        output1 = core.CfnOutput(
            self,
            "huiinstance1",
            description="Hui Web Server Public Ip Address",
            value=f"http://{hui_ec2.instance_public_ip}"
        )

        #security group
        #allow web traffic inbound
        hui_ec2.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Allow Web Traffic"
        )

        #ec2 iam role instance profile
        hui_ec2.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )

        #ec2 iam s3bucket access role
        hui_ec2.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3FullAccess"
            )
        )
    
