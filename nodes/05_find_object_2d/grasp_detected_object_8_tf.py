#!/usr/bin/env python3
# grasp_detected_object_tf.py
# 
# ------------------------------------
# edited WHS, OJ , 20.6.2022 #
# -------------------------------------
# Pick and Place für den realen UR3
# in Python mit der move_group_api
# und Kollsionsverhütung mit der Realsense 3D-Kamera
# -----------------------------------------
#
# http://docs.ros.org/en/jade/api/moveit_ros_planning_interface/html/classmoveit_1_1planning__interface_1_1MoveGroup.html
# -----------------------------------------
# usage
#   ...
# ----------------------------------------------------------------
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import numpy as np  # für deg2rad
from math import pi
import tf

def wait_for_state_update(box_name, scene, box_is_known=False,
                          box_is_attached=False, timeout=4):
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
        attached_objects = scene.get_attached_objects([box_name])
        is_attached = len(attached_objects.keys()) > 0
        is_known = box_name in scene.get_known_object_names()
        if (box_is_attached == is_attached) and (box_is_known == is_known):
            return True
        rospy.sleep(0.1)
        seconds = rospy.get_time()
    return False


# First initialize moveit_ Command and rospy nodes:
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)
# Instantiate the robot commander object,
# which is used to control the whole robot
robot = moveit_commander.RobotCommander()

# Instantiate the MoveGroupCommander object.
group_name = "ur3_arm"
group = moveit_commander.MoveGroupCommander(group_name)
group_name_gripper = "gripper"
group_gripper = moveit_commander.MoveGroupCommander(group_name_gripper)

# Create a Publisher
display_trajectory_publisher = rospy.Publisher(
    '/move_group/display_planned_path',
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20)

# create tf-listener
listener = tf.TransformListener()

# ##### Getting Basic Information ###############
# We can get the name of the reference frame for this robot:
planning_frame = group.get_planning_frame()
# print("= Reference frame: %s" % planning_frame)

# We can also print the name of the end-effector link for this group:
eef_link = group.get_end_effector_link()
print("= End effector: %s" % eef_link)

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()

# ---- 1. Move to home position ----
input("confirm moving ur3_arm to home position")
joint_goal = group.get_named_target_values("home")
group.go(joint_goal, wait=True)

# --- 2. get the pose of object_X  from Camera
print("looking for object_8 ==>")
(trans, rot) = listener.lookupTransform('/world', '/object_8', rospy.Time())
print("detected object position")
print(trans)

# --- 3. Object in Scene eintragen
# Desktop Plate is not needed because of Depth Cam, Yes!
# But Gripper does not go to Desktop then =>
# Add the object to the planning scene and deactivate collision checking
print("=== Adding object to Planning Scene  ===")
scene = moveit_commander.PlanningSceneInterface()
rospy.sleep(1.0)  # Wichtig! ohne Pause funkts nicht
box_pose = geometry_msgs.msg.PoseStamped()
box_pose.header.frame_id = robot.get_planning_frame()
box_pose.pose.orientation.w = 1.0
box_pose.pose.position.x = trans[0]
box_pose.pose.position.y = trans[1]
box_pose.pose.position.z = trans[2]
box_name = "object"
scene.add_box(box_name, box_pose, size=(0.08, 0.08, 0.1))
rospy.loginfo(wait_for_state_update(box_name, scene, box_is_known=True))

# --- 4. go to object position
# rosrun tf tf_echo world robotiq_85_left_finger_link
# trans = [0.36, 0.08, 0.3]  # Test Position
print("translation is ", trans)
pose_goal = group.get_current_pose()
pose_goal.pose.position.x = trans[0] - 0.04  # from tf-Tree
pose_goal.pose.position.y = trans[1] - 0.02  # from tf-Tree
pose_goal.pose.position.z = trans[2]  # from tf-Tree
pose_goal.pose.position.z = 0.35  # 35cm high

# pose_goal.orientation = [1.0, 1.0, 1.0, 1.0 ] # quaternion
# Drehwinkel um den Vektor ist w => w = 7101 =>  pi/4 = 0.7853..
print(" going to pose", pose_goal.pose.position)
print(" going to orientation quaternion ", pose_goal.pose.orientation)
# pose_goal.pose.orientation.w = 0
quaternion = (
    pose_goal.pose.orientation.x,
    pose_goal.pose.orientation.y,
    pose_goal.pose.orientation.z,
    pose_goal.pose.orientation.w)
euler_goal_pose_orientation = tf.transformations.euler_from_quaternion(quaternion) 
print(" going to orientation euler", euler_goal_pose_orientation)

quaternion = tf.transformations.quaternion_from_euler(
    euler_goal_pose_orientation[0],
    euler_goal_pose_orientation[1],
    euler_goal_pose_orientation[2] + pi/4,
    axes='sxyz'  )

euler_goal_pose_orientation = tf.transformations.euler_from_quaternion(quaternion) 
print(" going to orientation euler neu", euler_goal_pose_orientation)

# WICHTIG!
pose_goal.pose.orientation.x = quaternion[0]
pose_goal.pose.orientation.y = quaternion[1]
pose_goal.pose.orientation.z = quaternion[2]
pose_goal.pose.orientation.w = quaternion[3]


input("confirm moving ur3_arm to this position")
group.set_pose_target(pose_goal)
plan = group.plan()
sucess = group.go(wait=True)
print("suc?", sucess)
group.stop()
group.clear_pose_targets()

# --- 5. turning gripper  - alleine Gelenkwinkel funkt nicht !!!
# input("confirm turning wrist3")
# joint_goal = group.get_current_joint_values()
# joint_goal[5] = np.deg2rad(0)  # turn wrist3
# group.go(joint_goal, wait=True)

# --- 6. go to grip position
print("plan a cartesion path")
waypoints = []
wpose = group.get_current_pose().pose
wpose.position.z -= 0.10  # move down (z)
waypoints.append(copy.deepcopy(wpose))
(plan, fraction) = group.compute_cartesian_path(
                                                waypoints,
                                                0.001,        # eef_step
                                                0.0)         # jump_threshold
# Displaying a Trajectory in RViZ
display_trajectory = moveit_msgs.msg.DisplayTrajectory()
display_trajectory.trajectory_start = robot.get_current_state()
display_trajectory.trajectory.append(plan)
# Publish
display_trajectory_publisher.publish(display_trajectory)

# Execute the calculated path:
input("confirm moving ur3_arm 10 cm deeper")
group.execute(plan, wait=True)


# --- 7. Gripping
input("Confirm: you have to close the gripper with the UR3-Teach-Pad EA Werkzeugausgang 0 auf OFF")
# für die  Trajektorienplanung das Object an den Gripper attachen
grasping_group = "ur3_arm"
touch_links = robot.get_link_names(group=grasping_group)
print(touch_links)
#  no worxxxxxxxxxxx  
#  scene.attach_box('ee_link', box_name, touch_links=touch_links)


# --- 8. go to home position
input("confirm moving ur3_arm to home position")
joint_goal = group.get_named_target_values("home")
group.go(joint_goal, wait=True)

# --- at the end -----
