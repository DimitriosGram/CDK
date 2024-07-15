import aws_cdk as cdk
from aws.aws_stack import RBStackName

app = cdk.App()

# set up for local development, variable will be available during deployment.
dev_account = "344170542049"
prod_account = "556812392285"

# Variables passed from the GitHub CI/CD pipeline's `cdk deploy` command
branch = "release" if app.node.try_get_context("branch") == "main" else "dev"
account = prod_account if app.node.try_get_context("account") == prod_account else dev_account
db_env = "prd" if app.node.try_get_context("account") == prod_account else "uat"
region = "eu-west-2"


RBStackName(
    app,
    "rb-stack-name",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */
    env=cdk.Environment(account=account, region=region),
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    termination_protection=True if branch in ["dev", "release"] else False,
    branch_name=branch,
    account=account,
    aws_region=region,
    # Variables passed from the GitHub CI/CD pipeline's `cdk deploy` command
    lambda_function_name=app.node.try_get_context("lambda_function_name"),
    image_tag=app.node.try_get_context("image_tag"),
    ecr_repo=app.node.try_get_context("aws_ecr_repo"),
    db_env=db_env,
)

app.synth()
