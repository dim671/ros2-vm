import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'mob_rov'
    
    # Include the robot_state_publisher launch file from your package
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory(package_name), 'launch', 'presim.launch.py')
        ]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )
    
    # Set the custom Gazebo world file (obstacles.world) from your package's worlds folder
    gazebo_world = os.path.join(get_package_share_directory(package_name), 'worlds', 'obstacles.world')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'world': gazebo_world}.items()
    )
    
    # Spawn the robot in Gazebo (using the robot_description published by rsp)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'mob_rov'],
        output='screen'
    )
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
        output='screen'
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
        output='screen'
    )
    
    # Launch RViz2 with the drive_bot.rviz configuration from your package
    rviz_config = os.path.join(get_package_share_directory(package_name), 'config', 'drive_bot.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )
    
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        rviz_node,
        diff_drive_spawner,
        joint_broad_spawner
    ])

if __name__ == '__main__':
    generate_launch_description()
