from setuptools import setup

DEVICE_NAME = 'xsight'
HW_SKU = 'x86_64-x2evb-r0'

setup(
    name='sonic-platform',
    version='1.0',
    description='SONiC platform API implementation on Xsight Platforms',
    license='Apache 2.0',
    author='XPLT Team',
    author_email='michaelz@xsightlabs.com',
    url='https://github.com/Azure/sonic-buildimage',
    maintainer='Michael Zaidman',
    maintainer_email='michaelz@xsightlabs.com',
    packages=[
        'sonic_platform',
    ],
    package_dir={
        'sonic_platform': '../../../../device/{}/{}/sonic_platform'.format(DEVICE_NAME, HW_SKU)},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    keywords='sonic SONiC platform PLATFORM',
)
