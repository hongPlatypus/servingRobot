from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='project3',
            executable='init',
            name='init_node',
            output='screen'
        ),
        Node(
            package='project3',
            executable='waylast',
            name='waylast_node',
            output='screen'
        ),
        Node(
            package='project3',
            executable='pub_way',
            name='pub_way_node',
            output='screen'
        ),
    ])
