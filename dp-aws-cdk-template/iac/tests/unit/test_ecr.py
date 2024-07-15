from aws_cdk.assertions import Template, Match


def test_ecr(template: Template) -> None:
    template.has_resource_properties(
        "AWS::ECR::Repository",
        {
            "EmptyOnDelete": True,
            "EncryptionConfiguration": {"EncryptionType": "KMS"},
            "ImageScanningConfiguration": {"ScanOnPush": True},
            "ImageTagMutability": "MUTABLE",
            "LifecyclePolicy": {
                "LifecyclePolicyText": '{"rules":[{"rulePriority":1,"description"'
                + ':"Keep latest 2 images","selection":{"tagStatus":"any","countType"'
                + ':"imageCountMoreThan","countNumber":2},"action":{"type":"expire"}}]}'
            },
            "RepositoryName": "dp-repo-name",
            "Tags": Match.any_value(),
        },
    )


def test_ecr_repository_count(template: Template) -> None:
    template.resource_properties_count_is(
        "AWS::ECR::Repository",
        Match.object_like({}),
        1,
    )
