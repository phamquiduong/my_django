from dataclasses import dataclass, field
from typing import Literal


@dataclass
class KeySchema:
    attribute_name: str
    key_type: Literal['HASH', 'RANGE']

    @property
    def dict(self):
        return {
            'AttributeName': self.attribute_name,
            'KeyType': self.key_type,
        }


@dataclass
class AttributeDefinition:
    attribute_name: str
    attribute_type: Literal['S', 'N', 'B']

    @property
    def dict(self):
        return {
            'AttributeName': self.attribute_name,
            'AttributeType': self.attribute_type,
        }


@dataclass
class ProvisionedThroughput:
    read_capacity_units: int = 5
    write_capacity_units: int = 5

    @property
    def dict(self):
        return {
            'ReadCapacityUnits': self.read_capacity_units,
            'WriteCapacityUnits': self.write_capacity_units,
        }


@dataclass
class CreateTableAttr:
    table_name: str
    key_schema: list[KeySchema] = field(default_factory=list)
    attribute_definitions: list[AttributeDefinition] = field(default_factory=list)
    provisioned_throughput: ProvisionedThroughput | None = None
    billing_mode: Literal['PAY_PER_REQUEST', 'PROVISIONED'] = 'PAY_PER_REQUEST'

    @property
    def dict(self) -> dict:
        create_table_attr = {
            'TableName': self.table_name,
            'KeySchema': [ks.dict for ks in self.key_schema],
            'AttributeDefinitions': [ad.dict for ad in self.attribute_definitions],
        }

        if self.provisioned_throughput is not None:
            create_table_attr.update({'ProvisionedThroughput': self.provisioned_throughput.dict})
        else:
            create_table_attr.update({'BillingMode': self.billing_mode})

        return create_table_attr
