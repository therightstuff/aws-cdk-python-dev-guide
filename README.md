
# AWS CDK Python Dev Guide

This project is a template that's intended to serve as a guide for working with CDK in Python.

This project is based on the [aws-cdk-js-dev-guide](https://github.com/therightstuff/aws-cdk-js-dev-guide).

## Tooling setup for AWS development

### Preamble

It is valuable and necessary to go through the following steps to familiarize yourself with the tools.

- create programmatic user in IAM with admin permissions
- if you're using visual studio code (recommended), [configure aws toolkit](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/setup-toolkit.html)
- set up credentials with the profile id "default"
- get 12 digit account id from My Account in console
- follow [the CDK hello world tutorial](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#hello_world_tutorial)

### Tool Versions

CDK, like SAM, tends to be updated frequently with breaking changes. Prior to committing changes, please ensure that you are using the latest versions and that everything is building and running correctly.

### CDK Initialization

The first step to creating a CDK project is initializing it with `cdk init app` (eg. `cdk init app --language python`), and a CDK project cannot be initialized if the project directory isn't empty. If you would like to use an existing project (like this one) as a template, bear in mind that you will have to rename the stack in multiple locations and it would probably be safer and easier to create a new project and copy and paste in the bits you need (estimated time: 20-30 minutes if you're not familiar with the project structure).

## Python setup

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```bash
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```bash
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```bash
.venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```bash
pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```bash
cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

- `cdk ls`          list all stacks in the app
- `cdk synth`       emits the synthesized CloudFormation template(s)
- `cdk deploy`      deploy this stack to your default AWS account/region
- `cdk diff`        compare deployed stack with current state

### Stack definition

The stack definition is located in the `/aws_cdk_python_dev_guide` folder, this is where the stack is configured for deployment.

See [AWS CDK API documentation](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html) for reference.

#### Lambda Functions

Lambda functions are defined in the `handlers` directory, and include the following samples:

- `simple`: a stateless function

Lambda functions MUST return responses in the following format:

```python
{
    "statusCode": 200,
    "headers": {},
    "body": json.dumps({...})
}
```

#### Lambda Layers

Layers are composite packages that multiple lambda functions can reference.

To create a layer, simply add a `<layer name>` folder in the `layers` directory that has the following folder structure:

```text
|- `layers/layer-name`
    |- `python`
        |- `lib`
            |- `python3.X` # must match your lamdba runtime
                |- `site-packages`
                    |- `MODULE_1`
                    |- `MODULE_2`
```

After installing a module in your virtual environment (eg. `pip install arrow`) you can simply copy its folder from the matching location under `.venv`, eg. `.venv/lib/python3.7/site-packages/arrow`.

WARNING: A lambda function can use a maximum of 5 layers and be a maximum of 250MB unzipped.

#### API Gateway Integrations

When you create a `RestApi` object, the `.root` resource defaults to `/prod/`. You can add HTTP method handlers to the root, or add resource objects and add method handlers to those. To add a resource parameter, simply add a resource enclosed in curly braces (`{}`) and this will be accessible in the `event` object as `event.get("pathParameters")`.

Querystring parameters will be available in the `event` object as `event.get("queryStringParameters")`.

NOTE: it is not possible to rename a path parameter, as cdk will attempt to deploy the new resource before removing the old one and it cannot deploy two resources with the same path structure. The workaround suggested on [the serverless issue thread](https://github.com/serverless/serverless/issues/3785) is to comment out the resource definition, deploy, then uncomment it and deploy again.

`aws_cdk_python_dev_guide/aws_cdk_python_dev_guide_stack.py`:

```python
# Enable CORS for all resources of an api
api = RestApi(self, 'api-name', {
    default_cors_preflight_options={
        # array containing an origin, or Cors.ALL_ORIGINS
        allow_origins: [ cors_origin ],
        # array of methods eg. [ 'OPTIONS', 'GET', 'POST', 'PUT', 'DELETE' ]
        allow_methods: Cors.ALL_METHODS,
    }
})

# OR

# Enable CORS for a specific api resource
api2 = RestApi(self, 'api2-name');
api2_objects = api2.root.add_resource('objects');
api2_objects.add_cors_preflight({
    # array containing an origin, or Cors.ALL_ORIGINS
    allow_origins: [ cors_origin ],
    # array of methods eg. [ 'OPTIONS', 'GET', 'POST', 'PUT', 'DELETE' ]
    allow_methods: Cors.ALL_METHODS,
})
```

`handlers/myhandler/index.py`:

```python
return {
    "statusCode": 200,
    "headers": {
        'Access-Control-Allow-Origin': os.environ['CORS_ORIGIN'],
        'Access-Control-Allow-Credentials': True,
    },
    "body": json.dumps({ "success": True })
})
```

NOTE: This project defines an origin per stack in the `./stages.json` file, which requires a modification to the `AwsCdkPythonDevGuideStack` signature / kwargs. This is not a CDK requirement, you should configure it in any way that suits your purposes.

For more details see [https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigateway-readme.html](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigateway-readme.html) and [https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.CorsOptions.html](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.CorsOptions.html).

### Deployment

By default, CDK deploys stacks that are [environment-agnostic](https://docs.aws.amazon.com/cdk/latest/guide/environments.html). To enable environment-agnostic deployments, run `cdk bootstrap` before `cdk deploy`, but configuring specific regions is probably the safer practice.

To deploy to specific regions, update the `./regions.json` file with the desired region and account numbers.

An example for stack configuration has been provided in `./stages.json`.

To deploy a stack, `cdk deploy <stack name>` (wildcards are supported).

If you don't want to review each set of changes, use the `--require-approval=never` option (not recommended).

The `Outputs` displayed at the end of the process include the API Gateway endpoints. These can be used as-is for the example lambda functions.

### Redeploying a Stack

One of the great advantages of using CDK is that updating a stack is as simple as running the `cdk deploy <stack name>` again.

### Debugging

Testing a lambda function via the API Gateway interface is unlikely to report useful error details. If a function is not behaving correctly or is failing, go to your CloudWatch dashboard and find the log group for the function.

### Deleting a Stack

If for whatever reason you decide you want to delete a stack in its entirety, install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and run `aws cloudformation delete-stack --stack-name <stack name> --region <region name>`.
