import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    rplidar_ros2_dir = get_package_share_directory(
        'rplidar_ros')

    urdf2tf = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [rplidar_ros2_dir ,'/launch', '/urdf2tf.launch.py']),
    )

    odom2tf = launch_ros.actions.Node(
        package='rplidar_ros',
        executable='odom2tf',
        output='screen'
    )

    microros_agent = launch_ros.actions.Node(
        package='micro_ros_agent',
        executable='micro_ros_agent',
        arguments=['udp4','--port','8888'],
        output='screen'
    )



    rplidar = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [rplidar_ros2_dir, '/launch', '/rplidar_c1_launch.py']),
    )

    # 使用 TimerAction 启动后 5 秒执行 ydlidar 节点
    rplidar_delay = launch.actions.TimerAction(period=5.0, actions=[rplidar])
    
    return launch.LaunchDescription([
        urdf2tf,
        odom2tf,
        microros_agent,
        rplidar_delay
    ])