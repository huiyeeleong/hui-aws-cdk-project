from aws_cdk import core as cdk
import json

from aws_cdk import (
    core,
    aws_ssm as _ssm,
    aws_secretsmanager as _secretsmanager
)


class AwsCdkCustomizeResourcesStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Create AWS SSM parameter
        parameter1 = _ssm.StringParameter(
            self,
            "parameter1",
            description = "Load Testing Configuration",
            parameter_name = "NoOfConcurrentUsers",
            string_value = "100",
            tier = _ssm.ParameterTier.STANDARD

        )
        parameter2 = _ssm.StringParameter(
            self,
            "parameter2",
            description = "Load Testing Configuration",
            parameter_name = "/local/config/huifolder",
            string_value = "100",
            tier = _ssm.ParameterTier.STANDARD

        )

        parameter3 = _ssm.StringParameter(
            self,
            "parameter3",
            description = "Load Testing Configuration",
            parameter_name = "/local/config/huifolder2",
            string_value = "300",
            tier = _ssm.ParameterTier.STANDARD

        )

        #Create secret manager
        secret1 = _secretsmanager.Secret(
            self,
            "secret1",
            description = "Customer DB Password",
            secret_name = "my_db_password"
        )

        #templated secret
        templated_secret = _secretsmanager.Secret(
            self,
            "secret2",
            description="A templated secret for user data",
            secret_name = "user_kon_attributes",
            generate_secret_string = _secretsmanager.SecretStringGenerator(
                secret_string_template = json.dumps(
                    {"username": "kon"}
                ),
                generate_string_key = "password"
            )
        )



        output_Param1 = core.CfnOutput(
            self,
           "param1",
           description="NoOfConcurrentUser",
           value=f"{parameter1.string_value}" 
        )

        output_Param2 = core.CfnOutput(
            self,
            "secretValue1",
            description = "secret1",
            value= f"{secret1.secret_value}"
        )
