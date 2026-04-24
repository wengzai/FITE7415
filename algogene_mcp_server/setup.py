from setuptools import setup, find_packages

setup(
    name='algogene_mcp_server',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        'requests',
        'mcp-server',
    ],
    author='ALGOGENE FINANCIAL TECHNOLOGY COMPANY LIMITED',
    author_email='support@algogene.com',
    description='A set of tools that you can use to interact with ALGOGENE platform, a quant trading platform for strategy backtest, real-time data analytics and trading with 30+ brokers.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/algogene-fintech/algogene_mcp_server',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)