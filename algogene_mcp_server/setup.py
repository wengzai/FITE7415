from pathlib import Path

from setuptools import setup, find_packages


description = (
    "A set of tools that you can use to interact with ALGOGENE platform, "
    "a quant trading platform for strategy backtest, real-time data analytics "
    "and trading with 30+ brokers."
)


def read_long_description():
    setup_dir = Path(__file__).resolve().parent
    for readme_path in [setup_dir / "README.md", setup_dir.parent / "README.md"]:
        if readme_path.exists():
            return readme_path.read_text(encoding="utf-8")
    return description

setup(
    name='algogene_mcp_server',
    version='0.1.8',
    packages=['algogene_mcp_server'] + [
        f'algogene_mcp_server.{pkg}' for pkg in find_packages(where='.')
    ],
    package_dir={'algogene_mcp_server': '.'},
    install_requires=[
        'requests',
        'mcp-server',
    ],
    author='ALGOGENE FINANCIAL TECHNOLOGY COMPANY LIMITED',
    author_email='support@algogene.com',
    description=description,
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/algogene-fintech/algogene_mcp_server',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
