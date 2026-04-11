#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/static_transform_broadcaster.h"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h" // The math library

class StaticTfBroadcaster : public rclcpp::Node
{
public:
    StaticTfBroadcaster() : Node("static_tf_broadcaster")
    {
        // Create the broadcaster (A special publisher just for spatial frames)
        tf_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

        // Call our function to send the data once
        make_transforms();
    }

private:
    void make_transforms()
    {
        // 1. Create an empty transform message
        geometry_msgs::msg::TransformStamped t;

        // 2. Add time and frame names
        t.header.stamp = this->get_clock()->now();
        t.header.frame_id = "base_link"; // The parent (Center of robot)
        t.child_frame_id = "lidar_link"; // The child (The sensor)

        // 3. Set the distance (Translation) in meters
        t.transform.translation.x = 0.1; // 10cm forward
        t.transform.translation.y = 0.0; // Centered left/right
        t.transform.translation.z = 0.0; // Same height

        // 4. Set the rotation (Quaternion)
        tf2::Quaternion q;
        q.setRPY(0, 0, 0); // Roll=0, Pitch=0, Yaw=0 (Facing straight ahead)
        
        t.transform.rotation.x = q.x();
        t.transform.rotation.y = q.y();
        t.transform.rotation.z = q.z();
        t.transform.rotation.w = q.w();

        // 5. Send it out!
        tf_broadcaster_->sendTransform(t);
        RCLCPP_INFO(this->get_logger(), "Published Static TF: base_link -> lidar_link");
    }

    std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_broadcaster_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<StaticTfBroadcaster>());
    rclcpp::shutdown();
    return 0;
}

