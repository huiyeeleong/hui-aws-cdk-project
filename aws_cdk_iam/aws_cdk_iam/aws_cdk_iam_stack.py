from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_iam as _iam,
    aws_secretsmanager as _secretsmanager,
    aws_ssm as _ssm
)


class AwsCdkIamStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #create secret manager
        user1_pass = _secretsmanager.Secret(
            self,
            "user1pass",
            description="Password for user1",
            secret_name="user1_password"
        )

        #add user1 with secrets manager password
        user1 = _iam.User(
            self,
            "user1",
            password = user1_pass.secret_value,
            user_name = "user1"
        )

        # add user 2 with literal password
        #please dont hardcode the password this is really bad practice
        user2 = _iam.User(
            self,
            "user2",
            password = core.SecretValue.plain_text(
                "Dont-hardcore-the-password"
            ),
            user_name = "user2"
        )

        #Add IAM group
        dev_group = _iam.Group(
            self,
            "Cloud_DevGroup",
            group_name = "dev_group"
        )

        #Add user 2 to dev group
        dev_group.add_user(user2)

        #Add Managed Policy to Group
        dev_group.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )
        )

        #SSM Parameter 1
        param1 = _ssm.StringParameter(
            self,
            "parameter1",
            description="Keys to dev group",
            parameter_name = "/dev/local/randomfile",
            string_value = "12345",
            tier = _ssm.ParameterTier.STANDARD
        )
        #SSM Parameter 2
        param2 = _ssm.StringParameter(
            self,
            "parameter2",
            description="Keys to dev group",
            parameter_name = "/dev/local/randomfile/randomagain",
            string_value = "1234512",
            tier = _ssm.ParameterTier.STANDARD
        )

        #Grant dev group permission to param1
        param1.grant_read(dev_group)

        #Grant group to list all SSM parameters in console
        #add inline policy
        policy = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources= ["*"],
            actions=[
                "ssm:DescribeParameters"
            ]
        )
        policy.sid = "DescribeAllParamtersInConsole"

        #Add inline policy permission to group
        dev_group.add_to_policy(policy)


        #Create IAM Role
        dev_role = _iam.Role(
            self,
            "DevOpsRole",
            assumed_by = _iam.AccountPrincipal(f"{core.Aws.ACCOUNT_ID}"),
            role_name= "Cloud_DevOps_Role"
        )

        #Create Managed Policy & Attach to role
        list_ec2_policy = _iam.ManagedPolicy(
            self,
            "ListEC2Instances",
            description = "list_ec2_policy",
            statements=[
                _iam.PolicyStatement(
                    effect= _iam.Effect.ALLOW,
                    actions = [
                        "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "Cloudwatch:Get*"
                    ],
                    resources=["*"]
                )
            ],
            #Attach this policy to the dev role
            roles=[dev_role]
        )


        #Login url autogeneration
        output1 = core.CfnOutput(
            self,
            "user2loginurl",
            description="Login URL for user2",
            value=f"https://{core.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
        )
