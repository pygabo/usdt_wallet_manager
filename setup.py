from setuptools import setup, find_packages

setup(
    name='usdt_wallet_manager',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'usdt-wallet=usdt_wallet_manager.transactions:main',
        ],
    },
    author='Jose gabriel guzman',
    author_email='pygabo@gmail.com',
    description='A package to fetch and calculate USDT transactions from Etherscan.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pygabo/usdt_wallet_manager',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
