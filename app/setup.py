from setuptools import setup, find_packages

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='wbc',
    version='0.0.0',
    author='Maciej Brencz',
    author_email='maciej.brencz@gmail.com',
    description='Flask app providing WBC archives API',
    url='https://github.com/macbre/wbc.macbre.net',
    packages=find_packages(),
    install_requires=[
        'coverage==4.0.1',
        'flask==0.10.1',
        'monolog-python==0.1.0',
        'pytest==2.8.2',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'server=wbc.app:start'
        ],
    }
)