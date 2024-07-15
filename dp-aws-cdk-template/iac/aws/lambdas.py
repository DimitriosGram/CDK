from aws_cdk import (
    Duration,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    # aws_secretsmanager as secretsmanager
)


from .helper import HelperStack


def build_lambdas(scope: HelperStack) -> None:
    """create lambda stack invocation

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized

    """

    # Variables expected for lambda
    lambda_environment_var = {
        "region": scope.region,
        "bucket_name": scope.constructs.bucket_ref.bucket_name,
        "branch": scope.branch_name,  # branch unused, please review
        "reporting_month": "None",  # YYYYMM
        # define a list of sections or have it passed through Step Functions?
    }

    policy_ref = create_lambda_policy(scope)
    lambda_role = create_lambda_iam_role(scope, policy_ref)

    scope.constructs.dp_lamba_name = create_lambda(
        scope,
        scope.lambda_function_name,
        "main.lambda_handler",
        lambda_environment_var,
        lambda_role,
        512,
    )


def create_lambda_policy(scope: HelperStack):
    """create policy for the lambda

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized
    param aws_account_id: aws account id
    param region: aws region
    returns: policy document

    """
    policy_doc = iam.PolicyDocument(
        statements=[
            iam.PolicyStatement(actions=["sns:Publish"], resources=["*"], effect=iam.Effect.ALLOW),
            iam.PolicyStatement(actions=["secretsmanager:GetSecretValue"], resources=["*"], effect=iam.Effect.ALLOW),
            iam.PolicyStatement(
                actions=["s3:*"],
                resources=[
                    scope.constructs.bucket_ref.bucket_arn,
                    "{}/*".format(scope.constructs.bucket_ref.bucket_arn),
                ],
                effect=iam.Effect.ALLOW,
            ),
        ]
    )
    return policy_doc


def create_lambda_iam_role(scope: HelperStack, policy_doc):
    """create iam role for the lambda

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized
    param policy_doc: policy document for the lambda
    param aws_account_id: aws account id
    param region: aws region
    returns: iam lambda role

    """
    task_policy = iam.ManagedPolicy(
        scope=scope,
        id="dp-lambda-policy",
        managed_policy_name="dp-lambda-policy",
        description="Lambda policy for ...",
        document=policy_doc,
    )

    lambda_role = iam.Role(
        scope=scope,
        id="dp-lambda-role",
        assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[task_policy],
    )

    lambda_role.add_managed_policy(
        iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
    )

    # secret = secretsmanager.Secret("Secret")
    # secret.grant_read(lambda_role)

    # lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerFullAccess"))

    return lambda_role


def create_lambda(scope: HelperStack, lambda_name, lambda_handler, environment_var, lambda_role, mem_size):
    """create lambda stack

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized
    param lambda_name: lambda function name
    param lambda_handler: lambda function handler name as string
    param environment_var: environment variable to the lambda as dict
    param lambda_role: iam role to the lambda
    returns: lambda function

    """

    # Implement a conditional statement for first time deployment. If image doesn't exist, create a small
    #     basic image using DockerImageCode.from_image_asset()
    # Resources:
    # https://devops.stackexchange.com/questions/15225/cdk-how-to-solve-chicken-and-egg-problem-of-lambda-backed-with-ecr

    # Create Lambda
    lambda_func = _lambda.DockerImageFunction(
        scope,
        id=f"{lambda_name}",
        function_name=f"{lambda_name}",
        description="Reads data from RB data warehouse and outputs a number of files to S3 for Regulatory Reporting",
        role=lambda_role,
        environment=environment_var,  # Key value pairs for your lambda function
        timeout=Duration.seconds(900),
        memory_size=mem_size,
        # ephemeral_storage_size=512,
        # on_failure=,
        code=_lambda.DockerImageCode.from_ecr(repository=scope.constructs.repo, tag_or_digest=scope.image_tag),
        # code=_lambda.DockerImageCode.from_image_asset(
        #     directory=str(Path(__file__).parent.parent.parent),  # Path to Dockerfile
        #     file="Dockerfile",
        #     # build_args = {
        #     #     "ACCOUNT_ID": scope.account_id,
        #     #     "REGION": scope.aws_region,
        #     # },
        # ),
    )

    # # Allow our lambda fn to write
    # scope.constructs.bucket_ref.grant_read_write(lambda_func)

    # Add alarm to Lambda
    # The alarm triggers when:
    #   - a threshold of 1 is breached in a 24-hour period, evaluated 288 periods of 300 seconds (24-Hour)
    alarm = cloudwatch.Alarm(
        scope,
        f"{lambda_name}Alarm",
        metric=lambda_func.metric_errors(),
        alarm_name=f"{lambda_name}",
        threshold=1,
        evaluation_periods=288,  # default period is 300 seconds = 300 * 288 = 86400 (24 hours)
        datapoints_to_alarm=1,
        treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        actions_enabled=True,
    )

    alarm.add_alarm_action(cloudwatch_actions.SnsAction(build_sns(scope, f"{lambda_func}")))

    return lambda_func


def build_sns(scope, sns_topic_name):
    sns_topic = sns.Topic(scope, f"RBProject-{sns_topic_name}Topic")
    sns_topic.add_subscription(
        # subscriptions.EmailSubscription(f"dataplatform+{scope.branch_name}@recognisebank.co.uk")
        # Need to pass the branch name from the GitHub workflow to direct emails to
        # the appropriate mailbox
        subscriptions.EmailSubscription(scope.email)
    )
    return sns_topic
