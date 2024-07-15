import aws_cdk as cdk
from aws_cdk import aws_s3 as s3, aws_iam as iam
from .helper import HelperStack


def build_bucket(scope: HelperStack):
    """create s3 stack invocation

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized

    """
    scope.constructs.bucket_ref = create_bucket(scope, bucket_name="s3_bucket_name")

    create_bucket_policy(scope, scope.constructs.bucket_ref)


def create_bucket(scope: HelperStack, bucket_name):
    """create s3 bucket invocation

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized
    param bucket_name: bucket name as string

    """
    bucket_ref = s3.Bucket(
        scope,
        id=bucket_name,
        bucket_name=bucket_name,
        # bucket_name=bucket_name,
        versioned=True,
        block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        event_bridge_enabled=False,
        encryption=s3.BucketEncryption.S3_MANAGED,
        intelligent_tiering_configurations=[
            s3.IntelligentTieringConfiguration(
                name="IntelligentTieringConfig",
                # prefix="folder/name",
                archive_access_tier_time=cdk.Duration.days(90),
                deep_archive_access_tier_time=cdk.Duration.days(180),
            )
        ],
        lifecycle_rules=[
            s3.LifecycleRule(
                id="TmpRetentionRule",
                enabled=True,
                prefix="tmp",
                expiration=cdk.Duration.days(1),
                noncurrent_version_expiration=cdk.Duration.days(1),
            ),
            s3.LifecycleRule(
                id="deleteIncompleteMPUs", enabled=True, abort_incomplete_multipart_upload_after=cdk.Duration.days(1)
            ),
        ],
    )

    return bucket_ref


def create_bucket_policy(scope: HelperStack, bucket_ref):
    """create s3 bucket invocation

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized
    param bucket_ref: bucket reference to attach bucket policy to the bucket

    """
    bucket_ref.add_to_resource_policy(
        iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["s3:*"],
            resources=[bucket_ref.bucket_arn, "{}/*".format(bucket_ref.bucket_arn)],
            principals=[
                iam.ArnPrincipal(f"arn:aws:iam::{scope.account_id}:root"),
                # Granting permissions for the Databus-dev account to drop (the raw) files into s3 bucket
            ],
        )
    )


# def create_s3_event_notification(scope: ConstructTrackingStack, bucket_name, lambda_func, prefix, suffix):
#     bucket_name.add_event_notification(
#         s3.EventType.OBJECT_CREATED,
#         s3n.LambdaDestination(lambda_func),
#         s3.NotificationKeyFilter(prefix=prefix, suffix=suffix),
#     )
