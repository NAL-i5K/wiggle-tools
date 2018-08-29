from setuptools import setup, find_packages

setup(
    name='wiggle',
    author='NAL i5k workspace',
    author_email='i5k@ars.usda.gov',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gap2bigwig=wiggle.gap2bigwig:run_main',
            'GCcontent2bigwig=wiggle.GCcontent2bigwig:run_main'
        ]
    }
)
