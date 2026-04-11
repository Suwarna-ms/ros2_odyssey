#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/trigger.hpp"

using namespace std::placeholders;

class ResetServer : public rclcpp::Node
{
public:
  ResetServer() : Node("reset_server")
  { 
    service_ = this->create_service<std_srvs::srv::Trigger>(
     "/reset_sensor",std::bind(&ResetServer::handle_reset,this, _1,_2)
    );
    RCLCPP_INFO(this->get_logger(),"ready to reset the sensor. waiting for command..");
  }

private:
  void handle_reset(const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
                    const std::shared_ptr<std_srvs::srv::Trigger::Response> response)
  {
    (void)request;
   //requesting
    RCLCPP_INFO(this->get_logger(),"Incoming request! Resetting sensor now...");
  //response
    response->success = true;
    response->message = "sensor successfully reset";
    RCLCPP_INFO(this->get_logger(),"Reset complete. sending reply.");
    
  }
   
  rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr service_;
};
int main(int argc, char **argv)
{
    rclcpp::init(argc ,argv);
    rclcpp::spin(std::make_shared<ResetServer>());
    rclcpp::shutdown();
    return 0;
}
