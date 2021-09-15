from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_dynamodb as _dynamodb
)


class AwsCdkDynamodbStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #create dynamodb
        hui_table = _dynamodb.Table(
            self,
            "huiDynamoDB",
            partition_key = _dynamodb.Attribute(
                name = "id",
                type = _dynamodb.AttributeType.STRING
            ),
            #only for testing us this will delet the table if it not use
            removal_policy= core.RemovalPolicy.DESTROY,
            server_side_encryption = True
        )