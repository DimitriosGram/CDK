import base64
import pytest
from moto import mock_aws
import boto3

pytest.aws_region = "eu-west-2"


@pytest.fixture(scope="session", autouse=True)
def s3():
    """
    Pytest fixture that creates the temp bucket in
    the fake moto AWS account
    Yields a fake boto3 s3 client
    """
    with mock_aws():
        bucket_name = "temp_mock_bucket"
        s3 = boto3.client(service_name="s3", region_name=pytest.aws_region)
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": pytest.aws_region})

        yield s3


@pytest.fixture(scope="session", autouse=True)
def secrets_manager():
    """
    Pytest fixture that creates secret manager values
    """
    with mock_aws():
        sm = boto3.client(service_name="secretsmanager", region_name=pytest.aws_region)

        secret_id = "my-secret-id"
        secret_string = "This is a secret string"
        sm.create_secret(Name=secret_id, SecretString=secret_string)

        secret_id_binary = "my-secret-id-binary"
        binary_secret_data = b"binary-secret-id"
        binary_secret_string = base64.b64encode(binary_secret_data).decode("utf-8")
        sm.create_secret(Name=secret_id_binary, SecretString=binary_secret_string)

        yield sm


@pytest.fixture(scope="session", autouse=True)
def ssm():
    """
    Pytest fixture that creates ssm parameter
    Yields a fake boto3 ssm client
    """
    with mock_aws():
        ssm = boto3.client(service_name="ssm", region_name=pytest.aws_region)
        # Set up mock data for the parameter
        param_name = "my-parameter"
        param_value = "secret_value"
        ssm.put_parameter(Name=param_name, Value=param_value, Type="String", Overwrite=True)

        yield ssm
