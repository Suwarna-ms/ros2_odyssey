cmake_minimum_required(VERSION 3.8)
project(control_server_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_srvs REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  add_executable(server_exec src/reset_server.cpp)
  set(ament_cmake_copyright_FOUND TRUE)
  ament_target_dependencies(server_exec rclcpp std_srvs)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
  install(TARGETS server_exec DESTINATION lib/${PROJECT_NAME})
endif()

ament_package()
