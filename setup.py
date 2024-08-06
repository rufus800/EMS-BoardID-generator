from setuptools import setup, find_packages

setup(
    name='ems_board_id_generator',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5==5.15.6',
        'bcrypt==3.2.0',
        'pyserial==3.5',
    ],
    entry_points={
        'console_scripts': [
            'ems_board_id_generator=app.main:main',
        ],
    },
    author='Akinsoyinu Samuel',
    author_email='samuelrufus79@gmail.com',
    description='EMS Board ID Generator application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)