#!/usr/bin/env python3

from aws_cdk import core

from codetest.codetest_stack import CodetestStack


app = core.App()
CodetestStack(app, "codetest", env={'region': 'us-west-2'})

app.synth()
