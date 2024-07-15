from aws_cdk.assertions import Template, Match


def test_s3_buckets_created(template: Template) -> None:
    template.resource_properties_count_is(
        "AWS::S3::Bucket",
        Match.object_like(
            {
                "BucketEncryption": {
                    "ServerSideEncryptionConfiguration": [{"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
                },
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": True,
                    "BlockPublicPolicy": True,
                    "IgnorePublicAcls": True,
                    "RestrictPublicBuckets": True,
                },
                "VersioningConfiguration": {"Status": "Enabled"},
            }
        ),
        1,
    )


def test_s3_intelligent_tiering_configuration(template: Template) -> None:
    template.has_resource_properties(
        "AWS::S3::Bucket",
        Match.object_like(
            {
                "IntelligentTieringConfigurations": [
                    {
                        "Id": "RBtoAdenzaIntelligentTieringConfig",
                        "Status": "Enabled",
                        "Tierings": [
                            {"AccessTier": "ARCHIVE_ACCESS", "Days": 90},
                            {"AccessTier": "DEEP_ARCHIVE_ACCESS", "Days": 180},
                        ],
                    }
                ]
            }
        ),
    )


def test_s3_lifecycle_rules_configuration(template: Template) -> None:
    template.has_resource_properties(
        "AWS::S3::Bucket",
        Match.object_like(
            {
                "LifecycleConfiguration": {
                    "Rules": [
                        {
                            "Id": "TmpRetentionRule",
                            "Prefix": "tmp",
                            "Status": "Enabled",
                            "ExpirationInDays": 1,
                            "NoncurrentVersionExpiration": {"NoncurrentDays": 1},
                        },
                        {
                            "Id": "deleteIncompleteMPUs",
                            "Status": "Enabled",
                            "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 1},
                        },
                    ]
                }
            }
        ),
    )


def test_s3_bucket_access(template: Template) -> None:
    template.has_resource_properties(
        "AWS::S3::BucketPolicy",
        Match.object_like(
            {
                "PolicyDocument": {
                    "Statement": [
                        {
                            "Action": "s3:*",
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": Match.string_like_regexp("arn:aws:iam::(344170542049|556812392285):root"),
                            },
                            "Resource": [
                                {"Fn::GetAtt": [Match.string_like_regexp("rbbucketname*"), "Arn"]},
                                {
                                    "Fn::Join": [
                                        "",
                                        [{"Fn::GetAtt": [Match.string_like_regexp("rbbucketname*"), "Arn"]}, "/*"],
                                    ]
                                },
                            ],
                        }
                    ]
                }
            }
        ),
    )
