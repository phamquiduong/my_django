import logging
from contextlib import contextmanager
from typing import Any, Literal

import boto3
from django.conf import settings

from common.schemas.dynamodb import CreateTableAttr

logger = logging.getLogger(__name__)


class DynamoDBService:
    def __init__(
        self,
        region_name: str = settings.DYNAMO_DB_CONFIG['REGION_NAME'],
        endpoint_url=settings.DYNAMO_DB_CONFIG['ENDPOINT_URL'],
        aws_access_key_id: str = settings.DYNAMO_DB_CONFIG['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key: str = settings.DYNAMO_DB_CONFIG['AWS_SECRET_ACCESS_KEY'],
    ) -> None:
        connect_attr = {
            'region_name': region_name,
            'endpoint_url': endpoint_url,
            'aws_access_key_id': aws_access_key_id,
            'aws_secret_access_key': aws_secret_access_key,
        }

        self.resource = boto3.resource('dynamodb', **connect_attr)
        self.client = boto3.client('dynamodb', **connect_attr)

    def create_table(self, create_table_attr: CreateTableAttr) -> None:
        self.client.create_table(**create_table_attr.dict)  # type:ignore

    def delete_table(self, table_name: str) -> None:
        self.client.delete_table(TableName=table_name)  # type:ignore

    def create_ttl(self, table_name: str, attribute_name: str) -> None:
        update_ttl_attr = {
            'TableName': table_name,
            'TimeToLiveSpecification': {
                'Enabled': True,
                'AttributeName': attribute_name
            }
        }
        self.client.update_time_to_live(**update_ttl_attr)  # type:ignore

    def insert(self, table_name: str, data: dict) -> None:
        table = self.resource.Table(table_name)  # type:ignore
        table.put_item(Item=data)

    def get(self, table_name: str, query: dict[str, Any]) -> dict:
        """
        Args:
            query (dict[str, Any]): Make sure the query finds only one record
        """
        table = self.resource.Table(table_name)  # type:ignore
        response = table.get_item(Key=query)
        return response.get('Item')

    def update(  # pylint: disable=R0913,R0917
        self,
        table_name: str,
        query: dict[str, Any],
        expression: str,
        expression_value: dict[str, Any],
        return_value: Literal['NONE', 'ALL_OLD', 'UPDATED_OLD', 'ALL_NEW', 'UPDATED_NEW'] = 'UPDATED_NEW'
    ) -> dict:
        """
        Args:
            query (dict[str, Any]): Make sure the query finds only one record
            expression (str): The update expression. Example: `SET #field = :new_value`
        """
        table = self.resource.Table(table_name)  # type:ignore
        response = table.update_item(
            Key=query,
            UpdateExpression=expression,
            ExpressionAttributeValues=expression_value,
            ReturnValues=return_value,
        )
        return response['Attributes']

    def delete(self, table_name: str, query: dict[str, Any]) -> None:
        """
        Args:
            query (dict[str, Any]): Make sure the query finds only one record
        """
        table = self.resource.Table(table_name)  # type:ignore
        table.delete_item(Key=query)


@contextmanager
def get_dynamodb_service():
    try:
        yield DynamoDBService()
    except Exception as exc:
        logger.exception(exc)
        raise
    finally:
        pass
