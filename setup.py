from setuptools import setup, find_packages
setup(
    name = 'DTCNS',
    version= '1.0.0',
    description='a Python open source toolbox building Digital Twin-Oriented Complex Network Systems',
    author='Jiaqi Wen',
    author_email='jiaqi_wen@126.com',
    url='https://github.com/JiaqWen/DTCNS',
    classifiers=['Topic :: Digital Twin-Oriented Complex Network Systems',
                 'Programming Language :: Python'],
    license='GPLv3',
    install_requires=['numpy','copy','pandas','networkx','heapq','os','math'],
    python_requires=">=3.6",
    packages=find_packages()
)

