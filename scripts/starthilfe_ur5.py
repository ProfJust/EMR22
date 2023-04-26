#!/usr/bin/env python3
# -- starthilfe_ur5.py --
# GUI to control all the Launch Files etc. in the emr22 course
# edited WHS, OJ , 21.2.2022 #

from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,  QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # --- roscore ---
        self.myPb_roscore = QPushButton(self)
        self.myPb_roscore.setText('1 - Starte ROS-Master')
        self.myPb_roscore.setGeometry(220, 50, 200, 40)  # x,y,w,h
        self.myPb_roscore.clicked.connect(self.slot_roscore)

        # --- QLabel ---
        self.lbl_Left = QLabel(self)
        self.lbl_Left.setAlignment(Qt.AlignCenter)
        self.lbl_Left.setFont(QFont('Sanserif', 12))
        self.lbl_Left.setText("UR5 ohne Alles")
        self.lbl_Left.setGeometry(10, 10, 200, 40)  # x,y,w,h

        # --- QLabel ---
        self.lbl_Mid = QLabel(self)
        self.lbl_Mid.setAlignment(Qt.AlignCenter)
        self.lbl_Mid.setFont(QFont('Sanserif', 12))
        self.lbl_Mid.setText("UR5 & MoveIt!")
        self.lbl_Mid.setGeometry(220, 10, 200, 40)  # x,y,w,h

        # --- QLabel ---
        self.lbl_Right = QLabel(self)
        self.lbl_Right.setAlignment(Qt.AlignCenter)
        self.lbl_Right.setFont(QFont('Sanserif', 12))
        self.lbl_Right.setText("mit Gripper und MoveIt!")
        self.lbl_Right.setGeometry(430, 10, 200, 40)  # x,y,w,h

        # --- roslaunch emr22 ur5_gazebo_bringup.launch---
        self.myPb_gazebo_ur5 = QPushButton(self)
        self.myPb_gazebo_ur5.setText('2a - UR5 in Gazebo')
        self.myPb_gazebo_ur5.setGeometry(10, 90, 200, 40)  # x,y,w,h
        self.myPb_gazebo_ur5.clicked.connect(self.slot_ur5_gazebo)

        # --- roslaunch ---
        self.myPb_gazebo_ur5 = QPushButton(self)
        self.myPb_gazebo_ur5.setText('2b- First MoveIt!')
        self.myPb_gazebo_ur5.setGeometry(220, 90, 200, 40)  # x,y,w,h
        self.myPb_gazebo_ur5.clicked.connect(self.slot_ur5_moveit)

        # --- roslaunch ---
        self.myPb_gazebo_ur5 = QPushButton(self)
        self.myPb_gazebo_ur5.setText('2c- Pick + Place')
        self.myPb_gazebo_ur5.setGeometry(430, 90, 200, 40)  # x,y,w,h
        self.myPb_gazebo_ur5.clicked.connect(self.slot_ur5_grip_moveit)

        # --- Pick and Place Script ---
        self.myPb_pick_place = QPushButton(self)
        self.myPb_pick_place.setText('3b- Py API - Test')
        self.myPb_pick_place.setGeometry(220, 130, 200, 40)  # x,y,w,h
        self.myPb_pick_place.clicked.connect(self.slot_pick_place)

        # --- Pick and Place Script ---
        self.myPb_pick_place = QPushButton(self)
        self.myPb_pick_place.setText('3c- Pick + Place Collisison')
        self.myPb_pick_place.setGeometry(430, 130, 200, 40)  # x,y,w,h
        self.myPb_pick_place.clicked.connect(self.slot_pick_place_collision)

        self.myPb_depth = QPushButton(self)
        self.myPb_depth.setText('4c- mit Depth-Cam')
        self.myPb_depth.setGeometry(430, 170, 200, 40)  # x,y,w,h
        self.myPb_depth.clicked.connect(self.slot_ur5_depth)

        """
        # --- Pick and Place Script ---
        self.myPb_pick_place_dc = QPushButton(self)
        self.myPb_pick_place_dc.setText('C++ PickPlace Blaue Box mit DepthCam')
        self.myPb_pick_place_dc.setGeometry(10, 170, 300, 40)  # x,y,w,h
        self.myPb_pick_place_dc.clicked.connect(self.slot_pick_place_depth_cam)

        # --- find_object_2D ---
        self.myPb_find_object_2D = QPushButton(self)
        self.myPb_find_object_2D.setText('find_object_2D - gazebo')
        self.myPb_find_object_2D.setGeometry(10, 210, 300, 40)  # x,y,w,h
        self.myPb_find_object_2D.clicked.connect(self.slot_find_object_2D)

        # --- find_object_2D und Astra---
        self.myPb_astra = QPushButton(self)
        self.myPb_astra.setText(' Astra Orbbec und find_object_2D - real')
        self.myPb_astra.setGeometry(10, 250, 300, 40)  # x,y,w,h
        self.myPb_astra.clicked.connect(self.slot_astra_cam)
        """

        # --- Window konfigurieren und starten
        self.setGeometry(300, 300, 650, 300)
        self.setWindowTitle('EMR22  - G A Z E B O -  Starthilfe UR5 ')
        self.show()

    # --- Die  Slot-Methoden ---
    def slot_roscore(self):
        os.system('gnome-terminal -- bash -c "roscore; exec bash"')

    def slot_ur5_gazebo(self):
        os.system('gnome-terminal -- bash -c "roslaunch emr22 ur5_gazebo_bringup.launch; exec bash"')

    def slot_ur5_moveit(self):
        os.system('gnome-terminal -- bash -c "roslaunch emr22 ur5_gazebo_moveIt_bringup.launch; exec bash"')

    def slot_ur5_grip_moveit(self):
        os.system('gnome-terminal -- bash -c "roslaunch ur5_gripper_moveit_config demo_gazebo_pick_and_place.launch; exec bash"')

    def slot_pick_place(self):
        os.system('gnome-terminal -- bash -c "rosrun emr22 move_group_api_test.py; exec bash"')

    def slot_pick_place_collision(self):
        os.system('gnome-terminal -- bash -c "roslaunch ur5_gripper_moveit_config demo_gazebo_pick_and_place_collision.launch; exec bash"')

    def slot_ur5_depth(self):
        os.system('gnome-terminal -- bash -c "roslaunch ur5_gripper_moveit_config demo_gazebo_pick_and_place_depth.launch; exec bash"')

    """
    def slot_pick_place_depth_cam(self):
        # os.system('gnome-terminal -- bash -c "rosrun emr22 pick_and_place_collision_depth_cam.py; exec bash"')
        os.system('gnome-terminal -- bash -c "rosrun emr22 adaim_pick_place_depth; exec bash"')

    def slot_find_object_2D(self):
        os.system('gnome-terminal -- bash -c "roslaunch emr22 find_object_2d.launch"')

    def slot_astra_cam(self):
        os.system('gnome-terminal -- bash -c "roslaunch emr22 astra_find_object_2d.launch"')
    """


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
