#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class HealthPublisher : public rclcpp::Node
{
public:
 HealthPublisher() : Node("health_publisher")
 {
   publisher_ = this->create_publisher<std_msgs::msg::String>("/health_talker",10);
   timer_ = this->create_wall_timer(1s, std::bind(&HealthPublisher::timer_callback, this));
 
 }

private:
   void timer_callback()
   { 
     auto msg=std_msgs::msg::String();
     msg.data="system is healthy";
     RCLCPP_INFO(this->get_logger(),"Publishing:%s", msg.data.c_str());
     publisher_->publish(msg);
   }
   
   
   rclcpp::TimerBase::SharedPtr timer_;
   rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
 };

int main(int argc, char*argv[])
 {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HealthPublisher>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
 }
    
