from aws_cdk.assertions import Template, Match


def test_create_lambda(template: Template) -> None:
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "FunctionName": Match.any_value(),
            "PackageType": "Image",
            "Role": Match.any_value(),
            "Code": {
                "ImageUri": Match.any_value(),
            },
            "Tags": Match.any_value(),
        },
    )

    # Currently part of the lambda create_lambda function
    template.has_resource_properties(
        "AWS::CloudWatch::Alarm",
        {
            "AlarmActions": [{"Ref": Match.any_value()}],
            "ComparisonOperator": "GreaterThanOrEqualToThreshold",
            "DatapointsToAlarm": 1,
            "EvaluationPeriods": 288,
            # "AlarmDescription": Match.any_value(),
            "AlarmName": Match.any_value(),
            "Dimensions": [
                {"Name": "FunctionName", "Value": {"Ref": Match.any_value()}},
            ],
            "MetricName": "Errors",
            "Namespace": "AWS/Lambda",
            "Period": 300,
            "Statistic": "Sum",
            "Threshold": 1,
            "TreatMissingData": "notBreaching",
        },
    )


def test_create_lambda_iam_role(template: Template) -> None:
    template.has_resource_properties(
        "AWS::IAM::Role",
        {
            "AssumeRolePolicyDocument": {
                "Statement": [
                    {"Action": "sts:AssumeRole", "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}}
                ],
                "Version": "2012-10-17",
            },
            "ManagedPolicyArns": [
                {"Ref": Match.string_like_regexp("dplambdapolicy*")},
                {
                    "Fn::Join": [
                        "",
                        [
                            "arn:",
                            {"Ref": "AWS::Partition"},
                            ":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                        ],
                    ]
                },
                # {"Fn::Join": ["", ["arn:", {"Ref": "AWS::Partition"}, ":iam::aws:policy/AmazonAthenaFullAccess"]]},
            ],
        },
    )


def test_subscription_endpoint(template: Template) -> None:
    # Make sure subscription sends email to team account
    template.has_resource_properties(
        "AWS::SNS::Subscription",
        Match.object_like({"Endpoint": Match.string_like_regexp("your.email\\+[a-z]+@recognisebank.co.uk")}),
    )
