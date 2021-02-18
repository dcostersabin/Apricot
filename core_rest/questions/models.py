from abc import ABCMeta

from django.db import models
from rest_framework import serializers


class Question(models.Model):
    details = models.TextField(blank=False, verbose_name='details', null=False)
    inputs = models.TextField(blank=False, verbose_name='inputs', null=False)
    output = models.TextField(blank=False, verbose_name='output', null=False)

    def serialize(self):
        data = {
            'id': self.id,
            'details': self.details,
            'inputs': self.inputs,
            'output': self.output
        }
        return data


class QuestionSerializer(serializers.Serializer):
    details = serializers.CharField(min_length=10)
    inputs = serializers.CharField(min_length=1)
    output = serializers.CharField(min_length=1)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.details = validated_data.get('details', instance.details)
        instance.inputs = validated_data.get('inputs', instance.inputs)
        instance.output = validated_data.get('output', instance.output)
