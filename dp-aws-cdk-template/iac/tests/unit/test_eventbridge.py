from aws_cdk.assertions import Template, Match


def test_sample(template: Template) -> None:
    # print(template.find_resources('AWS::Events::Rule'))

    template.has_resource_properties(
        "AWS::Events::Rule",
        {
            "Description": Match.any_value(),
            "Name": Match.any_value(),
            "ScheduleExpression": "cron(0 0 28 2 ? 2023)",
            "State": "ENABLED",
            "Targets": [{"Arn": {"Fn::GetAtt": [Match.any_value(), "Arn"]}, "Id": "Target0"}],
        },
    )
