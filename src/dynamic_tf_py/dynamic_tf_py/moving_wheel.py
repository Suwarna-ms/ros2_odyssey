import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

# Helper function: Converts Roll/Pitch/Yaw into Quaternions
def euler_to_quaternion(roll, pitch, yaw):
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

class DynamicWheelBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_wheel_broadcaster')
        
        # 1. Create a Dynamic Broadcaster (Notice it's NOT Static)
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # 2. A variable to keep track of the wheel's rotation angle
        self.wheel_angle = 0.0 
        
        # 3. A timer that updates the wheel 30 times a second!
        self.timer = self.create_timer(0.033, self.broadcast_timer_callback)

    def broadcast_timer_callback(self):
        t = TransformStamped()

        # Setup the frames
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'wheel_link'

        # Position the wheel 20cm to the left (y-axis)
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.2
        t.transform.translation.z = 0.0

        # Increase the angle so it spins!
        self.wheel_angle += 0.05 

        # Convert the spinning yaw angle to a Quaternion
        q = euler_to_quaternion(0, 0, self.wheel_angle)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Send the moving frame
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = DynamicWheelBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

