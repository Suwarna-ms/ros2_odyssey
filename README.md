🚀 ROS2 Odyssey: Autonomous Rover Architecture

ROS2 Distribution: Humble Hawksbill

OS: Ubuntu 22.04 LTS

📌 Project Overview

This repository contains the complete software stack for an autonomous, differential-drive rover built from scratch in ROS2. The system features custom physics modeling, SLAM mapping, AMCL localization, and interactive behavior trees for dynamic obstacle avoidance.

🧠 Core Architecture

This workspace is divided into several custom packages:

rover_description: Contains the custom Xacro/URDF robot model and Gazebo physics plugins.

rover_bringup: Houses the master .launch.py deployment files for one-touch system startup.

rover_actions: Custom C++ Action Servers and Python Action Clients for executing smart behaviors (e.g., dynamic delivery dispatching).

dynamic_tf_py: Broadcasts live coordinate frame transforms.

⚙️ Dependencies

ros-humble-gazebo-ros-pkgs

ros-humble-slam-toolbox

ros-humble-navigation2

ros-humble-nav2-bringup

🛠️ Usage & Deployment

1. Mapping Mode (SLAM)

To explore a new environment and generate a 2D occupancy grid:

colcon build
source install/setup.bash
ros2 launch rover_bringup master_mapping.launch.py


2. Autonomous Delivery Mode (AMCL & Nav2)

To load a saved map and enable dynamic obstacle avoidance:

ros2 launch rover_bringup master_bringup.launch.py


Once booted, use the 2D Pose Estimate tool in RViz to initialize the AMCL particle swarm, then dispatch the robot via the Nav2 Goal tool or custom Python action clients.

Built during a comprehensive 40-Day ROS2 Engineering Sprint.
