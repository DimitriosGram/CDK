from aws_cdk import Tags
from constructs import Construct
from .helper import HelperStack
from .s3 import build_bucket
from .ecr import build_ecr
from .lambdas import build_lambdas
from .eventbridge import build_triggers


class RBStackName(HelperStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._add_tags()

        # The code that defines your stack goes here
        build_bucket(self)
        build_ecr(self)
        build_lambdas(self)
        build_triggers(self)

    def _add_tags(self) -> None:
        """
        Sets the tags on the stack so the stack's constructs inherit them
        :return: None
        """
        tag_dict = {
            "creator": "DataPlatform",
            "owner": "DataPlatform",
            "service-level": "Check Confluence",
            "function": "Check Confluence",
            "purpose": "Check Confluence",
            "project": "Check Confluence",
            "runbook": "github repo link to runbook docs/runbook.md",
            "repo": "github repo address",
        }
        tags = Tags.of(self)

        for k, v in tag_dict.items():
            tags.add(k, v)
            self.cfn_tags.append({"key": k, "value": v})
