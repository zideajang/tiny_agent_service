from codecs import open
from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="multiagent",
    version="1.0.0",
    description="The Multi-Role Programming Framework", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://space.bilibili.com/476895565?spm_id_from=333.1007.0.0",
    author="zidea",
    author_email="zidea",
    keywords="agent multi-role multi-agent programming gpt llm",
    packages=find_packages(
        include=["multiagent"],
        exclude=["contrib", "docs", "examples","resources","workdir","logs","test"]),
    python_requires=">=3.9"
)
