from aws_cdk import core as cdk
from aws_cdk import (
    core,
    aws_rds as _rds,
    aws_iam as _iam,
    aws_ec2 as _ec2
)


class rds_tier_stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str,rds_security_group, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #Create RDS Stack
        hui_db = _rds.DatabaseInstance(
            self,
            "rdsID",
            master_username = "admin",
            database_name = "hui_rds",
            engine = _rds.DatabaseInstanceEngine.MYSQL,
            vpc=vpc,
            port=3306,
            allocated_storage = 30,
            multi_az = False,
            instance_class = _ec2.InstanceType.of(
                _ec2.InstanceClass.BURSTABLE2,
                _ec2.InstanceSize.MICRO
            ),
            removal_policy = core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            delete_automated_backups=True,
            backup_retention=core.Duration.days(7)
        )
        #Inbound rule for RDS
        for sg in rds_security_group:
            hui_db.connections.allow_default_port_from(
                sg, "Allow EC2 ASG access to RDS MySQL")

        # Output RDS Database EndPoint Address
        output_1 = core.CfnOutput(self,
                                  "DatabaseConnectionCommand",
                                  value=f"mysql -h {hui_db._instance_endpoint_address} -P 3306 -u mystiquemaster -p",
                                  description="Connect to the database using this command"
                                  )