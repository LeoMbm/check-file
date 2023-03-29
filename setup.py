from setuptools import setup


setup(
    name='beatstemp',
    version='0.1',
    packages=['beatstemp'],
    install_requires=open('./requirements.txt').readlines(),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'beatstemp=beatstemp:main.run',
        ],
    },
)
