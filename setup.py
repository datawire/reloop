from setuptools import setup, find_packages

import versioneer


setup(
    name='reloop',
    description='reloop: painless microservice dev setup',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'reloopd=reloop.reloopd:reloopd'
        ],
    },
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
