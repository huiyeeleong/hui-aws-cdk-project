from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_s3 as _s3,
    aws_s3_deployment as _s3_deployment
)


class AwsCdkStaticWebsiteStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Create s3 bucket
        hui_static_website = _s3.Bucket(
            self,
            "huibucketdemo",
            versioned = True,
            public_read_access = True,
            website_index_document = "index.html",
            website_error_document = "404.html",
            removal_policy = core.RemovalPolicy.DESTROY
        )

        #zip static webpage folder and add to bucket
        #this will automatically create lambda to do it by using this _s3_deployment
        add_assets_to_site = _s3_deployment.BucketDeployment(
            self,
            "deploystaticwebpage",
            sources=[
                _s3_deployment.Source.asset(
                    "/Users/huiyeeleong/Desktop/hui-aws-cdk-project/aws_cdk_static_website/static_webpage"
                )
            ],
            destination_bucket = hui_static_website
        )

