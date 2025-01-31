from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    # TURTLEBOT3_MODEL 설정
    set_turtlebot3_model = SetEnvironmentVariable('TURTLEBOT3_MODEL', 'waffle')

    # 맵 파일 경로 설정
    map_arg = DeclareLaunchArgument(
        'map',
        default_value=PathJoinSubstitution([
            FindPackageShare('project3'),
            'maps',
            'default_map.yaml'
        ]),
        description='Path to map yaml file'
    )

    # Gazebo 실행
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                'turtlebot3_world.launch.py'
            ])
        ]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Navigation2 실행
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_navigation2'),
                'launch',
                'navigation2.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': 'true',
            'map': LaunchConfiguration('map'),
            'rviz_config_file': PathJoinSubstitution([
                FindPackageShare('turtlebot3_navigation2'),
                'rviz',
                'nav2_default_view.rviz'
            ])
        }.items()
    )

    # 초기 위치 노드
    init_node = TimerAction(
        period=5.0,  # 5초 후 실행
        actions=[
            Node(
                package='project3',
                executable='init',
                name='init_node',
                output='screen'
            )
        ]
    )

    # Waypoint Navigation 노드
    waylast_node = TimerAction(
        period=10.0,  # 10초 후 실행
        actions=[
            Node(
                package='project3',
                executable='waylast',
                name='waylast_node',
                output='screen'
            )
        ]
    )

    # Publisher 노드
    pub_way_node = TimerAction(
        period=12.0,  # 12초 후 실행
        actions=[
            Node(
                package='project3',
                executable='pub_way',
                name='pub_way_node',
                output='screen'
            )
        ]
    )

    # 모든 런치 액션 합치기
    return LaunchDescription([
        set_turtlebot3_model,
        map_arg,
        gazebo_launch,
        nav2_launch,
        init_node,
        waylast_node,
        pub_way_node,
    ])
