from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    core,
    aws_sns as _sns,
    aws_sns_subscriptions as _subs
)


class AwsCdkSnsStackStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        hui_topic = _sns.Topic(
            self,
            "huitopic",
            display_name= "Latest topics on hui",
            topic_name = "HuiHotTopic"
        )

        #Add subscription to sns topic
        hui_topic.add_subscription(
            _subs.EmailSubscription("dummy@email.com")
        )
