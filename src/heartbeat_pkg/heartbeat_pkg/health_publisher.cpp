#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class HealthPublisher : public rclcpp::Node {
public:
  HealthPublisher() : Node("health_publisher_cpp"), count_(0) {
    // Create the publisher
    publisher_ = this->create_publisher<std_msgs::msg::String>("system_status", 10);

    // Create a timer that executes every 1 second
    timer_ = this->create_wall_timer(1000ms, std::bind(&HealthPublisher::timer_callback, this));
    
    RCLCPP_INFO(this->get_logger(), "C++ Health Publisher has started.");
  }

private:
  void timer_callback() {
    auto message = std_msgs::msg::String();
    message.data = "System Healthy (C++): " + std::to_string(count_++);
    
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }

  // Member variables (using shared_ptr)
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  // Using std::make_shared to manage node lifetime
  rclcpp::spin(std::make_shared<HealthPublisher>());
  rclcpp::shutdown();
  return 0;
}
```

---

### 2. Configuration Files
C++ packages require two files to tell the compiler how to build the binary.

#### **package.xml**
Ensure these dependencies are inside the `<package>` tags:
```xml
<depend>rclcpp</depend>
<depend>std_msgs</depend>

<buildtool_depend>ament_cmake</buildtool_depend>
```

#### **CMakeLists.txt**
This is the most critical part. It replaces `setup.py` entry points.
```cmake
cmake_minimum_required(VERSION 3.8)
project(heartbeat_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Define the executable
add_executable(health_talker_cpp src/health_publisher.cpp)

# Link dependencies to the executable
ament_target_dependencies(health_talker_cpp rclcpp std_msgs)

# Install the executable so 'ros2 run' can find it
install(TARGETS
  health_talker_cpp
  DESTINATION lib/${PROJECT_NAME})

ament_package()
