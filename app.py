#!/usr/bin/env python3

from aws_cdk import core
import json

from aws_cdk_python_dev_guide.aws_cdk_python_dev_guide_stack import AwsCdkPythonDevGuideStack

app = core.App()
core.Tags.of(app).add("app", "my-app-tag")

with open('stages.json') as stagesJson:
    stages = json.load(stagesJson)

with open('regions.json') as regionsJson:
    regions = json.load(regionsJson)

for name in stages:
    stage = stages.get(name)
    for regionKey in stage.get("regions"):
        if regionKey:
            region = regions.get(regionKey)
            region_options = core.Environment(account=region.get("account"),
                                              region=region.get("region"))
            stack_name = f"AwsPythonStack-{name}-{regionKey}"
        else:
            # deploy region-agnostic when no region is specified
            region_options = None
            stack_name = f"AwsPythonStack-{name}"

        stack_instance = AwsCdkPythonDevGuideStack(
            app,
            stack_name,
            env=region_options,
            origin=stage.get("origin"))
        # this will add a stack tag to all stack components
        core.Tags.of(stack_instance).add("stack-name", stack_name)

app.synth()
