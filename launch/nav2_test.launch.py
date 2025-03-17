import os
import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir


def generate_launch_description():
    navigation2_dir = "/home/wjhh/fortest/src/rplidar_ros"
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    rviz_fornav2_config_dir = os.path.join(
    nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')
    
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    map_yaml_path = launch.substitutions.LaunchConfiguration(
        'map', default=os.path.join(navigation2_dir, 'map', 'second_map.yaml'))
    nav2_param_path = launch.substitutions.LaunchConfiguration(
        'params_file', default=os.path.join(navigation2_dir, 'config', 'nav2_params.yaml'))


    return LaunchDescription([
   

    DeclareLaunchArgument(
            'use_sim_time', default_value=use_sim_time,
            description='Use simulation (Gazebo) clock if true'),

    DeclareLaunchArgument(
            'map', default_value=map_yaml_path,
            description='Full path to map file to load'),
    DeclareLaunchArgument(
            'params_file', default_value=nav2_param_path,
            description='Full path to param file to load'),      


        launch.actions.IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_bringup_dir, '/launch', '/bringup_launch.py']),
            # 使用 Launch 参数替换原有参数
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_param_path}.items(),
                ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_fornav2_config_dir],
            output='screen'
        ),

    ])