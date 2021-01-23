import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="aws_cdk_python_dev_guide",
    version="0.0.1",

    description="A guide for AWS CDK development using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="therightstuff",

    license='MIT',

    package_dir={"": "aws_cdk_python_dev_guide"},
    packages=setuptools.find_packages(where="aws_cdk_python_dev_guide"),

    install_requires=[
        "aws-cdk.assets==1.86.0",
        "aws-cdk.aws-apigateway==1.86.0",
        "aws-cdk.aws-applicationautoscaling==1.86.0",
        "aws-cdk.aws-autoscaling-common==1.86.0",
        "aws-cdk.aws-certificatemanager==1.86.0",
        "aws-cdk.aws-cloudformation==1.86.0",
        "aws-cdk.aws-cloudwatch==1.86.0",
        "aws-cdk.aws-codeguruprofiler==1.86.0",
        "aws-cdk.aws-ec2==1.86.0",
        "aws-cdk.aws-ecr==1.86.0",
        "aws-cdk.aws-ecr-assets==1.86.0",
        "aws-cdk.aws-efs==1.86.0",
        "aws-cdk.aws-elasticloadbalancingv2==1.86.0",
        "aws-cdk.aws-events==1.86.0",
        "aws-cdk.aws-iam==1.86.0",
        "aws-cdk.aws-kms==1.86.0",
        "aws-cdk.aws-lambda==1.86.0",
        "aws-cdk.aws-logs==1.86.0",
        "aws-cdk.aws-route53==1.86.0",
        "aws-cdk.aws-s3==1.86.0",
        "aws-cdk.aws-s3-assets==1.86.0",
        "aws-cdk.aws-sns==1.86.0",
        "aws-cdk.aws-sqs==1.86.0",
        "aws-cdk.aws-ssm==1.86.0",
        "aws-cdk.cloud-assembly-schema==1.86.0",
        "aws-cdk.core==1.86.0",
        "aws-cdk.custom-resources==1.86.0",
        "aws-cdk.cx-api==1.86.0",
        "aws-cdk.region-info==1.86.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
