from aws_cdk import core
from aws_cdk.aws_apigateway import Cors, RestApi, LambdaIntegration
from aws_cdk.aws_lambda import Function, Runtime, Code, LayerVersion

class AwsCdkPythonDevGuideStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        # remove custom keys before calling super
        super_kwargs = {k: v for k, v in kwargs.items() if k not in ["origin"]}
        super().__init__(scope, construct_id, **super_kwargs)

        # set default CORS origin to ALL_ORIGINS
        cors_origin = kwargs.get("origin") or "*";
        cors_environment = {
            "CORS_ORIGIN": cors_origin
        }

        # reusable RESTful API CORS options object
        cors_options = {
            "allow_origins": [ cors_origin ], # array containing an origin, or Cors.ALL_ORIGINS
            "allow_methods": Cors.ALL_METHODS, # array of methods eg. [ 'OPTIONS', 'GET', 'POST', 'PUT', 'DELETE' ]
        }

        # ************************************************************************
        # ************************ simple lambda function ************************
        # ************************************************************************

        simple_function = Function(self, "simple-function",
            runtime=Runtime.PYTHON_3_8,
            code=Code.from_asset("handlers/simple"),
            handler="index.main",
            environment={
                **cors_environment,
                "GREETING": "Hello World!"})

        simple_api = RestApi(self, "simple-api",
                  rest_api_name="Simple API sample",
                  description="Simple API sample with no dependencies",
                  default_cors_preflight_options=cors_options)

        simple_api.root.add_method("GET",
            LambdaIntegration(simple_function,
                request_templates={"application/json": '{ "statusCode": "200" }'}))

        # ************************************************************************
        # ********************* layer definition and usage ***********************
        # ************************************************************************

        layer = LayerVersion(self, 'sample-layer',
            code=Code.from_asset('layers/sample-layer'),
            compatible_runtimes=[Runtime.PYTHON_3_7],
            license='MIT',
            description='A sample layer for the layer test functions',)

        # layer test function
        layer_function = Function(self, 'layer-function',
            runtime=Runtime.PYTHON_3_7,
            code=Code.from_asset("handlers/layer"),
            handler='index.main',
            environment=cors_environment,
            layers=[layer])

        # layer api
        layer_api = RestApi(self, 'layer-api',
            default_cors_preflight_options=cors_options)

        layer_api.root.add_method('GET', LambdaIntegration(layer_function));
