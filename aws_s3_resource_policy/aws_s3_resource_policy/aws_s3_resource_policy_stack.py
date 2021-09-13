from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_s3 as _s3,
    aws_iam as _iam
)


class AwsS3ResourcePolicyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Create S3 bucket
        hui_bucket = _s3.Bucket(
            self,
            "HuiBucketID",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        #Add Bucket Resource Policy
        hui_bucket.add_to_resource_policy(
            _iam.PolicyStatement(
                effect = _iam.Effect.ALLOW,
                actions = ["s3:GetObject"],
                resources = [hui_bucket.arn_for_objects("*html")],
                principals= [_iam.AnyPrincipal()]
            )
        )

        #Deny http access
        hui_bucket.add_to_resource_policy(
            _iam.PolicyStatement(
                effect= _iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{hui_bucket.bucket_arn}/*"],
                principals= [_iam.AnyPrincipal()],
                conditions={
                    "Bool": {"aws:SecureTansport":False}
                }
            )
        )


