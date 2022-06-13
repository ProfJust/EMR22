#!/usr/bin/env python3
# http://wiki.ros.org/tf/Tutorials/Adding%20a%20frame%20%28Python%29
# usage:   $ rosrun tf tf_echo world object_8
# -----------------------------------------------------------------
# Version vom 13.6.22 mit numpy eul2quat

import rospy
import tf
import numpy as np  # Scientific computing library for Python




if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        # Hier Abstand camera_link zum world_frame eintragen
        # vorher messen in Meter
        # x, y, z    67cm hohes Stativ
        # quaternion?

        # UR5e 13_06_22
        br.sendTransform((1.30, 0.04, 0.70),
                         (tf.transformations.quaternion_from_euler(0.0 , 0.5, 3.14)),
                         rospy.Time.now(),
                         "camera_link",
                         "world")

        
        rate.sleep()
