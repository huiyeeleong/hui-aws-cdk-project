from aws_cdk import core as cdk
from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_autoscaling as _autoscaling,
    aws_sns as _sns,
    aws_sns_subscriptions as _subs,
    aws_cloudwatch as _cloudwatch,
    aws_cloudwatch_actions as _cloudwatch_actions
)


class AwsCdkCloudwatchStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Create SNS Topic for Operations Team):
        hui_ops_team = _sns.Topic(self,
                                "huiOpsTeam",
                                display_name="Hui Support Team",
                                topic_name="huiOpsTeam"
                                )

        # Add Subscription to SNS Topic
        hui_ops_team.add_subscription(
            _subs.EmailSubscription("dummy@email.com")
        )

        # Create custom VPC:
        vpc = _ec2.Vpc(
            self,
            "HuiVpcId",
            cidr="10.0.0.0/24",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="public", subnet_type=_ec2.SubnetType.PUBLIC
                )
            ]
        )

        #Define the VPC or we can reuse exsiting vpc
        #vpc = _ec2.Vpc.from_lookup(
        #    self,
        #    "ImportedVPC",
        #    vpc_id="vpc-d21e0fb0"
        #)

        # Read EC2 BootStrap Script from my local
        try:
            with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_cloudwatch/aws_cdk_cloudwatch/bootstrap_script/install_httpd.sh", 
            mode="r") as file: user_data = file.read()
        except OSError:
            print('Unable to read bootstrap script')

        # Get the latest ami
        amzn_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # Create webserver instance
        web_server = _ec2.Instance(self,
                                   "huiWebServer",
                                   instance_type=_ec2.InstanceType(
                                       instance_type_identifier="t2.micro"),
                                   instance_name="huiWebServer",
                                   machine_image=amzn_linux_ami,
                                   vpc=vpc,
                                   vpc_subnets=_ec2.SubnetSelection(
                                       subnet_type=_ec2.SubnetType.PUBLIC
                                   ),
                                   user_data=_ec2.UserData.custom(user_data)
                                   )

        # Allow ec2 inbound rule
        web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Allow Web Traffic"
        )

        # Add iam role to server (SSM role)
        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
        )

        # Read Lambda Code from my local pc
        try:
            with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_cloudwatch/aws_cdk_cloudwatch/hui_example_lambda.py", mode="r") as f:
                hui_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        # Simple Lambda Function to return event
        huifn = _lambda.Function(self,
                                       "huiFunction",
                                       function_name="hui_function",
                                       runtime=_lambda.Runtime.PYTHON_3_7,
                                       handler="index.lambda_handler",
                                       code=_lambda.InlineCode(
                                           hui_fn_code),
                                       timeout=core.Duration.seconds(3),
                                       reserved_concurrent_executions=1,
                                       environment={
                                           "LOG_LEVEL": "INFO",
                                           "AUTOMATION": "SKON"
                                       }
                                       )

        # create cloudwatch metric for webserver
        ec2_metric_for_avg_cpu = _cloudwatch.Metric(
            namespace="AWS/EC2",
            metric_name="CPUUtilization",
            dimensions={
                "InstanceId": web_server.instance_id
            },
            period=core.Duration.minutes(5)
        )

        # Low CPU Alarm for Web Server
        low_cpu_alarm = _cloudwatch.Alarm(
            self,
            "lowCPUAlarm",
            alarm_description="Alert if CPU is less than 10%",
            alarm_name="low-cpu-alarm",
            actions_enabled=True,
            metric=ec2_metric_for_avg_cpu,
            threshold=10,
            comparison_operator=_cloudwatch.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(5),
            treat_missing_data=_cloudwatch.TreatMissingData.NOT_BREACHING
        )

        # Trigger sns topic when EC2 Alarm State has trigger
        low_cpu_alarm.add_alarm_action(
            _cloudwatch_actions.SnsAction(
                hui_ops_team
            )
        )

        # Create Lambda Alarm
        hui_fn_error_alarm = _cloudwatch.Alarm(
            self,
            "konstoneFunctionErrorAlarm",
            metric=huifn.metric_errors(),
            threshold=2,
            evaluation_periods=1,
            datapoints_to_alarm=1,
            period=core.Duration.minutes(5)
        )

        # Inform SNS on Lambda Alarm State
        hui_fn_error_alarm.add_alarm_action(
            _cloudwatch_actions.SnsAction(
                hui_ops_team
            )
        )






