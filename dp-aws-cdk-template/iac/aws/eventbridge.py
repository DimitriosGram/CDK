from .helper import HelperStack
from aws_cdk import aws_events as events, aws_events_targets as targets


def build_triggers(scope: HelperStack) -> None:
    """create EventBridge invocation

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized.

    """

    create_cron_trigger(scope, "RbToAdenza-schedule", scope.constructs.dp_adenza_lambda)


def create_cron_trigger(scope: HelperStack, id_value, lambda_func_name):
    """create EventBridge cron job trigger

    param scope: scope parameter specifies the parent construct, within which the child construct is initialized.
    param id_value: id value for the EventBridge stack rule.
    param lambda_func_name: lambda function reference to invoke from EventBridge.

    """

    cron_expression = "cron(15 9 1-31 JAN-DEC MON-SUN *)" if scope.branch_name == "main" else "cron(0 0 28 2 ? 2023)"

    schedule = events.Rule(
        scope=scope,
        id=id_value,
        enabled=True,
        rule_name=id_value,
        description="Invoke lambda",
        schedule=events.Schedule.expression(cron_expression),
    )  # Need to set a cron scheduler

    # Set the target of our EventBridge rule to our Lambda function
    schedule.add_target(targets.LambdaFunction(lambda_func_name))
