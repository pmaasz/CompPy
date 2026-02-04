try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    version = 4

except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    version = 5

import BladePlot
import RenderWindow
from FileOps import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow  # Store reference to MainWindow instance
        MainWindow.setObjectName("CompPy")
        MainWindow.resize(805, 583)

        self.commonVars = []
        self.rotorVars = []
        self.statorVars = []
        
        self.commonValidators = {"RPM" : None, "Loading (Psi)" : None, "Flow (Phi)" : None, "Reaction (R)" : None, "Mean Line Radius" : None}
        self.rotorValidators = {"Y Twist (Rotor)" : None, "X Twist (Rotor)" : None, "Tip Chord (Rotor)" : None, "Rotor Diameter" : None, "Root Chord (Rotor)" : None, "Blade Thickness (Rotor)" : None, "Hub Diameter" : None, "Hub Length" : None, "Blade Clearance" : None, "Num of Blade (Rotor)" : None}
        self.statorValidators = {"Duct ID" : None, "Duct Length" : None, "Duct Thickness" : None, "Num of Blade (Stator)" : None, "Mount Can Length" : None, "Mount Can Dia" : None, "Mount Can Loc" : None, "Blade Thickness (Stator)" : None, "Root Chord (Stator)" : None, "Tip Chord (Stator)" : None, "X Twist (Stator)" : None, "Y Twist (Stator)" : None}
        
        # Valid ranges for each field to provide helpful suggestions
        self.validRanges = {
            "RPM": "1 - 100,000",
            "Loading (Psi)": "0.0 - 1.0",
            "Flow (Phi)": "0.0 - 1.0",
            "Reaction (R)": "0.0 - 1.0",
            "Mean Line Radius": "0.0 - 1000.0 mm",
            "Y Twist (Rotor)": "0.0 - 100.0 degrees",
            "X Twist (Rotor)": "0.0 - 100.0 degrees",
            "Tip Chord (Rotor)": "0.0 - 1000.0 mm",
            "Rotor Diameter": "0.0 - 1000.0 mm",
            "Root Chord (Rotor)": "0.0 - 1000.0 mm",
            "Blade Thickness (Rotor)": "0.0 - 1000.0 mm",
            "Hub Diameter": "0.0 - 10,000.0 mm",
            "Hub Length": "0.0 - 1000.0 mm",
            "Blade Clearance": "0.0 - 10.0 mm",
            "Num of Blade (Rotor)": "1 - 1000",
            "Duct ID": "0.0 - 1000.0 mm",
            "Duct Length": "0.0 - 1000.0 mm",
            "Duct Thickness": "0.0 - 100.0 mm",
            "Num of Blade (Stator)": "1 - 1000",
            "Mount Can Length": "0.0 - 1000.0 mm",
            "Mount Can Dia": "0.0 - 1000.0 mm",
            "Mount Can Loc": "0.0 - 1000.0 mm",
            "Blade Thickness (Stator)": "0.0 - 100.0 mm",
            "Root Chord (Stator)": "0.0 - 1000.0 mm",
            "Tip Chord (Stator)": "0.0 - 1000.0 mm",
            "X Twist (Stator)": "0.0 - 1000.0 degrees",
            "Y Twist (Stator)": "0.0 - 1000.0 degrees"
        }
        
        self.exportObj = None
        self.clicked = None
        self.fileOpen = False
        self.failed = []
        self.darkMode = False
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        

        self.Rotor_Frame = QFrame(self.centralwidget)
        self.Rotor_Frame.setMaximumSize(QSize(375, 16777215))
        self.Rotor_Frame.setFrameShape(QFrame.StyledPanel)
        self.Rotor_Frame.setFrameShadow(QFrame.Raised)
        self.Rotor_Frame.setObjectName("Rotor_Frame")
        
        self.gridLayout_2 = QGridLayout(self.Rotor_Frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.YT_Label = QLabel(self.Rotor_Frame)
        self.YT_Label.setStyleSheet("font: bold")
        self.YT_Label.setObjectName("YT_Label")
        
        self.gridLayout_2.addWidget(self.YT_Label, 11, 2, 1, 1)
        
        self.YT_Line = QLineEdit(self.Rotor_Frame)
        self.YT_Line.setAlignment(Qt.AlignCenter)
        self.YT_Line.setObjectName("Y Twist (Rotor)")
        self.YT_Line.setValidator(QDoubleValidator(0.0, 100.0, 3, self.YT_Line))
        self.YT_Line.textChanged.connect(self.CheckState)
        self.YT_Line.textChanged.emit(self.YT_Line.text())
        
        self.gridLayout_2.addWidget(self.YT_Line, 11, 3, 1, 1)
        
        self.wallCheck = QCheckBox(self.Rotor_Frame)
        self.wallCheck.setStyleSheet("font: bold;")
        self.wallCheck.setObjectName("wallCheck")
        
        self.gridLayout_2.addWidget(self.wallCheck, 12, 0, 1, 1)
        
        self.RDia_Label = QLabel(self.Rotor_Frame)
        self.RDia_Label.setStyleSheet("font: bold")
        self.RDia_Label.setObjectName("RDia_Label")
        
        self.gridLayout_2.addWidget(self.RDia_Label, 2, 0, 1, 1)
        
        self.BT_Label = QLabel(self.Rotor_Frame)
        self.BT_Label.setStyleSheet("font: bold")
        self.BT_Label.setObjectName("BT_Label")
        
        self.gridLayout_2.addWidget(self.BT_Label, 9, 0, 1, 1)
        
        self.R_Title = QLabel(self.Rotor_Frame)
        self.R_Title.setStyleSheet("font-size: 16px; font: bold;")
        self.R_Title.setObjectName("R_Title")
        
        self.gridLayout_2.addWidget(self.R_Title, 0, 0, 1, 2)
        
        self.NB_Label = QLabel(self.Rotor_Frame)
        self.NB_Label.setStyleSheet("font: bold")
        self.NB_Label.setObjectName("NB_Label")
        
        self.gridLayout_2.addWidget(self.NB_Label, 4, 2, 1, 1)
        
        self.RC_Label = QLabel(self.Rotor_Frame)
        self.RC_Label.setStyleSheet("font: bold")
        self.RC_Label.setObjectName("RC_Label")
        
        self.gridLayout_2.addWidget(self.RC_Label, 7, 0, 1, 1)
        
        self.HDia_Label = QLabel(self.Rotor_Frame)
        self.HDia_Label.setStyleSheet("font: bold")
        self.HDia_Label.setObjectName("HDia_Label")
        
        self.gridLayout_2.addWidget(self.HDia_Label, 2, 2, 1, 1)
        
        self.TC_Label = QLabel(self.Rotor_Frame)
        self.TC_Label.setStyleSheet("font: bold")
        self.TC_Label.setObjectName("TC_Label")
        
        self.gridLayout_2.addWidget(self.TC_Label, 7, 2, 1, 1)
        
        self.XT_Line = QLineEdit(self.Rotor_Frame)
        self.XT_Line.setAlignment(Qt.AlignCenter)
        self.XT_Line.setObjectName("X Twist (Rotor)")
        self.XT_Line.setValidator(QDoubleValidator(0.0, 100.0, 3, self.XT_Line))
        self.XT_Line.textChanged.connect(self.CheckState)
        self.XT_Line.textChanged.emit(self.XT_Line.text())
        
        self.gridLayout_2.addWidget(self.XT_Line, 11, 1, 1, 1)
        
        self.TC_Line = QLineEdit(self.Rotor_Frame)
        self.TC_Line.setAlignment(Qt.AlignCenter)
        self.TC_Line.setObjectName("Tip Chord (Rotor)")
        self.TC_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.TC_Line))
        self.TC_Line.textChanged.connect(self.CheckState)
        self.TC_Line.textChanged.emit(self.TC_Line.text())
        
        self.gridLayout_2.addWidget(self.TC_Line, 7, 3, 1, 1)
        
        self.RD_Line = QLineEdit(self.Rotor_Frame)
        self.RD_Line.setAlignment(Qt.AlignCenter)
        self.RD_Line.setObjectName("Rotor Diameter")
        self.RD_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.RD_Line))
        self.RD_Line.textChanged.connect(self.CheckState)
        self.RD_Line.textChanged.emit(self.RD_Line.text())
        
        self.gridLayout_2.addWidget(self.RD_Line, 2, 1, 1, 1)
        
        self.HL_Label = QLabel(self.Rotor_Frame)
        self.HL_Label.setStyleSheet("font: bold")
        self.HL_Label.setObjectName("HL_Label")
        
        self.gridLayout_2.addWidget(self.HL_Label, 4, 0, 1, 1)
        
        self.RC_Line = QLineEdit(self.Rotor_Frame)
        self.RC_Line.setAlignment(Qt.AlignCenter)
        self.RC_Line.setObjectName("Root Chord (Rotor)")
        self.RC_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.RC_Line))
        self.RC_Line.textChanged.connect(self.CheckState)
        self.RC_Line.textChanged.emit(self.RC_Line.text())
        
        self.gridLayout_2.addWidget(self.RC_Line, 7, 1, 1, 1)
        
        self.BT_Line = QLineEdit(self.Rotor_Frame)
        self.BT_Line.setAlignment(Qt.AlignCenter)
        self.BT_Line.setObjectName("Blade Thickness (Rotor)")
        self.BT_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.BT_Line))
        self.BT_Line.textChanged.connect(self.CheckState)
        self.BT_Line.textChanged.emit(self.BT_Line.text())
        
        self.gridLayout_2.addWidget(self.BT_Line, 9, 1, 1, 1)
        
        self.BC_Label = QLabel(self.Rotor_Frame)
        self.BC_Label.setStyleSheet("font: bold")
        self.BC_Label.setObjectName("BC_Label")
        
        self.gridLayout_2.addWidget(self.BC_Label, 9, 2, 1, 1)
        
        self.HD_Line = QLineEdit(self.Rotor_Frame)
        self.HD_Line.setAlignment(Qt.AlignCenter)
        self.HD_Line.setObjectName("Hub Diameter")
        self.HD_Line.setValidator(QDoubleValidator(0.0, 10000.0, 3, self.HD_Line))
        self.HD_Line.textChanged.connect(self.CheckState)
        self.HD_Line.textChanged.emit(self.HD_Line.text())
        
        self.gridLayout_2.addWidget(self.HD_Line, 2, 3, 1, 1)
        
        self.HL_Line = QLineEdit(self.Rotor_Frame)
        self.HL_Line.setAlignment(Qt.AlignCenter)
        self.HL_Line.setObjectName("Hub Length")
        self.HL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.HL_Line))
        self.HL_Line.textChanged.connect(self.CheckState)
        self.HL_Line.textChanged.emit(self.HL_Line.text())
        
        self.gridLayout_2.addWidget(self.HL_Line, 4, 1, 1, 1)
        
        self.BC_Line = QLineEdit(self.Rotor_Frame)
        self.BC_Line.setAlignment(Qt.AlignCenter)
        self.BC_Line.setObjectName("Blade Clearance")
        self.BC_Line.setValidator(QDoubleValidator(0.0, 10.0, 3, self.BC_Line))
        self.BC_Line.textChanged.connect(self.CheckState)
        self.BC_Line.textChanged.emit(self.BC_Line.text())
        
        self.gridLayout_2.addWidget(self.BC_Line, 9, 3, 1, 1)
        
        self.XT_Label = QLabel(self.Rotor_Frame)
        self.XT_Label.setStyleSheet("font: bold")
        self.XT_Label.setObjectName("XT_Label")
        
        self.gridLayout_2.addWidget(self.XT_Label, 11, 0, 1, 1)
        
        self.NB_Line = QLineEdit(self.Rotor_Frame)
        self.NB_Line.setAlignment(Qt.AlignCenter)
        self.NB_Line.setObjectName("Num of Blade (Rotor)")
        self.NB_Line.setValidator(QIntValidator(1, 1000,  self.NB_Line))
        self.NB_Line.textChanged.connect(self.CheckState)
        self.NB_Line.textChanged.emit(self.NB_Line.text())
        
        self.gridLayout_2.addWidget(self.NB_Line, 4, 3, 1, 1)
        
        self.line_2 = QFrame(self.Rotor_Frame)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 4)
        
        self.gridLayout.addWidget(self.Rotor_Frame, 1, 0, 1, 1)
        
        self.Up_Frame = QFrame(self.centralwidget)
        self.Up_Frame.setMaximumSize(QSize(16777215, 400))
        self.Up_Frame.setFrameShape(QFrame.StyledPanel)
        self.Up_Frame.setFrameShadow(QFrame.Raised)
        self.Up_Frame.setObjectName("Up_Frame")
        
        self.horizontalLayout = QHBoxLayout(self.Up_Frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.L_Frame = QFrame(self.Up_Frame)
        self.L_Frame.setMaximumSize(QSize(410, 16777215))
        self.L_Frame.setFrameShape(QFrame.StyledPanel)
        self.L_Frame.setFrameShadow(QFrame.Raised)
        self.L_Frame.setObjectName("L_Frame")
        
        self.gridLayout_4 = QGridLayout(self.L_Frame)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setHorizontalSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
                 
        self.U_Frame = QFrame(self.L_Frame)
        self.U_Frame.setMinimumSize(QSize(200, 0))
        self.U_Frame.setMaximumSize(QSize(200, 200))
        self.U_Frame.setFrameShape(QFrame.StyledPanel)
        self.U_Frame.setFrameShadow(QFrame.Raised)
        self.U_Frame.setObjectName("U_Frame")
        
        self.formLayout = QFormLayout(self.U_Frame)
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.formLayout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        
        self.R_Label = QLabel(self.U_Frame)
        self.R_Label.setStyleSheet("font: bold;")
        self.R_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.R_Label.setObjectName("R_Label")
        
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.R_Label)
        
        self.R_Line = QLineEdit(self.U_Frame)
        self.R_Line.setAlignment(Qt.AlignCenter)
        self.R_Line.setObjectName("Reaction (R)")
        self.R_Line.setValidator(QDoubleValidator(0.0, 1.0, 3, self.R_Line))
        self.R_Line.textChanged.connect(self.CheckState)
        self.R_Line.textChanged.emit(self.R_Line.text())
        
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.R_Line)
        
        self.PSI_Label = QLabel(self.U_Frame)
        self.PSI_Label.setStyleSheet("font: bold;")
        self.PSI_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.PSI_Label.setObjectName("PSI_Label")
        
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.PSI_Label)
        
        self.PSI_Line = QLineEdit(self.U_Frame)
        self.PSI_Line.setAlignment(Qt.AlignCenter)
        self.PSI_Line.setObjectName("Loading (Psi)")
        self.PSI_Line.setValidator(QDoubleValidator(0.0, 1.0, 3, self.PSI_Line))
        self.PSI_Line.textChanged.connect(self.CheckState)
        self.PSI_Line.textChanged.emit(self.PSI_Line.text())
        
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.PSI_Line)
        
        self.PHI_Label = QLabel(self.U_Frame)
        self.PHI_Label.setStyleSheet("font: bold;")
        self.PHI_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.PHI_Label.setObjectName("PHI_Label")
        
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.PHI_Label)
        
        self.PHI_Line = QLineEdit(self.U_Frame)
        self.PHI_Line.setAlignment(Qt.AlignCenter)
        self.PHI_Line.setObjectName("Flow (Phi)")
        self.PHI_Line.setValidator(QDoubleValidator(0.0, 1.0, 3, self.PHI_Line))
        self.PHI_Line.textChanged.connect(self.CheckState)
        self.PHI_Line.textChanged.emit(self.PHI_Line.text())
        
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.PHI_Line)
        
        self.Title = QLabel(self.U_Frame)
        self.Title.setStyleSheet("font-size: 16px; font: bold;")
        self.Title.setAlignment(Qt.AlignCenter)
        self.Title.setObjectName("Title")
        
        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.Title)
        
        self.MLR_Label = QLabel(self.U_Frame)
        self.MLR_Label.setStyleSheet("font: bold;")
        self.MLR_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.MLR_Label.setObjectName("MLR_Label")
        
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.MLR_Label)
        
        self.MLR_Line = QLineEdit(self.U_Frame)
        self.MLR_Line.setAlignment(Qt.AlignCenter)
        self.MLR_Line.setObjectName("Mean Line Radius")
        self.MLR_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.MLR_Line))
        self.MLR_Line.textChanged.connect(self.CheckState)
        self.MLR_Line.textChanged.emit(self.MLR_Line.text())
        
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.MLR_Line)
        
        self.RPM_Label = QLabel(self.U_Frame)
        self.RPM_Label.setStyleSheet("font: bold;")
        self.RPM_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.RPM_Label.setObjectName("RPM_Label")
        
        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.RPM_Label)
        
        self.RPM_Line = QLineEdit(self.U_Frame)
        self.RPM_Line.setAlignment(Qt.AlignCenter)
        self.RPM_Line.setObjectName("RPM")
        self.RPM_Line.setValidator(QIntValidator(1, 100000,  self.RPM_Line))
        self.RPM_Line.textChanged.connect(self.CheckState)
        self.RPM_Line.textChanged.emit(self.RPM_Line.text())
        
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.RPM_Line)
        
        self.line = QFrame(self.U_Frame)
        self.line.setMinimumSize(QSize(200, 0))
        self.line.setMaximumSize(QSize(16777215, 16777215))
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.line)
        
        self.gridLayout_4.addWidget(self.U_Frame, 0, 1, 1, 1)
        
        self.listWidget = QListWidget(self.L_Frame)
        self.listWidget.setMinimumSize(QSize(200, 200))
        self.listWidget.setMaximumSize(QSize(200, 200))
        self.listWidget.setTextElideMode(Qt.ElideMiddle)
        self.listWidget.setObjectName("listWidget")
        
        
        self.listWidget.itemClicked.connect(self.ListClicked)
        
        self.gridLayout_4.addWidget(self.listWidget, 0, 0, 1, 1)
        
        self.renderExport = QPushButton(self.L_Frame)
        self.renderExport.setObjectName("renderExport")
        self.renderExport.clicked.connect(self.Export)
        
        self.gridLayout_4.addWidget(self.renderExport, 3, 1, 1, 1)
        
        self.frame = QFrame(self.L_Frame)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        self.removeButton = QPushButton(self.frame)
        self.removeButton.setObjectName("removeButton")
        self.removeButton.clicked.connect(self.RemoveStage)
        self.gridLayout_5.addWidget(self.removeButton, 0, 1, 1, 1)
        
        self.addButton = QPushButton(self.frame)
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.AddStage)
        self.gridLayout_5.addWidget(self.addButton, 0, 0, 1, 1)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.gridLayout_5.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 1, 0, 2, 1)
        
        self.profileButton = QPushButton(self.L_Frame)
        self.profileButton.setObjectName("profileButton")
        self.profileButton.clicked.connect(self.PlotProfile)
        
        self.renderButton = QPushButton(self.L_Frame)
        self.renderButton.setObjectName("renderButton")
        self.renderButton.clicked.connect(self.Render)
        
       
        self.gridLayout_4.addWidget(self.profileButton, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.renderButton, 2, 1, 1, 1)
        self.horizontalLayout.addWidget(self.L_Frame)
        
        self.R_Frame = QFrame()
        self.R_FrameLayout = QGridLayout(self.R_Frame)
        self.R_Frame.setMinimumSize(QSize(375, 0))
        self.R_Frame.setMaximumSize(QSize(400, 400))
        self.R_Frame.setObjectName("R_Frame")
        
        self.L_Frame.raise_()
        self.L_Frame.raise_()
        
        self.horizontalLayout.addWidget(self.R_Frame)
        
        self.gridLayout.addWidget(self.Up_Frame, 0, 0, 1, 3)
        
        self.Stator_Frame = QFrame(self.centralwidget)
        self.Stator_Frame.setMaximumSize(QSize(375, 200))
        self.Stator_Frame.setFrameShape(QFrame.StyledPanel)
        self.Stator_Frame.setFrameShadow(QFrame.Raised)
        self.Stator_Frame.setObjectName("Stator_Frame")
        
        self.gridLayout_3 = QGridLayout(self.Stator_Frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.DI_Label = QLabel(self.Stator_Frame)
        self.DI_Label.setStyleSheet("font: bold;")
        self.DI_Label.setObjectName("DI_Label")
        
        self.gridLayout_3.addWidget(self.DI_Label, 2, 2, 1, 1)
        
        self.S_Title = QLabel(self.Stator_Frame)
        self.S_Title.setStyleSheet("font-size: 16px; font: bold;")
        self.S_Title.setObjectName("S_Title")
        
        self.gridLayout_3.addWidget(self.S_Title, 0, 0, 1, 4)
        
        self.DI_Line = QLineEdit(self.Stator_Frame)
        self.DI_Line.setAlignment(Qt.AlignCenter)
        self.DI_Line.setObjectName("Duct ID")
        self.DI_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.DI_Line))
        self.DI_Line.textChanged.connect(self.CheckState)
        self.DI_Line.textChanged.emit(self.DI_Line.text())
        
        self.gridLayout_3.addWidget(self.DI_Line, 2, 3, 1, 1)
        
        self.DT_Label = QLabel(self.Stator_Frame)
        self.DT_Label.setStyleSheet("font: bold;")
        self.DT_Label.setObjectName("DT_Label")
        
        self.gridLayout_3.addWidget(self.DT_Label, 3, 0, 1, 1)
        
        self.DL_Label = QLabel(self.Stator_Frame)
        self.DL_Label.setStyleSheet("font: bold;")
        self.DL_Label.setObjectName("DL_Label")
        
        self.gridLayout_3.addWidget(self.DL_Label, 2, 0, 1, 1)
        
        self.DL_Line = QLineEdit(self.Stator_Frame)
        self.DL_Line.setAlignment(Qt.AlignCenter)
        self.DL_Line.setObjectName("Duct Length")
        self.DL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.DL_Line))
        self.DL_Line.textChanged.connect(self.CheckState)
        self.DL_Line.textChanged.emit(self.DL_Line.text())
        
        self.gridLayout_3.addWidget(self.DL_Line, 2, 1, 1, 1)
        
        self.DT_Line = QLineEdit(self.Stator_Frame)
        self.DT_Line.setAlignment(Qt.AlignCenter)
        self.DT_Line.setObjectName("Duct Thickness")
        self.DT_Line.setValidator(QDoubleValidator(0.0, 100.0, 3, self.DT_Line))
        self.DT_Line.textChanged.connect(self.CheckState)
        self.DT_Line.textChanged.emit(self.DT_Line.text())
        
        self.gridLayout_3.addWidget(self.DT_Line, 3, 1, 1, 1)
        
        self.NB_Label_2 = QLabel(self.Stator_Frame)
        self.NB_Label_2.setStyleSheet("font: bold;")
        self.NB_Label_2.setObjectName("NB_Label_2")
        
        self.gridLayout_3.addWidget(self.NB_Label_2, 3, 2, 1, 1)
        
        self.NB_Line_2 = QLineEdit(self.Stator_Frame)
        self.NB_Line_2.setAlignment(Qt.AlignCenter)
        self.NB_Line_2.setObjectName("Num of Blade (Stator)")
        self.NB_Line_2.setValidator(QIntValidator(1, 1000,  self.NB_Line_2))
        self.NB_Line_2.textChanged.connect(self.CheckState)
        self.NB_Line_2.textChanged.emit(self.NB_Line_2.text())
        
        self.gridLayout_3.addWidget(self.NB_Line_2, 3, 3, 1, 1)
        
        self.CL_Label = QLabel(self.Stator_Frame)
        self.CL_Label.setStyleSheet("font: bold;")
        self.CL_Label.setObjectName("CL_Label")
        
        self.gridLayout_3.addWidget(self.CL_Label, 4, 0, 1, 1)
        
        self.CL_Line = QLineEdit(self.Stator_Frame)
        self.CL_Line.setAlignment(Qt.AlignCenter)
        self.CL_Line.setObjectName("Mount Can Length")
        self.CL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.CL_Line))
        self.CL_Line.textChanged.connect(self.CheckState)
        self.CL_Line.textChanged.emit(self.CL_Line.text())
        
        self.gridLayout_3.addWidget(self.CL_Line, 4, 1, 1, 1)
        
        self.CID_Label = QLabel(self.Stator_Frame)
        self.CID_Label.setStyleSheet("font: bold;")
        self.CID_Label.setObjectName("CID_Label")
        
        self.gridLayout_3.addWidget(self.CID_Label, 4, 2, 1, 1)
        
        self.CID_Line = QLineEdit(self.Stator_Frame)
        self.CID_Line.setAlignment(Qt.AlignCenter)
        self.CID_Line.setObjectName("Mount Can Dia")
        self.CID_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.CID_Line))
        self.CID_Line.textChanged.connect(self.CheckState)
        self.CID_Line.textChanged.emit(self.CID_Line.text())
        
        self.gridLayout_3.addWidget(self.CID_Line, 4, 3, 1, 1)
        
        self.XL_Label = QLabel(self.Stator_Frame)
        self.XL_Label.setStyleSheet("font: bold;")
        self.XL_Label.setObjectName("XL_Label")
        
        self.gridLayout_3.addWidget(self.XL_Label, 5, 0, 1, 1)
        
        self.XL_Line = QLineEdit(self.Stator_Frame)
        self.XL_Line.setAlignment(Qt.AlignCenter)
        self.XL_Line.setObjectName("Mount Can Loc")
        self.XL_Line.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.XL_Line))
        self.XL_Line.textChanged.connect(self.CheckState)
        self.XL_Line.textChanged.emit(self.XL_Line.text())
        
        self.gridLayout_3.addWidget(self.XL_Line, 5, 1, 1, 1)
        
        self.BT_Label_2 = QLabel(self.Stator_Frame)
        self.BT_Label_2.setStyleSheet("font: bold;")
        self.BT_Label_2.setObjectName("BT_Label_2")
        
        self.gridLayout_3.addWidget(self.BT_Label_2, 5, 2, 1, 1)
        
        self.BT_Line_2 = QLineEdit(self.Stator_Frame)
        self.BT_Line_2.setAlignment(Qt.AlignCenter)
        self.BT_Line_2.setObjectName("Blade Thickness (Stator)")
        self.BT_Line_2.setValidator(QDoubleValidator(0.0, 100.0, 3, self.BT_Line_2))
        self.BT_Line_2.textChanged.connect(self.CheckState)
        self.BT_Line_2.textChanged.emit(self.BT_Line_2.text())
        
        self.gridLayout_3.addWidget(self.BT_Line_2, 5, 3, 1, 1)
        
        self.RC_Label_2 = QLabel(self.Stator_Frame)
        self.RC_Label_2.setStyleSheet("font: bold;")
        self.RC_Label_2.setObjectName("RC_Label_2")
        
        self.gridLayout_3.addWidget(self.RC_Label_2, 6, 0, 1, 1)
        
        self.RC_Line_2 = QLineEdit(self.Stator_Frame)
        self.RC_Line_2.setAlignment(Qt.AlignCenter)
        self.RC_Line_2.setObjectName("Root Chord (Stator)")
        self.RC_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.RC_Line_2))
        self.RC_Line_2.textChanged.connect(self.CheckState)
        self.RC_Line_2.textChanged.emit(self.RC_Line_2.text())
        
        self.gridLayout_3.addWidget(self.RC_Line_2, 6, 1, 1, 1)
        
        self.TC_Label_2 = QLabel(self.Stator_Frame)
        self.TC_Label_2.setStyleSheet("font: bold;")
        self.TC_Label_2.setObjectName("TC_Label_2")
        
        self.gridLayout_3.addWidget(self.TC_Label_2, 6, 2, 1, 1)
        
        self.TC_Line_2 = QLineEdit(self.Stator_Frame)
        self.TC_Line_2.setAlignment(Qt.AlignCenter)
        self.TC_Line_2.setObjectName("Tip Chord (Stator)")
        self.TC_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.TC_Line_2))
        self.TC_Line_2.textChanged.connect(self.CheckState)
        self.TC_Line_2.textChanged.emit(self.TC_Line_2.text())
        
        self.gridLayout_3.addWidget(self.TC_Line_2, 6, 3, 1, 1)
        
        self.XT_Label_2 = QLabel(self.Stator_Frame)
        self.XT_Label_2.setStyleSheet("font: bold;")
        self.XT_Label_2.setObjectName("XT_Label_2")
        
        self.gridLayout_3.addWidget(self.XT_Label_2, 7, 0, 1, 1)
        
        self.XT_Line_2 = QLineEdit(self.Stator_Frame)
        self.XT_Line_2.setAlignment(Qt.AlignCenter)
        self.XT_Line_2.setObjectName("X Twist (Stator)")
        self.XT_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.XT_Line_2))
        self.XT_Line_2.textChanged.connect(self.CheckState)
        self.XT_Line_2.textChanged.emit(self.XT_Line_2.text())
        
        self.gridLayout_3.addWidget(self.XT_Line_2, 7, 1, 1, 1)
        
        self.YT_Label_2 = QLabel(self.Stator_Frame)
        self.YT_Label_2.setStyleSheet("font: bold;")
        self.YT_Label_2.setObjectName("YT_Label_2")
        
        self.gridLayout_3.addWidget(self.YT_Label_2, 7, 2, 1, 1)
        
        self.YT_Line_2 = QLineEdit(self.Stator_Frame)
        self.YT_Line_2.setAlignment(Qt.AlignCenter)
        self.YT_Line_2.setObjectName("Y Twist (Stator)")
        self.YT_Line_2.setValidator(QDoubleValidator(0.0, 1000.0, 3, self.YT_Line_2))
        self.YT_Line_2.textChanged.connect(self.CheckState)
        self.YT_Line_2.textChanged.emit(self.YT_Line_2.text())
        
        self.gridLayout_3.addWidget(self.YT_Line_2, 7, 3, 1, 1)
        
        self.line_3 = QFrame(self.Stator_Frame)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        
        self.gridLayout_3.addWidget(self.line_3, 1, 0, 1, 4)
        
        self.gridLayout.addWidget(self.Stator_Frame, 1, 2, 1, 1)
        
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 805, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        
        MainWindow.setMenuBar(self.menubar)
        
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip("Open File")
        self.actionOpen.triggered.connect(self.OpenFile)
        
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setStatusTip("Save File")
        self.actionSave.triggered.connect(self.SaveFile)
        
        self.actionToggleDarkMode = QAction(MainWindow)
        self.actionToggleDarkMode.setObjectName("actionToggleDarkMode")
        self.actionToggleDarkMode.setCheckable(True)
        self.actionToggleDarkMode.setChecked(False)
        self.actionToggleDarkMode.setStatusTip("Toggle Dark Mode")
        self.actionToggleDarkMode.triggered.connect(self.ToggleDarkMode)

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuView.addAction(self.actionToggleDarkMode)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        #Set Tab Order
        MainWindow.setTabOrder(self.R_Line, self.PSI_Line)
        MainWindow.setTabOrder(self.PSI_Line, self.PHI_Line)
        MainWindow.setTabOrder(self.PHI_Line, self.MLR_Line)
        MainWindow.setTabOrder(self.MLR_Line, self.RPM_Line)
        MainWindow.setTabOrder(self.RPM_Line, self.RD_Line)
        MainWindow.setTabOrder(self.RD_Line, self.HD_Line)
        MainWindow.setTabOrder(self.HD_Line, self.HL_Line)
        MainWindow.setTabOrder(self.HL_Line, self.NB_Line)
        MainWindow.setTabOrder(self.NB_Line, self.RC_Line)
        MainWindow.setTabOrder(self.RC_Line, self.TC_Line)
        MainWindow.setTabOrder(self.TC_Line, self.BT_Line)
        MainWindow.setTabOrder(self.BT_Line, self.BC_Line)
        MainWindow.setTabOrder(self.BC_Line, self.XT_Line)
        MainWindow.setTabOrder(self.XT_Line, self.YT_Line)
        MainWindow.setTabOrder(self.YT_Line, self.DL_Line)
        MainWindow.setTabOrder(self.DL_Line, self.DI_Line)
        MainWindow.setTabOrder(self.DI_Line, self.DT_Line)
        MainWindow.setTabOrder(self.DT_Line, self.NB_Line_2)
        MainWindow.setTabOrder(self.NB_Line_2, self.CL_Line)
        MainWindow.setTabOrder(self.CL_Line, self.CID_Line)
        MainWindow.setTabOrder(self.CID_Line, self.XL_Line)
        MainWindow.setTabOrder(self.XL_Line, self.BT_Line_2)
        MainWindow.setTabOrder(self.BT_Line_2, self.RC_Line_2)
        MainWindow.setTabOrder(self.RC_Line_2, self.TC_Line_2)
        MainWindow.setTabOrder(self.TC_Line_2, self.XT_Line_2)
        MainWindow.setTabOrder(self.XT_Line_2, self.YT_Line_2)
        
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    ################################
    ##Function: retranslateUi
    #Sets the text of all the labels
    ##Inputs: 
    #self: Ui_MainWindow
    #MainWindow: MainWindow
    ##Returns:
    #none
    ################################   
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("CompPy - Compressor Design")
        self.YT_Label.setText("Center of Y Twist")
        self.wallCheck.setText("Support Wall")
        self.RDia_Label.setText("Rotor Diameter")
        self.BT_Label.setText("Blade Thickness")
        self.R_Title.setText("Rotor Specifications")
        self.NB_Label.setText("Num of Blades")
        self.RC_Label.setText("Root Chord")
        self.HDia_Label.setText("Hub Diameter")
        self.TC_Label.setText("Tip Chord")
        self.HL_Label.setText("Hub Length")
        self.BC_Label.setText("Blade Clearance")
        self.XT_Label.setText("Center of X Twist")
        self.R_Label.setText("Reaction (R)")
        self.PSI_Label.setText("Loading (PSI)")
        self.PHI_Label.setText("Flow (PHI)")
        self.Title.setText("Universal Coefficients")
        self.MLR_Label.setText("Mean Line Radius")
        self.RPM_Label.setText("RPM")
        self.renderExport.setText("Export STL")
        self.removeButton.setText("Remove Stage")
        self.addButton.setText("Add Stage")
        self.profileButton.setText("Draw Blade Profile")
        self.renderButton.setText("Render STL")
        self.DI_Label.setText("Duct ID")
        self.S_Title.setText("Stator Specifications")
        self.DT_Label.setText("Duct Thickness")
        self.DL_Label.setText("Duct Length")
        self.NB_Label_2.setText("Num of Blades")
        self.CL_Label.setText("Mount Can Length")
        self.CID_Label.setText("Mount Can Dia")
        self.XL_Label.setText("Mount Can Loc")
        self.BT_Label_2.setText("Blade Thickness")
        self.RC_Label_2.setText("Root Chord")
        self.TC_Label_2.setText("Tip Chord")
        self.XT_Label_2.setText("Center of X Twist")
        self.YT_Label_2.setText("Center of Y Twist")
        self.menuFile.setTitle("File")
        self.menuView.setTitle("View")
        self.actionOpen.setText("Open")
        self.actionSave.setText("Save")
        self.actionToggleDarkMode.setText("Dark Mode")
        
    ################################
    ##Function: OpenFile
    #Opens compressor profile from .json file
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def OpenFile(self):
        #Open open file dialog window
        name = QFileDialog.getOpenFileName(self.MainWindow, "Open File",  None, 'Json files (*.json)')
        
        #Clear the list of anything
        self.listWidget.clear()
        try:
            #Version stuff
            if version == 5: name = name[0]
            
            #Set dictionaries with incoming vars
            self.commonVars, self.rotorVars, self.statorVars = map(list, zip(*list(StageOpen(name))))
            
            #Add the stages
            for i in range(1, len(self.commonVars) + 1):
                self.listWidget.addItem("Stage {}".format(i))
            
        except EOFError: 
            print("Invalid File, Confirm File is Correct")
            
            
    ################################
    ##Function: SaveFile
    #Saves compressor profile to .json file
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################       
    def SaveFile(self):
        # Check if we have any stages to save
        if not self.commonVars or not self.rotorVars or not self.statorVars:
            box = QMessageBox(self.MainWindow)
            box.setText("No Stages to Save")
            box.setInformativeText("Please add a stage first using 'Add Stage' button.")
            box.setWindowTitle("Save Error")
            box.exec_()
            return
        
        # Ensure we have a valid clicked index
        if self.clicked is None or self.clicked >= len(self.commonVars):
            self.clicked = 0
        
        #Open save file dialog window
        name = QFileDialog.getSaveFileName(self.MainWindow, "Save File", None, 'Json files (*.json)')
        
        # Check if user cancelled
        if version == 5:
            if not name[0]:
                return
            name = name[0]
        elif not name:
            return
        
        #Make sure the current stage is saved to the dictionaries
        for dict in [self.commonVars[self.clicked], self.rotorVars[self.clicked], self.statorVars[self.clicked]]:
            for item in dict:
                widget = self.MainWindow.findChild(QLineEdit, item)
                if widget:
                    text = widget.text()
                    if text:
                        dict[item] = text
        
        #Save dictionaries to .json file
        if not name.lower().endswith('.json'):
            name += '.json'
        StageSave(name, self.commonVars, self.rotorVars, self.statorVars)
    
    
    ################################
    ##Function: RemoveStage
    #Removes selected stage from list and profiles
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def RemoveStage(self):
        #Check if anything is selected
        listItems = self.listWidget.selectedItems()
        if not listItems:
            return
        
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return
            
        #Get the index from the stage name (e.g., "Stage 1" -> index 0)
        try:
            stageIndex = int(currentItem.text().split()[-1]) - 1
        except (ValueError, IndexError):
            return
        
        #Delete from data lists if index is valid
        if 0 <= stageIndex < len(self.rotorVars):
            del self.rotorVars[stageIndex]
            del self.commonVars[stageIndex]
            del self.statorVars[stageIndex]
        
        #Remove item from list widget
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))
                     
                     
    ################################
    ##Function: AddStage
    #Adds next stage to list and profiles
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def AddStage(self):            
        #Add stage list item
        self.listWidget.addItem("Stage {}".format(self.listWidget.count() + 1))

        #Add new stage vars
        self.rotorVars.append({"Y Twist (Rotor)" : "", "X Twist (Rotor)" : "", "Tip Chord (Rotor)" : "", "Rotor Diameter" : "", "Root Chord (Rotor)" : "", "Blade Thickness (Rotor)" : "", "Hub Diameter" : "", "Hub Length" : "", "Blade Clearance" : "", "Num of Blade (Rotor)" : ""})
        self.statorVars.append({"Duct ID" : "", "Duct Length" : "", "Duct Thickness" : "", "Num of Blade (Stator)" : "", "Mount Can Length" : "", "Mount Can Dia" : "", "Mount Can Loc" : "", "Blade Thickness (Stator)" : "", "Root Chord (Stator)" : "", "Tip Chord (Stator)" : "", "X Twist (Stator)" : "", "Y Twist (Stator)" : ""})
        self.commonVars.append({"RPM" : "", "Loading (Psi)" : "", "Flow (Phi)" : "", "Reaction (R)" : "", "Mean Line Radius" : ""})
        
        
    ################################
    ##Function: ListClicked
    #Loads currently selected stage profile
    #while saving the previously selected profile
    ##Inputs: 
    #self: Ui_MainWindow
    #clicked: currently selected stage
    ##Returns:
    #none
    ################################   
    def ListClicked(self, clicked):
        #Check if we have any stages
        if not self.commonVars or not self.rotorVars or not self.statorVars:
            return
            
        #Making sure there's no overlap
        if (self.clicked and (self.clicked < self.listWidget.count())): 
            pass
        else: 
            self.clicked = 0
        
        #Ensure clicked index is valid
        if self.clicked >= len(self.commonVars):
            self.clicked = 0
        
        #Set current value of qLineEdit to corresponding dict value,
        #of previously selected stage, if there is a value to change
        for dict in [self.commonVars[self.clicked], self.rotorVars[self.clicked], self.statorVars[self.clicked]]:
            for item in dict:
                widget = self.MainWindow.findChild(QLineEdit, item)
                if widget:
                    text = widget.text()
                    if text:
                        dict[item] = text

        #Set currently selected stage
        try:
            self.clicked = int(clicked.text().split()[-1]) - 1
        except (ValueError, IndexError):
            self.clicked = 0
        
        #Ensure new clicked index is valid
        if self.clicked >= len(self.commonVars):
            self.clicked = 0
        
        #Set each value in list of current stage to their corresponding qLineEdit
        for dict in [self.commonVars, self.rotorVars, self.statorVars]:
            for obj in dict[self.clicked]:
                widget = self.MainWindow.findChild(QLineEdit, obj)
                if widget:
                    widget.setText(str(dict[self.clicked][obj]))


    ################################
    ##Function: Export
    #If object rendered, exports to .stl file
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def Export(self):       
        #If object was previously generated
        if self.exportObj:
            name = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', None, 'STL files (*.stl)')
            
            if version == 5:
                if not name[0].lower().endswith('.stl'):
                    name[0] += '.stl'
                self.exportObj.save(name[0])
                
            else:
                if not name.lower().endswith('.stl'):
                    name += '.stl'
                self.exportObj.save(name)
                
        #If there was no rendered object, display error window
        else:
            box = QMessageBox(self.MainWindow)
            box.setText("Nothing to Export")
            box.setInformativeText("Generate STL Object")
            box.setWindowTitle("Export Error")
            box.exec_()
                                
    
    ################################
    ##Function: CheckState
    #Determines validity of currently editing qLineEdit
    #Green for acceptable
    #Yellow / Red are unacceptable
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################       
    def CheckState(self):
        sender = self.MainWindow.sender()
        state = sender.validator().validate(sender.text(), 0)[0]
        
        #Check every line
        for dict in [self.commonValidators, self.rotorValidators, self.statorValidators]:
            if sender.objectName() in dict:
                dict[sender.objectName()] = state
            else: continue
            
        #Set color of qLineEdit box (theme-aware) and tooltip
        if state == QValidator.Acceptable:
            bgcolor = "#00cc44" if self.darkMode else "#009933" # green
            sender.setToolTip("")  # Clear tooltip on valid input
        elif state == QValidator.Intermediate:
            bgcolor = "#cccc00" if self.darkMode else "#ffff00" # yellow
            valid_range = self.validRanges.get(sender.objectName(), "see documentation")
            sender.setToolTip(f"Incomplete input. Valid range: {valid_range}")
        else:
            bgcolor = "#ff3333" if self.darkMode else "#ff0000" # red
            valid_range = self.validRanges.get(sender.objectName(), "see documentation")
            sender.setToolTip(f"Invalid input! Valid range: {valid_range}")
        
        # Always use black text on validation colors for readability
        sender.setStyleSheet("QLineEdit { background-color: %s; color: #000000; }" % bgcolor)
    
        
    ################################
    ##Function: CheckAllStates
    #If object to be rendered or plotted each
    #qLineEdit object needs to be acceptably valid
    ##Inputs: 
    #self: Ui_MainWindow
    #obj: "R" or "S"
    ##Returns:
    #none
    ################################   
    def CheckAllStates(self, obj):
    
        if obj == "R": to_check = [self.commonValidators, self.rotorValidators]
        else: to_check = [self.commonValidators, self.statorValidators]
        
        #Check all values in validators dict
        #If one was not acceptable, append it to failure list with valid range suggestion
        for dict in to_check:
            if all(val == 2 for val in dict.values()): break
            else:
                for item in dict:
                    if dict[item] != 2:
                        # Add tuple with field name and valid range
                        valid_range = self.validRanges.get(item, "see documentation")
                        self.failed.append((item, valid_range))
                    else: pass

        
    ################################
    ##Function: PlotProfile
    #Plots blade profile for selected object if all valid
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def PlotProfile(self):
        from RClickWin import RenderSel, ErrorWindow
        
        # Check if we have any stages
        if not self.commonVars or not self.rotorVars or not self.statorVars:
            box = QMessageBox(self.MainWindow)
            box.setText("No Stages Available")
            box.setInformativeText("Please add a stage first using 'Add Stage' button.")
            box.setWindowTitle("Plot Profile Error")
            box.exec_()
            return
        
        # Ensure we have a valid clicked index
        if self.clicked is None or self.clicked >= len(self.commonVars):
            self.clicked = 0
        
        #Delete Currently Occupating Widget
        for i in reversed(range(self.R_FrameLayout.count())): 
            widget = self.R_FrameLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        #Make sure the current stage is saved to the dictionaries
        for dict in [self.commonVars[self.clicked], self.rotorVars[self.clicked], self.statorVars[self.clicked]]:
            for item in dict:
                widget = self.MainWindow.findChild(QLineEdit, item)
                if widget:
                    text = widget.text()
                    if text:
                        dict[item] = text
        
        wind = RenderSel(self.MainWindow)
        wind.show()
        
        if wind.exec_():
            if wind.sel == 1: 
                self.CheckAllStates("R")
                
                #If there was no failure
                if not self.failed: 
                    prof = BladePlot.NACA4Profile(self.MainWindow, self.commonVars[self.clicked], self.rotorVars[self.clicked], "R")
                    self.R_FrameLayout.addWidget(prof)
                    prof.plotter()
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    prof.close()
                    
                #If there was a failure, show the failures
                else: ErrorWindow(self.MainWindow, self.failed).show()
                    
            #If stator was picked
            elif wind.sel == 2: 
                self.CheckAllStates("S")
                
                #If there was no failure
                if not self.failed: 
                    prof = BladePlot.NACA4Profile(self.MainWindow, self.commongVars[self.clicked], self.statorVars[self.clicked], "S")
                    self.R_FrameLayout.addWidget(prof)
                    prof.plotter()
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    prof.close()
                
                #If there was a failure, show the failures
                else: ErrorWindow(self.MainWindow, self.failed).show()
            
            else: pass
            
        #Reset failed list
        self.failed = []
        

    ################################
    ##Function: Render
    #3D renders selected object if all valid
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def Render(self):
        from RClickWin import RenderSel, ErrorWindow
        
        # Check if we have any stages
        if not self.commonVars or not self.rotorVars or not self.statorVars:
            box = QMessageBox(self.MainWindow)
            box.setText("No Stages Available")
            box.setInformativeText("Please add a stage first using 'Add Stage' button.")
            box.setWindowTitle("Render Error")
            box.exec_()
            return
        
        # Ensure we have a valid clicked index
        if self.clicked is None or self.clicked >= len(self.commonVars):
            self.clicked = 0
        
        #Delete Currently Occupating Widget
        for i in reversed(range(self.R_FrameLayout.count())): 
            widget = self.R_FrameLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        #Make sure the current stage is saved to the dictionaries
        for dict in [self.commonVars[self.clicked], self.rotorVars[self.clicked], self.statorVars[self.clicked]]:
            for item in dict:
                widget = self.MainWindow.findChild(QLineEdit, item)
                if widget:
                    text = widget.text()
                    if text:
                        dict[item] = text
                     
        #Display selection window
        wind = RenderSel(self.MainWindow)
        wind.show()
        
        #Once window is closed
        if wind.exec_():
            #If rotor was picked
            if wind.sel == 1: 
                self.CheckAllStates("R")
                
                #If there was no failure
                if not self.failed: 
                    rend = RenderWindow.RenderWindow(self.MainWindow, self.commonVars[self.clicked], self.rotorVars[self.clicked], "R", self.wallCheck.isChecked())
                    self.R_FrameLayout.addWidget(rend)
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    self.exportObj = rend.returnObject()
                    
                #If there was a failure, show the failures
                else: ErrorWindow(self.MainWindow, self.failed).show()
            
            #If stator was picked
            elif wind.sel == 2: 
                self.CheckAllStates("S")
                
                #If there was no failure
                if not self.failed: 
                    rend = RenderWindow.RenderWindow(self.MainWindow, self.commonVars[self.clicked], self.statorVars[self.clicked], "S")
                    self.R_FrameLayout.addWidget(rend)
                    self.R_Frame.setLayout(self.R_FrameLayout)
                    self.exportObj = rend.returnObject()
                
                #If there was a failure, show the failures
                else: ErrorWindow(self.MainWindow, self.failed).show()
            
            else: pass
  
        #Reset failed list
        self.failed = []
                                
    
    ################################
    ##Function: ToggleDarkMode
    #Toggles between light and dark mode
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def ToggleDarkMode(self):
        self.darkMode = not self.darkMode
        self.ApplyTheme()
    
    
    ################################
    ##Function: ApplyTheme
    #Applies the current theme (light or dark)
    ##Inputs: 
    #self: Ui_MainWindow
    ##Returns:
    #none
    ################################   
    def ApplyTheme(self):
        if self.darkMode:
            # Dark mode palette
            darkPalette = """
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #e0e0e0;
                }
                QFrame {
                    background-color: #323232;
                    border: 1px solid #3f3f3f;
                }
                QLabel {
                    color: #e0e0e0;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #555555;
                    padding: 2px;
                }
                QLineEdit:focus {
                    border: 1px solid #0078d4;
                }
                QPushButton {
                    background-color: #404040;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    padding: 5px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                    border: 1px solid #666666;
                }
                QPushButton:pressed {
                    background-color: #353535;
                }
                QListWidget {
                    background-color: #404040;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                }
                QListWidget::item:selected {
                    background-color: #0078d4;
                }
                QListWidget::item:hover {
                    background-color: #4a4a4a;
                }
                QMenuBar {
                    background-color: #323232;
                    color: #e0e0e0;
                }
                QMenuBar::item:selected {
                    background-color: #404040;
                }
                QMenu {
                    background-color: #323232;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                }
                QMenu::item:selected {
                    background-color: #0078d4;
                }
                QCheckBox {
                    color: #e0e0e0;
                }
            """
            self.MainWindow.setStyleSheet(darkPalette)
        else:
            # Light mode (default Qt style)
            self.MainWindow.setStyleSheet("")
        
        # Reapply validation colors for line edits
        for dict in [self.commonValidators, self.rotorValidators, self.statorValidators]:
            for name, state in dict.items():
                if state is not None:
                    widget = self.MainWindow.findChild(QLineEdit, name)
                    if widget:
                        if state == QValidator.Acceptable:
                            bgcolor = "#009933" if not self.darkMode else "#00cc44"
                        elif state == QValidator.Intermediate:
                            bgcolor = "#ffff00" if not self.darkMode else "#cccc00"
                        else:
                            bgcolor = "#ff0000" if not self.darkMode else "#ff3333"
                        widget.setStyleSheet("QLineEdit { background-color: %s; color: #000000; }" % bgcolor)
    
    
    ################################
    ##Function: closeEvent
    #Handles closing of program
    ##Inputs: 
    #self: Ui_MainWindow
    #event: closing event
    ##Returns:
    #none
    ################################   
    def closeEvent(self, event):
        qApp.quit()
        event.ignore()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

