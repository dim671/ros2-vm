import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Use simulation time; default is true.
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Define the path to the YAML file that you want to load.
    # Here we use the mapper_params_online_async.yaml file from the slam_toolbox package.
    slam_params_file = os.path.join(
        get_package_share_directory("slam_toolbox"),
        'config',
        'mapper_params_online_async.yaml'
    )

    # Optionally, you can declare the launch argument if you want to override it via command-line.
    declare_use_sim_time_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation/Gazebo clock if true'
    )

    # Create the slam_toolbox node. The parameters field will load your YAML file.
    start_async_slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[slam_params_file, {'use_sim_time': use_sim_time}]
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_argument)
    ld.add_action(start_async_slam_toolbox_node)

    return ld

#LAUNCH COMMAND (use_sim_time:=false, on real robot)= ros2 launch slam_toolbox online_async_launch.py params_file:=./src/mob_rov/config/mapper_params_online_async.yaml use_sim_time:=true

