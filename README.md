# mujoco-voxel

This repo holds a robotic arm implementation of the PerAct behavorial learning technique runnning on MuJoCo. The detail of PerAct can be found in the following repository [Perceiver-Actor](https://github.com/peract/peract). 

The robot model can perform a specific task based on the user language command (open drawers, pick up objects,...)

In this project, the 3D presentation of the robot scene is converted into a [Voxel](https://en.wikipedia.org/wiki/Voxel) presentation, before the voxels are fed into the PerAct model. The model predicts the next actions for the robot to complete the commanded task.
