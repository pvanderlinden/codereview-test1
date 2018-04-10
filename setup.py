from setuptools import setup, find_packages


setup(
    name='extractor',
    description='HTML metadata extractor',

    version='1.0',
    packages=find_packages(exclude=('tests',)),

    install_requires=(
        'requests',
        'beautifulsoup4',
        'python-dateutil',
    ),

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3.5',
    ],

    zip_safe=False,
)
