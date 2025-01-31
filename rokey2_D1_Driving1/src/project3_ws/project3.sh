#!/bin/bash

# Launch turtlebot3_gazebo
echo "Launching TurtleBot3 Gazebo Simulation..."
gnome-terminal -- bash -c "ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py use_sim_time:=true; exec bash"

# Wait for the first process to initialize
sleep 5  # 터틀봇3 Gazebo 시뮬레이션이 초기화될 때까지 대기

# Launch turtlebot3_navigation2
echo "Launching TurtleBot3 Navigation2..."
gnome-terminal -- bash -c "ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=true map:=$HOME/my_map.yaml; exec bash"

# Wait for the second process to initialize
sleep 5  # 네비게이션 초기화 대기

# Launch project3 robot_launch.py
echo "Launching project3..."
gnome-terminal -- bash -c "ros2 launch project3 robot_launch.py; exec bash"

echo "All processes launched!"
