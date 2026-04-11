cmake_minimum_required(VERSION 3.8)
project(heartbeat_pkg_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# --- YOUR CUSTOM ADDITIONS START HERE ---

# 1. Create the executable
add_executable(health_talker_cpp src/health_publisher.cpp)

# 2. Link ROS 2 dependencies
ament_target_dependencies(health_talker_cpp rclcpp std_msgs)

# 3. Install the binary so ros2 run can find it
install(TARGETS
  health_talker_cpp
  DESTINATION lib/${PROJECT_NAME})

# --- YOUR CUSTOM ADDITIONS END HERE ---

ament_package()
