from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='ApiSpbStuRuz',
    version='1.1.1',
    author='Dafter',
    author_email='DafterPlay@mail.ru',
    description='Library implementing API schedules of SPbPu',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/DafterT/ApiSpbStuRuz',
    packages=find_packages(),
    install_requires=['aiohttp>=3.8.3'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='python SPbPu',
    python_requires='>=3.11'
)
