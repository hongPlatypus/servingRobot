from setuptools import find_packages, setup

package_name = 'project3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    install_requires=['setuptools', 'project3_interfaces'],  # 통합
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/robot_launch.py']),
    ],
    zip_safe=True,
    maintainer='yeonho',
    maintainer_email='yeonho@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "pub=project3.pub:main",
            "sub=project3.sub:main",
            "way=project3.way:main", 
            "init=project3.init:main",
            "waylast=project3.waylast:main",
            "pub_way=project3.pub_way:main",   
        ],
    },
)
