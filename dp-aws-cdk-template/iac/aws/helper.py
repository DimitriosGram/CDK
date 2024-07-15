from aws_cdk import Stack
from constructs import Construct
from typing import Any, List, Dict


class ConstructDict(dict):
    """
    Class to enable easy storage and access of constructs
    """

    def __getattr__(self, k: str) -> Any:
        return self.__getitem__(k)

    def __setattr__(self, k: str, v: Any) -> None:
        self.__setitem__(k, v)

    def __delattr__(self, item: Any) -> None:
        self.__delitem__(item)


class HelperStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        self.branch_name = kwargs.pop("branch_name")
        self.account_id = kwargs.pop("account")
        self.aws_region = kwargs.pop("aws_region")
        self.env = kwargs.pop("db_env")
        self.ecr_repo = kwargs.pop("ecr_repo")
        self.lambda_function_name = kwargs.pop("lambda_function_name")
        self.image_tag = kwargs.pop("image_tag")
        self.email = f"your.email+{self.branch_name}@gmail.com"
        super().__init__(scope, construct_id, **kwargs)

        self.constructs = ConstructDict()

        self.cfn_tags: List[Dict[str, str]] = []
