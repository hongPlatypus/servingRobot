cmake_minimum_required(VERSION 3.5)
project(driving1_interfaces)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)  # std_msgs 패키지를 찾도록 추가

# Generate interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/NotifySoldout.srv"  # 정의한 서비스 파일
  DEPENDENCIES std_msgs  # 의존성 명시
)

ament_package()

