# 🚀 ROS2 Odyssey: Autonomous Rover Architecture

![ROS2 Badge](https://img.shields.io/badge/ROS2-Humble-22314E?style=for-the-badge&logo=ros)
![Ubuntu Badge](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=ubuntu)
![Python Badge](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python)
![C++ Badge](https://img.shields.io/badge/C++-17-00599C?style=for-the-badge&logo=c%2B%2B)

**Author:** SUWI | **Status:** Active Deployment

## 📌 Executive Summary
This repository contains the complete software stack for an autonomous, differential-drive rover built from scratch. Designed during a 40-Day Engineering Sprint, the system features custom Gazebo physics modeling, `slam_toolbox` mapping, `AMCL` localization, and a fully integrated `Nav2` stack for dynamic obstacle avoidance. 

## 🏗️ System Architecture X-Ray
Below is the live `rqt_graph` demonstrating the data flow between the physics engine, the AMCL particle swarm, and the Nav2 controllers.

![System Architecture](rover_architecture.png)

## 🧠 Core Engineering Features
- [x] **Custom URDF/Xacro Design:** Fully articulated robot model with Gazebo physics plugins for differential drive and Lidar sensors.
- [x] **Autonomous Navigation:** `nav2_bringup` integration utilizing Global/Local Costmaps and Behavior Tree recovery instincts (Spin/Backup).
- [x] **Smart Dispatch System:** Custom Python Action Clients for automated "Room-to-Room" delivery tasks.
- [x] **Industrial Deployment:** Single-command boot using nested `.launch.py` master files.
- [x] **Containerization:** `Dockerfile` configured for universal system deployment.
- [x] **CI/CD Pipeline:** Automated GitHub Actions testing colcon builds on Ubuntu 22.04 servers.

## ⚙️ Package Breakdown
* `rover_description`: Robot physics, meshes, and URDF generation.
* `rover_bringup`: Master launch files (`master_bringup.launch.py`, `master_mapping.launch.py`).
* `rover_actions`: C++ Action Servers for complex robot behaviors.
* `dynamic_tf_py`: Broadcasting live coordinate frames.

## 🛠️ Quick Start Guide
```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ros2_odyssey.git

# 2. Build the workspace
cd ros2_odyssey
colcon build

# 3. Launch the complete autonomous stack
source install/setup.bash
ros2 launch rover_bringup master_bringup.launch.py

