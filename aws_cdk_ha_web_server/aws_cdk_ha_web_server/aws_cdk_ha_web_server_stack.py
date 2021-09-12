from aws_cdk import core as cdk

from aws_cdk import (
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_autoscaling as _autoscaling,
    core   
)


class AwsCdkHaWebServerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Read bootstrap script
        with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_ha_web_server/aws_cdk_ha_web_server/bootstrap_scripts/install_httpd.sh"
        , mode="r") as file: 
            user_data = file.read()

        #Get the latest ami - linux
        linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation = _ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition = _ec2.AmazonLinuxEdition.STANDARD,
            storage = _ec2.AmazonLinuxStorage.EBS,
            virtualization = _ec2.AmazonLinuxVirt.HVM
        )

        #Define VPC 
        vpc = _ec2.Vpc.from_lookup(
            self,
            "ImportedVPC",
            vpc_id="vpc-d21e0fb0"
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

        #Add Listener for ALB
        listener = alb.add_listener(
            "ListenerID",
            port=80,
            open=True
        )

        # Hui Webserver IAM EC2 role
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

        #Create ASG for 2 ec2 instance
        hui_web_server_asg = _autoscaling.AutoScalingGroup(
            self,
            "HuiWebServerASGId",
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PRIVATE
            ),
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t2.micro"),
                machine_image = linux_ami,
                role=hui_web_server_role,
                min_capacity=2,
                max_capacity=2,
                #desired_capacity=2,
                user_data = _ec2.UserData.custom(
                    user_data
                )
            )
        
        
        #Alow ASG security group receive traffic from ALB
        hui_web_server_asg.connections.allow_from(
            alb, _ec2.Port.tcp(80),
            description="Allows ASG Security Group receive traffic from ALB"
        )
        #Add ASG Group Instances to ALB Target Group
        listener.add_targets(
            "listenerId",
            port=80,
            targets=[hui_web_server_asg]
        )

        #Out CFN Stack the ALB domain name
        output_alb1 = core.CfnOutput(
            self,
            "albDomainName",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Hui Web Server ALB Domain Name"
        )



