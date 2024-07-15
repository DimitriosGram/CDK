from aws_cdk.assertions import Template, Match


def test_tags_added_to_services(template: Template) -> None:
    type_list = [
        "AWS::S3::Bucket",
        "AWS::IAM::Role",
        "AWS::Lambda::Function",
        # "AWS::StepFunctions::StateMachine",
        "AWS::SNS::Topic",
        "AWS::Events::Rule",
    ]

    # Define the expected tags as a dictionary
    expected_tags = {
        "Tags": [
            {"Key": "creator", "Value": "DataPlatform"},
            {"Key": "function", "Value": Match.any_value()},
            {"Key": "owner", "Value": "DataPlatform"},
            {"Key": "project", "Value": Match.any_value()},
            {"Key": "purpose", "Value": Match.any_value()},
            {"Key": "repo", "Value": Match.string_like_regexp("https://github.com*")},
            {"Key": "runbook", "Value": Match.string_like_regexp("https://github.com*")},
            {"Key": "service-level", "Value": Match.any_value()},
        ]
    }

    for type in type_list:
        # Assert that the S3 bucket resource has the expected tags
        template.has_resource_properties("AWS::S3::Bucket", Match.object_like(expected_tags))
