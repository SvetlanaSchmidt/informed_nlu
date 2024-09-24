import json
from typing import List
from dataclasses import dataclass

"""Developed by Maren Pielka"""

@dataclass
class Contradiction():
    premise: str
    hypothesis: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            start=data['premise'],
            end=data['hypothesis'],
        )

    def to_dict(self):
        data = {
            'premise': self.premise,
            'hypothesis': self.hypothesis,
        }

        return data


@dataclass
class ContradictionType():
    name: str
    description: str
    instances: List[Contradiction]

    def add_instances(self, instances: List[Contradiction]):
        self.instances.extend(instances)

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            description=data['description'],
            instances=[Contradiction.from_dict(instance) for instance in data['instances']]
        )

    def to_dict(self):
        data = {
            'name': self.name,
            'description': self.description,
            'instances': [instance.to_dict() for instance in self.instances]
        }

        return data