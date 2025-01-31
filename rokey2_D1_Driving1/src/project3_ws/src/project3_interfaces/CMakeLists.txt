cmake_minimum_required(VERSION 3.8)
project(project3_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# 메시지 파일 정의
set(msg_files
  "msg/TableCommand.msg"
)


# 메시지 및 서비스 파일 생성
rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
)

# 패키지 의존성 추가
ament_export_dependencies(rosidl_default_runtime)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
