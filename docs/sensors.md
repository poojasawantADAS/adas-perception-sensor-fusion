# Sensors Used in ADAS

## Camera
Cameras provide high-resolution visual information used for detecting lanes,
vehicles, pedestrians, and traffic signs. In this project, camera data is used
as the primary input for perception due to its availability and effectiveness
in object detection tasks.

## Radar
Radar sensors measure distance and relative velocity of objects using radio
waves. They are robust in poor weather conditions but provide lower spatial
resolution compared to cameras.

## LiDAR
LiDAR sensors generate 3D point clouds by measuring the time of flight of laser
pulses. They provide accurate depth information but are expensive and sensitive
to adverse weather conditions.


## Dataset Used
This project uses the KITTI dataset, which provides real-world driving data
including synchronized camera images. The current implementation focuses on
camera-based perception, while radar and LiDAR are discussed conceptually to
explain multi-sensor ADAS systems.
