#!/usr/bin/env python3

from aws_cdk import core
import json

from aws_cdk_python_dev_guide.aws_cdk_python_dev_guide_stack import AwsCdkPythonDevGuideStack

app = core.App()

with open('stages.json') as stagesJson:
    stages = json.load(stagesJson)

with open('regions.json') as regionsJson:
    regions = json.load(regionsJson)

for name in stages:
    stage = stages.get(name)
    for regionKey in stage.get("regions"):
        if regionKey:
            region = regions.get(regionKey)
            AwsCdkPythonDevGuideStack(
                app,
                f"AwsPythonStack-{name}-{regionKey}",
                env=core.Environment(account=region.get("account"), region=region.get("region")),
                origin=stage.get("origin"))
        else:
            # deploy region-agnostic when no region is specified
            AwsCdkPythonDevGuideStack(
                app,
                f"AwsPythonStack-{name}",
                origin=stage.get("origin"))

app.synth()
