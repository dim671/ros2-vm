from setuptools import setup, find_packages
from glob import glob
import os

package_name = 'mob_rov'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # So ROS2 knows about your package
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Install all launch files
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),

        # Install URDF and Xacro files
        # This grabs all .urdf and .xacro files in the urdf folder
        ('share/' + package_name + '/urdf', glob('urdf/*.urdf') + glob('urdf/*.xacro')),

        # Install config files (e.g., ros2_control.yaml)
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dgomartir',
    maintainer_email='dgomartir@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Add your console scripts here if needed
        ],
    },
)
