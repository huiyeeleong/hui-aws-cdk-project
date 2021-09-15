from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_sqs as _sqs
)


class AwsCdkSqsStackStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Create SQS queue
        hui_queue = _sqs.Queue(
            self,
            "huiqueue",
            queue_name = "hui_queue.fifo",
            fifo = True,
            encryption = _sqs.QueueEncryption.KMS_MANAGED,
            retention_period = core.Duration.days(4),
            visibility_timeout = core.Duration.seconds(45)
        )
