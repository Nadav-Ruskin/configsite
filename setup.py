from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call


# class Post_Develop_Command(develop):
#     """Post-installation for development mode."""
#     def run(self):
#         check_call("apt-get install this-package".split())
#         develop.run(self)

class Post_Install_Command(install):
    """Post-installation for installation mode."""
    def run(self):
        check_call("mkdir /test".split())
        install.run(self)



setup(
    name='configsite',
    version='0.1',
    description='A configuration site for DMS demo.',
    package_data={'': ['license.txt']},
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    install_requires=[]
    # cmdclass={
    #     # 'develop': Post_Develop_Command,
    #     'install': Post_Install_Command
    # }
)
