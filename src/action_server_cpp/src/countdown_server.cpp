#include <functional>
#include <memory>
#include <thread>
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rover_actions/action/countdown.hpp" // Our custom action!

class CountdownServer : public rclcpp::Node
{
public:
  using Countdown = rover_actions::action::Countdown;
  using GoalHandleCountdown = rclcpp_action::ServerGoalHandle<Countdown>;

  CountdownServer() : Node("countdown_server")
  {
    // Create the Action Server (Opening the restaurant)
    this->action_server_ = rclcpp_action::create_server<Countdown>(
      this, "countdown",
      std::bind(&CountdownServer::handle_goal, this, std::placeholders::_1, std::placeholders::_2),
      std::bind(&CountdownServer::handle_cancel, this, std::placeholders::_1),
      std::bind(&CountdownServer::handle_accepted, this, std::placeholders::_1));
      
    RCLCPP_INFO(this->get_logger(), "Countdown Action Server is Ready!");
  }

private:
  rclcpp_action::Server<Countdown>::SharedPtr action_server_;

  // 1. RECEIVE THE ORDER
  rclcpp_action::GoalResponse handle_goal(
    const rclcpp_action::GoalUUID & uuid, std::shared_ptr<const Countdown::Goal> goal)
  {
    RCLCPP_INFO(this->get_logger(), "Received goal request with starting count %d", goal->starting_count);
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  // 2. HANDLE CANCELLATIONS (If the user leaves early)
  rclcpp_action::CancelResponse handle_cancel(const std::shared_ptr<GoalHandleCountdown> goal_handle)
  {
    RCLCPP_INFO(this->get_logger(), "Received request to cancel goal");
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  // 3. START COOKING
  void handle_accepted(const std::shared_ptr<GoalHandleCountdown> goal_handle)
  {
    std::thread{std::bind(&CountdownServer::execute, this, std::placeholders::_1), goal_handle}.detach();
  }

  // 4. THE ACTUAL WORK (The Loop)
  void execute(const std::shared_ptr<GoalHandleCountdown> goal_handle)
  {
    RCLCPP_INFO(this->get_logger(), "Executing goal...");
    const auto goal = goal_handle->get_goal();
    auto feedback = std::make_shared<Countdown::Feedback>();
    auto result = std::make_shared<Countdown::Result>();

    int current = goal->starting_count;

    // Loop until we reach 0
    while (current > 0) {
      // Check if user cancelled
      if (goal_handle->is_canceling()) {
        result->success = false;
        result->message = "Cancelled by user!";
        goal_handle->canceled(result);
        RCLCPP_INFO(this->get_logger(), "Goal canceled");
        return;
      }

      // Send Feedback
      feedback->current_count = current;
      feedback->status = "Counting down...";
      goal_handle->publish_feedback(feedback);
      RCLCPP_INFO(this->get_logger(), "Feedback: %d seconds left", current);

      // Wait 1 second
      rclcpp::sleep_for(std::chrono::seconds(1));
      current--;
    }

    // Done! Send Result
    result->success = true;
    result->message = "Countdown complete!";
    goal_handle->succeed(result);
    RCLCPP_INFO(this->get_logger(), "Goal succeeded");
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<CountdownServer>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}

      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
