from aws_cdk import core as cdk

from aws_cdk import core
import json

class StacksFromCfnStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #read cfn stack
        try:
            with open("/Users/huiyeeleong/Desktop/hui-aws-cdk-project/stacks_from_cfn/stacks_from_cfn/ssm_param.json", mode="r") as file: 
                cfn_template = json.load(file)
        
        except OSError:
            print("Unable to load CFN template")

        resources_from_cfn_template = core.CfnInclude(
            self,
            "huiinfra",
            template=cfn_template,
            
            
        )
        read_bkt_arn = core.Fn.get_att("EncryptedS3Bucket", "Arn")

        output_1 = core.CfnOutput(
            self,
            "EncryptedBucketArn",
            value=f"{read_bkt_arn.to_string()}",
            description="Arn of encrypted bucket from cfn template"
        )