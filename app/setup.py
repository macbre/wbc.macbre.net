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
        'coverage==4.2',
        'flask==0.11.1',
        'Flask-Assets==0.11',
        'cssmin==0.2.0',
        'jsmin==2.2.1',
        'gunicorn==19.6.0',
        'monolog-python==0.1.0',
        'PyMySQL==0.7.6',
        'pytest==2.9.2',
        'redis==2.10.5'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'server=wbc.app:start',
            'stopwords=wbc.cli.stopwords:build'
        ],
    }
)
