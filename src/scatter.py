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
    """Create a UI Class"""

    def __init__(self):
        """Constructor"""
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool Window")
        self.setFixedWidth(470)
        self.setFixedHeight(520)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatterT = Scatter()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setStyleSheet("font: Bold 40px")

        self.scatter_scl_lbl = QtWidgets.QLabel("Scatter Scale")
        self.scatter_scl_lbl.setStyleSheet("font: Bold 20px")
        self.scatter_note_scl_lbl = QtWidgets.QLabel(
            "Set min/max value from 0 to 5.0 for randomize rotation")
        self.scatter_note_scl_lbl.setStyleSheet("font: Bold 12px")

        self.scatter_rot_lbl = QtWidgets.QLabel("Scatter Rotation Offset")
        self.scatter_rot_lbl.setStyleSheet("font: Bold 20px")
        self.scatter_note_rot_lbl = QtWidgets.QLabel(
            "Set min/max value from 0 to 360 for randomize rotation")
        self.scatter_note_rot_lbl.setStyleSheet("font: Bold 12px")

        self.sct_cnl_lay = self.cancel_lay_ui()
        self.rnd_rotation_lay = self.randomize_rotate_ui()
        self.rnd_scale_lay = self.randomize_scale_ui()
        self.main_layout_ui()

    def main_layout_ui(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)

        self.main_lay.addWidget(self.scatter_scl_lbl)
        self.main_lay.addWidget(self.scatter_note_scl_lbl)
        self.main_lay.addLayout(self.rnd_scale_lay)

        self.main_lay.addWidget(self.scatter_rot_lbl)
        self.main_lay.addWidget(self.scatter_note_rot_lbl)
        self.main_lay.addLayout(self.rnd_rotation_lay)

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

    def scatter_scl_connections(self):
        self.min_x_scl_sbx.valueChanged.connect(self.update_scl_min_x)
        self.min_y_scl_sbx.valueChanged.connect(self.update_scl_min_y)
        self.min_z_scl_sbx.valueChanged.connect(self.update_scl_min_z)
        self.max_x_scl_sbx.valueChanged.connect(self.update_scl_max_x)
        self.max_y_scl_sbx.valueChanged.connect(self.update_scl_max_y)
        self.max_z_scl_sbx.valueChanged.connect(self.update_scl_max_z)

    def scatter_rot_connections(self):
        self.min_x_rot_sbx.valueChanged.connect(self.update_rot_min_x)
        self.min_y_rot_sbx.valueChanged.connect(self.update_rot_min_y)
        self.min_z_rot_sbx.valueChanged.connect(self.update_rot_min_z)
        self.max_x_rot_sbx.valueChanged.connect(self.update_rot_max_x)
        self.max_y_rot_sbx.valueChanged.connect(self.update_rot_max_y)
        self.max_z_rot_sbx.valueChanged.connect(self.update_rot_max_z)

    def update_rot_min_x(self):
        self.scatterT.rot_min_x = self.min_x_rot_sbx.value()

    def update_rot_min_y(self):
        self.scatterT.rot_min_y = self.min_y_rot_sbx.value()

    def update_rot_min_z(self):
        self.scatterT.rot_min_z = self.min_z_rot_sbx.value()

    def update_rot_max_x(self):
        self.scatterT.rot_max_x = self.max_x_rot_sbx.value()

    def update_rot_max_y(self):
        self.scatterT.rot_max_y = self.max_y_rot_sbx.value()

    def update_rot_max_z(self):
        self.scatterT.rot_max_z = self.max_z_rot_sbx.value()

    def update_scl_min_x(self):
        self.scatterT.scl_min_x = self.min_x_scl_sbx.value()

    def update_scl_min_y(self):
        self.scatterT.scl_min_y = self.min_y_scl_sbx.value()

    def update_scl_min_z(self):
        self.scatterT.scl_min_z = self.min_z_scl_sbx.value()

    def update_scl_max_x(self):
        self.scatterT.scl_max_x = self.max_x_scl_sbx.value()

    def update_scl_max_y(self):
        self.scatterT.scl_max_y = self.max_y_scl_sbx.value()

    def update_scl_max_z(self):
        self.scatterT.scl_max_z = self.max_z_scl_sbx.value()

    @QtCore.Slot()
    def scatter_object(self):
        self.scatterT.scatter_obj()

    @QtCore.Slot()
    def scatter_rotate_object(self):
        self.scatterT.scatter_rotate_obj()

    @QtCore.Slot()
    def scatter_scale_object(self):
        self.scatterT.scatter_scale_obj()

    @QtCore.Slot()
    def cancel(self):
        """Quits the window"""
        self.close()

    def cancel_lay_ui(self):
        """scatter and cancel layout"""
        self.scatter_btn = QtWidgets.QPushButton("Scatter Object")
        self.scatter_btn.setStyleSheet("font: Bold 15px")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("font: Bold 13px")
        self.scatter_btn.setFixedHeight(40)
        self.cancel_btn.setFixedHeight(40)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_btn, 0, 0)
        layout.addWidget(self.cancel_btn, 0, 1)
        return layout

    def randomize_rotate_ui(self):
        """Random rotation layout"""
        self.rot_btn = QtWidgets.QPushButton("Randomize Rotation Offset")
        self.rot_btn.setStyleSheet("font: Bold 15px")
        self.rot_btn.setMinimumHeight(50)
        self.rotate_x()
        self.rotate_y()
        self.rotate_z()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.rot_btn, 1, 0)

        layout.addWidget(self.rotX_lbl, 0, 1)
        layout.addWidget(self.min_x_rot_sbx, 0, 2)
        layout.addWidget(self.x_rot_space, 0, 3)
        layout.addWidget(self.max_x_rot_sbx, 0, 4)

        layout.addWidget(self.rotY_lbl, 1, 1)
        layout.addWidget(self.min_y_rot_sbx, 1, 2)
        layout.addWidget(self.y_rot_space, 1, 3)
        layout.addWidget(self.max_y_rot_sbx, 1, 4)

        layout.addWidget(self.rotZ_lbl, 2, 1)
        layout.addWidget(self.min_z_rot_sbx, 2, 2)
        layout.addWidget(self.z_rot_space, 2, 3)
        layout.addWidget(self.max_z_rot_sbx, 2, 4)
        return layout

    def rotate_x(self):
        self.min_x_rot_sbx = QtWidgets.QSpinBox()
        self.min_x_rot_sbx.setMaximum(360)
        self.min_x_rot_sbx.setSingleStep(5)
        self.min_x_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_x_rot_sbx.setFixedWidth(60)
        self.min_x_rot_sbx.setFixedHeight(25)
        self.min_x_rot_sbx.setValue(self.scatterT.rot_min_x)

        self.rotX_lbl = QtWidgets.QLabel("X")
        self.rotX_lbl.setFixedWidth(15)
        self.rotX_lbl.setIndent(9)
        self.x_rot_space = QtWidgets.QLabel("-")
        self.x_rot_space.setFixedWidth(10)
        self.x_rot_space.setStyleSheet("font: 20px")

        self.max_x_rot_sbx = QtWidgets.QSpinBox()
        self.max_x_rot_sbx.setMaximum(360)
        self.max_x_rot_sbx.setSingleStep(5)
        self.max_x_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_x_rot_sbx.setFixedWidth(60)
        self.max_x_rot_sbx.setFixedHeight(25)
        self.max_x_rot_sbx.setValue(self.scatterT.rot_max_x)

    def rotate_y(self):
        self.min_y_rot_sbx = QtWidgets.QSpinBox()
        self.min_y_rot_sbx.setMaximum(360)
        self.min_y_rot_sbx.setSingleStep(5)
        self.min_y_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_y_rot_sbx.setFixedWidth(60)
        self.min_y_rot_sbx.setFixedHeight(25)
        self.min_y_rot_sbx.setValue(self.scatterT.rot_min_y)

        self.rotY_lbl = QtWidgets.QLabel("Y")
        self.rotY_lbl.setFixedWidth(15)
        self.rotY_lbl.setIndent(9)
        self.y_rot_space = QtWidgets.QLabel("-")
        self.y_rot_space.setFixedWidth(10)
        self.y_rot_space.setStyleSheet("font: 20px")

        self.max_y_rot_sbx = QtWidgets.QSpinBox()
        self.max_y_rot_sbx.setMaximum(360)
        self.max_y_rot_sbx.setSingleStep(5)
        self.max_y_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_y_rot_sbx.setFixedWidth(60)
        self.max_y_rot_sbx.setFixedHeight(25)
        self.max_y_rot_sbx.setValue(self.scatterT.rot_max_y)

    def rotate_z(self):
        self.min_z_rot_sbx = QtWidgets.QSpinBox()
        self.min_z_rot_sbx.setMaximum(360)
        self.min_z_rot_sbx.setSingleStep(5)
        self.min_z_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_z_rot_sbx.setFixedWidth(60)
        self.min_z_rot_sbx.setFixedHeight(25)
        self.min_z_rot_sbx.setValue(self.scatterT.rot_min_z)

        self.rotZ_lbl = QtWidgets.QLabel("Z")
        self.rotZ_lbl.setFixedWidth(15)
        self.rotZ_lbl.setIndent(9)
        self.z_rot_space = QtWidgets.QLabel("-")
        self.z_rot_space.setFixedWidth(10)
        self.z_rot_space.setStyleSheet("font: 20px")

        self.max_z_rot_sbx = QtWidgets.QSpinBox()
        self.max_z_rot_sbx.setMaximum(360)
        self.max_z_rot_sbx.setSingleStep(5)
        self.max_z_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_z_rot_sbx.setFixedWidth(60)
        self.max_z_rot_sbx.setFixedHeight(25)
        self.max_z_rot_sbx.setValue(self.scatterT.rot_max_z)

    def randomize_scale_ui(self):
        """random scale layout"""
        self.scl_btn = QtWidgets.QPushButton("Randomize Scale")
        self.scl_btn.setStyleSheet("font: Bold 15px")
        self.scl_btn.setMinimumHeight(50)
        self.scale_x()
        self.scale_y()
        self.scale_z()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scl_btn, 1, 0)

        layout.addWidget(self.sclX_lbl, 0, 1)
        layout.addWidget(self.min_x_scl_sbx, 0, 2)
        layout.addWidget(self.x_scl_space, 0, 3)
        layout.addWidget(self.max_x_scl_sbx, 0, 4)

        layout.addWidget(self.sclY_lbl, 1, 1)
        layout.addWidget(self.min_y_scl_sbx, 1, 2)
        layout.addWidget(self.y_scl_space, 1, 3)
        layout.addWidget(self.max_y_scl_sbx, 1, 4)

        layout.addWidget(self.sclZ_lbl, 2, 1)
        layout.addWidget(self.min_z_scl_sbx, 2, 2)
        layout.addWidget(self.z_scl_space, 2, 3)
        layout.addWidget(self.max_z_scl_sbx, 2, 4)
        return layout

    def scale_x(self):
        self.min_x_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.min_x_scl_sbx.setDecimals(1)
        self.min_x_scl_sbx.setSingleStep(.1)
        self.min_x_scl_sbx.setMaximum(5)
        self.min_x_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_x_scl_sbx.setFixedWidth(60)
        self.min_x_scl_sbx.setFixedHeight(25)
        self.min_x_scl_sbx.setValue(self.scatterT.scl_min_x)

        self.sclX_lbl = QtWidgets.QLabel("X")
        self.sclX_lbl.setFixedWidth(15)
        self.sclX_lbl.setIndent(9)
        self.x_scl_space = QtWidgets.QLabel("-")
        self.x_scl_space.setFixedWidth(10)
        self.x_scl_space.setStyleSheet("font: 20px")

        self.max_x_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.max_x_scl_sbx.setDecimals(1)
        self.max_x_scl_sbx.setSingleStep(.1)
        self.max_x_scl_sbx.setMaximum(5)
        self.max_x_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_x_scl_sbx.setFixedWidth(60)
        self.max_x_scl_sbx.setFixedHeight(25)
        self.max_x_scl_sbx.setValue(self.scatterT.scl_max_x)

    def scale_y(self):
        self.min_y_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.min_y_scl_sbx.setDecimals(1)
        self.min_y_scl_sbx.setSingleStep(.1)
        self.min_y_scl_sbx.setMaximum(5)
        self.min_y_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_y_scl_sbx.setFixedWidth(60)
        self.min_y_scl_sbx.setFixedHeight(25)
        self.min_y_scl_sbx.setValue(self.scatterT.scl_min_y)

        self.sclY_lbl = QtWidgets.QLabel("Y")
        self.sclY_lbl.setFixedWidth(15)
        self.sclY_lbl.setIndent(9)
        self.y_scl_space = QtWidgets.QLabel("-")
        self.y_scl_space.setFixedWidth(10)
        self.y_scl_space.setStyleSheet("font: 20px")

        self.max_y_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.max_y_scl_sbx.setDecimals(1)
        self.max_y_scl_sbx.setSingleStep(.1)
        self.max_y_scl_sbx.setMaximum(5)
        self.max_y_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_y_scl_sbx.setFixedWidth(60)
        self.max_y_scl_sbx.setFixedHeight(25)
        self.max_y_scl_sbx.setValue(self.scatterT.scl_max_y)

    def scale_z(self):
        self.min_z_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.min_z_scl_sbx.setDecimals(1)
        self.min_z_scl_sbx.setSingleStep(.1)
        self.min_z_scl_sbx.setMaximum(5)
        self.min_z_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_z_scl_sbx.setFixedWidth(60)
        self.min_z_scl_sbx.setFixedHeight(25)
        self.min_z_scl_sbx.setValue(self.scatterT.scl_min_z)

        self.sclZ_lbl = QtWidgets.QLabel("Z")
        self.sclZ_lbl.setFixedWidth(15)
        self.sclZ_lbl.setIndent(9)
        self.z_scl_space = QtWidgets.QLabel("-")
        self.z_scl_space.setFixedWidth(10)
        self.z_scl_space.setStyleSheet("font: 20px")

        self.max_z_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.max_z_scl_sbx.setDecimals(1)
        self.max_z_scl_sbx.setSingleStep(.1)
        self.max_z_scl_sbx.setMaximum(5)
        self.max_z_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_z_scl_sbx.setFixedWidth(60)
        self.max_z_scl_sbx.setFixedHeight(25)
        self.max_z_scl_sbx.setValue(self.scatterT.scl_max_z)


class Scatter(object):

    def __init__(self):
        self.rot_min_x = 0
        self.rot_min_y = 0
        self.rot_min_z = 0

        self.rot_max_x = 360
        self.rot_max_y = 360
        self.rot_max_z = 360

        self.scl_min_x = 0
        self.scl_min_y = 0
        self.scl_min_z = 0

        self.scl_max_x = 5
        self.scl_max_y = 5
        self.scl_max_z = 5

    def scatter_obj(self):
        """scatter the selected object"""
        vert_list = cmds.ls(selection=True, fl=True)
        scatter_grp = cmds.group(n='scatter_grp', a=False)
        object_to_instance = vert_list[0]
        if cmds.objectType(object_to_instance) == 'transform':
            for vert in vert_list:
                vertex_pos = cmds.xform(vert, q=True, ws=True, t=True)
                new_instance = cmds.instance(object_to_instance, n='obj_inst')
                cmds.move(vertex_pos[0], vertex_pos[1], vertex_pos[2],
                          new_instance)
        cmds.delete(vert_list[0])

    def scatter_rotate_obj(self):
        """Scatter the object with randomize rotation offset"""
        obj_list = cmds.ls('obj_inst*', dag=1)
        for obj in obj_list:
            rand_rot_x = random.uniform(self.rot_min_x,
                                        self.rot_max_x)
            rand_rot_y = random.uniform(self.rot_min_y,
                                        self.rot_max_y)
            rand_rot_z = random.uniform(self.rot_min_z,
                                        self.rot_max_z)
            cmds.rotate(rand_rot_x,
                        rand_rot_y,
                        rand_rot_z,
                        obj, relative=True, objectSpace=True, ocp=True)

    def scatter_scale_obj(self):
        """Scatter the object with randomize scale"""
        obj_list = cmds.ls('obj_inst*', fl=True, dag=1)
        for obj in obj_list:
            rand_scl_x = random.uniform(self.scl_min_x,
                                        self.scl_max_x)
            rand_scl_y = random.uniform(self.scl_min_y,
                                        self.scl_max_y)
            rand_scl_z = random.uniform(self.scl_min_z,
                                        self.scl_max_z)
            cmds.scale(rand_scl_x,
                       rand_scl_y,
                       rand_scl_z,
                       obj, relative=True)
