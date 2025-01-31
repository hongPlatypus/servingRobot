from setuptools import find_packages, setup

package_name = 'driving1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'rclpy','project3_interfaces','driving1_interfaces'],
    zip_safe=True,
    maintainer='sujeong',
    maintainer_email='qaz2342004@naver.com',
    description='Kitchen GUI for order processing',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'kitchen_gui = driving1.kitchen_gui:main',  # entry point 수정
        ],
    },
)

