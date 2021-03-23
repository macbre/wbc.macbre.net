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
        'coverage==5.5',
        'flask==1.1.2',
        'Flask-Assets==0.12',
        'cssmin==0.2.0',
        'jsmin==2.2.2',
        'gunicorn==20.0.4',
        'monolog-python==0.1.0',
        'PyMySQL==0.9.2',
        'pytest==5.4.2'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'server=wbc.app:start',
            'sitemap=wbc.cli.sitemap:build'
        ],
    }
)
