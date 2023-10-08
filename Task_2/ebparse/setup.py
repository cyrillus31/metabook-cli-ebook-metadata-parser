from setuptools import setup

setup(
    name="ebparse",
    version="0.1",
    py_modules=['ebparse'],
    entry_points={"console_script": ["ebparse=ebparse"]},
    install_requires=["argparse"],
    author="Kirill Fedtsov",
    author_email="kirill.olegovich31@gmail.com",
    description="This cli tool allows you to quickly parse metadata from common e-book formats.",
)
