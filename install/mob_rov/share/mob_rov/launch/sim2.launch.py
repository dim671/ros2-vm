import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

import xacro

def generate_launch_description():
    # Launch argument: use_sim_time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Paths
    pkg_share = get_package_share_directory('mob_rov')
    xacro_file = os.path.join(pkg_share, 'urdf', 'mob_rov2.xacro')
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'mob_rov2.rviz')  # Adjust if needed

    # 1. Process Xacro -> URDF
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    # 2. Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': use_sim_time
        }]
    )

    # 3. Start Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'pause': 'false'}.items()
    )

    # 4. Spawn Robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'mob_rov2'  # Robot name in Gazebo
        ],
        output='screen'
    )

    # 5. Spawner for joint_state_broadcaster
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    # 6. Spawner for diff_drive_controller (adjust if you use a different controller name)
    diff_drive_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    # 7. RViz (optional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Launch everything
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time if true'
        ),
        gazebo,
        robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
        diff_drive_spawner,
        rviz_node
    ])
