from setuptools import setup, find_packages

setup(
    name='mysql-parquet-lib',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A utility library to connect to MySQL and export data to Parquet format',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'mysql-connector-python',
        'pyarrow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)