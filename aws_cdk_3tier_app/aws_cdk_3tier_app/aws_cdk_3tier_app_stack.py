from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_autoscaling as _autoscaling,    
    aws_iam as _iam
)


class AwsCdk3TierAppStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Read Bootstrap script we can read from S3 or local
        with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_3tier_app/aws_cdk_3tier_app/bootstrap_script/install_httpd.sh", 
        mode="r") as file:
            user_data = file.read()
        
        #Get the latest Linux AMI
        amazon_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation = _ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition = _ec2.AmazonLinuxEdition.STANDARD,
            storage = _ec2.AmazonLinuxStorage.EBS,
            virtualization = _ec2.AmazonLinuxVirt.HVM
        )

        #Create application load balancer
        alb = _elbv2.ApplicationLoadBalancer(
            self,
            "myAlbId",
            #vpc = vpc,
            internet_facing=True,
            load_balancer_name="HuiWebServerALB"
        )

