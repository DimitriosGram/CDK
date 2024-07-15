import os
import pytest
import aws_cdk as cdk
from aws_cdk.assertions import Template
from iac.aws.aws_stack import RBStackName

@pytest.fixture(scope="session", autouse=True)
def template() -> Template:
    region = os.environ.get("AWS_REGION", "eu-west-2")
    account = os.environ.get("AWS_ACCOUNT", "344170542049")
    env = cdk.Environment(region=region, account=account)
    ecr_repo = "dp-rb-repo-name"
    lambda_function_name = "RBLambdaName"
    image_tag = "latest"
    db_env = "uat"

    app = cdk.App()
    stack = RBStackName(
        app,
        "rb-stack-name",
        env=env,
        branch_name="dev",
        account=account,
        aws_region=region,
        ecr_repo=ecr_repo,
        lambda_function_name=lambda_function_name,
        image_tag=image_tag,
        db_env=db_env,
    )
    # print(f"--------------- {dir(Template.from_stack(stack))} ---------------------")
    print(f">>> \n{Template.from_stack(stack).find_resources('AWS::ECR::Repository')}\n <<<")
    return Template.from_stack(stack)
