from setuptools import setup

setup(
    name="metabook",
    version="0.1",
    py_modules=['metabook'],
    entry_points={"console_script": ["metabook=metabook"]},
    install_requires=["argparse"],
    author="Kirill Fedtsov",
    author_email="kirill.olegovich31@gmail.com",
    description="This cli tool allows you to quickly parse metadata from common e-book formats.",
)
