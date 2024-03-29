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
        'coverage==7.4.0',
        'flask==3.0.1',
        'Flask-Assets==2.1.0',
        'cssmin==0.2.0',
        'jsmin==3.0.1',
        'gunicorn==21.2.0',
        'monolog-python==0.1.0',
        'PyMySQL==1.1.0',
        'pytest==6.2.5'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'server=wbc.app:start',
            'sitemap=wbc.cli.sitemap:build'
        ],
    }
)
