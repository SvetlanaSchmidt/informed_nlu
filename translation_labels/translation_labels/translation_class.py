import json
from typing import List
from dataclasses import dataclass

@dataclass
class Translation():
    source_sentence: str
    target_sentence: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            start=data['source_sentence'],
            end=data['target_sentence'],
        )

    def to_dict(self):
        data = {
            'source_sentence': self.source_sentence,
            'target_sentence': self.target_sentence,
        }

        return data


@dataclass
class TranslationLabel():
    name: str
    description: str
    instances: List[Translation]

    def add_instances(self, instances: List[Translation]):
        self.instances.extend(instances)

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            description=data['description'],
            instances=[Translation.from_dict(instance) for instance in data['instances']]
        )

    def to_dict(self):
        data = {
            'name': self.name,
            'description': self.description,
            'instances': [instance.to_dict() for instance in self.instances]
        }

        return data