from setuptools import setup

setup(
    name='twecoll3',
    version='2.0.0',
    description='CLI tool to create gdf and gexf files of social networks for use with Gephi',
    url='https://github.com/lucahammer/twecoll3',
    author='Luca Hammer',
    py_modules=['twecoll3'],
    install_requires=[
        'Click',
        'tqdm',
        'TwitterAPI'
    ],
    entry_points='''
        [console_scripts]
        twecoll3=twecoll3:cli
    ''',
)
