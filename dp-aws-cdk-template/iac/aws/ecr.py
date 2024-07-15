from aws_cdk import (
    RemovalPolicy,
    aws_ecr as ecr,
)
from .helper import HelperStack


def build_ecr(scope: HelperStack) -> None:
    scope.constructs.repo = ecr.Repository(
        scope=scope,
        id=f"ecr-{scope.ecr_repo}",
        repository_name=scope.ecr_repo,
        # encryption=ecr.RepositoryEncryption.AES_256,
        encryption=ecr.RepositoryEncryption.KMS,
        lifecycle_rules=[ecr.LifecycleRule(description="Keep latest 2 images", max_image_count=2)],
        image_scan_on_push=True,
        image_tag_mutability=ecr.TagMutability.MUTABLE,
        # All images will be deleted on repository deletion
        removal_policy=RemovalPolicy.DESTROY,
        empty_on_delete=True,
    )
