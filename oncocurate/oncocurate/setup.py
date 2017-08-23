from setuptools import setup

setup(
    name='curation_assistant',
    version='1.0',
    py_modules=['oncocurate'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        oncocurate=oncocurate:cli
    ''',
)