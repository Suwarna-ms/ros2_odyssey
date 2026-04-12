# 1. Base the container on the official ROS2 Humble image
FROM osrf/ros:humble-desktop

# 2. Tell the container to use Bash instead of standard shell
SHELL ["/bin/bash", "-c"]

# 3. Create a workspace folder INSIDE the virtual container
RUN mkdir -p /ros2_ws/src
WORKDIR /ros2_ws

# 4. Copy your code from your laptop into the container's src folder
COPY src/ /ros2_ws/src/

# 5. Install system dependencies that your packages need
RUN apt-get update && apt-get install -y \
    python3-pip \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    && rm -rf /var/lib/apt/lists/*

# 6. Build the code inside the container
RUN source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install

# 7. Create a startup script so the robot boots the moment the container turns on
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

# 8. Set the default command when the container boots
CMD ["bash", "-c", "source /opt/ros/humble/setup.bash && source /ros2_ws/install/setup.bash && ros2 launch rover_bringup master_bringup.launch.py"]
