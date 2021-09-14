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

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc, **kwargs) -> None:
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
            vpc = vpc,
            internet_facing=True,
            load_balancer_name="HuiWebServerALB"
        )

        #Create Security Group inbound rule for ALB
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description="Allow Internet access on ALB port 80"
        )

        #Add listener to ALB
        listener = alb.add_listener(
            "listenerId",
            port=80,
            open=True
        )

        #Web server instance IAM role
        hui_web_server_role = _iam.Role(
            self,
            "HuiWebServerRoleId",
            assumed_by = _iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            ),
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3FullAccess"
                )
            ]
        )

        #Create ASG for 2 Instances
        self.web_server_asg = _autoscaling.AutoScalingGroup(
            self,
            "HuiWebServerASGId",
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PRIVATE
            ),
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t2.micro"),
                machine_image = amazon_linux_ami ,
                role=hui_web_server_role,
                min_capacity=2,
                max_capacity=2,
                #desired_capacity=2,
                user_data = _ec2.UserData.custom(
                    user_data
                )
            )

        #Add ASG instance to ALB target group
        self.web_server_asg.connections.allow_from(
            alb, _ec2.Port.tcp(80),
            description="Allows ASG Security Group receive traffic from ALB"
        )

        #Add ASG Group Instances to ALB Target Group
        listener.add_targets(
            "listenerId",
            port=80,
            targets=[self.web_server_asg]
        )

        #Out CFN Stack the ALB domain name
        output_alb1 = core.CfnOutput(
            self,
            "albDomainName",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Hui Web Server ALB Domain Name"
        )


