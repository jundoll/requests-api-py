from setuptools import setup

setup(
    name='requests-api-py',
    version="0.1.0",
    license='MIT',
    packages=[
        'src'
    ],
    package_dir={
        'requests_api': 'src'
    }
)
