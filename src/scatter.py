import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import random
from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Simple UI Class"""

    def __init__(self):
        """Constructor"""
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool Window")
        self.setFixedWidth(450)
        self.setFixedHeight(475)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setStyleSheet("font: Bold 40px")
        self.scatter_rot_lbl = QtWidgets.QLabel("Scatter Rotation Offset")
        self.scatter_rot_lbl.setStyleSheet("font: Bold 20px")
        self.scatter_scl_lbl = QtWidgets.QLabel("Scatter Scale")
        self.scatter_scl_lbl.setStyleSheet("font: Bold 20px")
        self.sct_cnl_lay = self.cancel_lay_ui()
        self.rnd_rotation_lay = self.randomize_rotate_ui()
        self.rnd_scale_lay = self.randomize_scale_ui()
        self.main_layout_ui()

    def main_layout_ui(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addWidget(self.scatter_rot_lbl)
        self.main_lay.addLayout(self.rnd_rotation_lay)
        self.main_lay.addWidget(self.scatter_scl_lbl)
        self.main_lay.addLayout(self.rnd_scale_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.sct_cnl_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self.scatter_object)
        self.cancel_btn.clicked.connect(self.cancel)
        self.rot_btn.clicked.connect(self.scatter_rotate_object)
        self.scatter_rot_connections()
        self.scl_btn.clicked.connect(self.scatter_scale_object)
        self.scatter_scl_connections()
