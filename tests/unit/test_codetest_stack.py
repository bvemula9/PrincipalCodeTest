import json
import pytest

from aws_cdk import core
from codetest.codetest_stack import CodetestStack


def get_template():
    app = core.App()
    CodetestStack(app, "codetest")
    return json.dumps(app.synth().get_stack("codetest").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
