from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1070, 703)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ====================================================
        # Animation section
        # ====================================================

        self.animacion = QtWidgets.QGroupBox(self.centralwidget)
        self.animacion.setGeometry(QtCore.QRect(270, 20, 561, 361))
        self.animacion.setObjectName("animacion")

        self.boton = QtWidgets.QPushButton(self.animacion)
        self.boton.setGeometry(QtCore.QRect(210, 320, 121, 28))
        self.boton.setObjectName("boton")

        self.gif = QtWidgets.QLabel(self.animacion)
        self.gif.setGeometry(QtCore.QRect(140, 20, 291, 291))
        self.gif.setText("")
        self.gif.setPixmap(QtGui.QPixmap("animacion.gif"))
        self.gif.setScaledContents(True)
        self.gif.setObjectName("gif")

        # ====================================================
        # CO2 graph section
        # ====================================================

        self.grafico = QtWidgets.QGroupBox(self.centralwidget)
        self.grafico.setGeometry(QtCore.QRect(380, 480, 381, 201))
        self.grafico.setObjectName("grafico")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.grafico)
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(10, 20, 361, 171)
        )
        self.verticalLayoutWidget.setObjectName(
            "verticalLayoutWidget"
        )

        self.graph = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget
        )
        self.graph.setContentsMargins(0, 0, 0, 0)
        self.graph.setObjectName("graph")

        # ====================================================
        # LED intensity section
        # ====================================================

        self.intensidad = QtWidgets.QGroupBox(
            self.centralwidget
        )
        self.intensidad.setGeometry(
            QtCore.QRect(20, 480, 261, 201)
        )
        self.intensidad.setObjectName("intensidad")

        self.dial = QtWidgets.QDial(self.intensidad)
        self.dial.setGeometry(
            QtCore.QRect(50, 70, 151, 121)
        )
        self.dial.setStyleSheet(
            "background-color: rgb(0, 0, 200);"
        )
        self.dial.setMinimum(0)
        self.dial.setMaximum(255)
        self.dial.setNotchesVisible(True)
        self.dial.setObjectName("dial")

        self.lcd_dial = QtWidgets.QLCDNumber(
            self.intensidad
        )
        self.lcd_dial.setGeometry(
            QtCore.QRect(70, 20, 101, 41)
        )
        self.lcd_dial.setObjectName("lcd_dial")

        # ====================================================
        # Sensor value section
        # ====================================================

        self.valor_co2 = QtWidgets.QGroupBox(
            self.centralwidget
        )
        self.valor_co2.setGeometry(
            QtCore.QRect(840, 480, 201, 201)
        )
        self.valor_co2.setObjectName("valor_co2")

        self.lcd_co2 = QtWidgets.QLCDNumber(
            self.valor_co2
        )
        self.lcd_co2.setGeometry(
            QtCore.QRect(30, 90, 139, 86)
        )
        self.lcd_co2.setObjectName("lcd_co2")

        # ====================================================
        # Serial connection section
        # ====================================================

        self.conexion = QtWidgets.QGroupBox(
            self.centralwidget
        )
        self.conexion.setGeometry(
            QtCore.QRect(420, 390, 281, 81)
        )
        self.conexion.setMinimumSize(
            QtCore.QSize(201, 0)
        )

        font = QtGui.QFont()
        font.setBold(True)

        self.conexion.setFont(font)
        self.conexion.setObjectName("conexion")

        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(
            self.conexion
        )
        self.horizontalLayoutWidget_3.setGeometry(
            QtCore.QRect(6, 20, 271, 51)
        )
        self.horizontalLayoutWidget_3.setObjectName(
            "horizontalLayoutWidget_3"
        )

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_3
        )
        self.horizontalLayout_3.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.horizontalLayout_3.setObjectName(
            "horizontalLayout_3"
        )

        self.conectar = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_3
        )
        self.conectar.setObjectName("conectar")
        self.horizontalLayout_3.addWidget(
            self.conectar
        )

        self.puertos = QtWidgets.QComboBox(
            self.horizontalLayoutWidget_3
        )
        self.puertos.setObjectName("puertos")
        self.horizontalLayout_3.addWidget(
            self.puertos
        )

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        # ====================================================
        # Signal connections
        # ====================================================

        self.conectar.clicked.connect(
            MainWindow.connect
        )

        self.boton.clicked.connect(
            MainWindow.animation
        )

        self.dial.valueChanged.connect(
            self.lcd_dial.display
        )

        self.dial.valueChanged.connect(
            MainWindow.writeDial
        )

        QtCore.QMetaObject.connectSlotsByName(
            MainWindow
        )

    def retranslateUi(self, MainWindow):
        translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(
            translate(
                "MainWindow",
                "Arduino Air Quality Monitor",
            )
        )

        self.animacion.setTitle(
            translate(
                "MainWindow",
                "Sensor Visualization",
            )
        )

        self.boton.setText(
            translate(
                "MainWindow",
                "Start Animation",
            )
        )

        self.grafico.setTitle(
            translate(
                "MainWindow",
                "Air Quality Graph",
            )
        )

        self.intensidad.setTitle(
            translate(
                "MainWindow",
                "LED Intensity",
            )
        )

        self.valor_co2.setTitle(
            translate(
                "MainWindow",
                "MQ-135 Sensor Value",
            )
        )

        self.conexion.setTitle(
            translate(
                "MainWindow",
                "Serial Connection",
            )
        )

        self.conectar.setText(
            translate(
                "MainWindow",
                "Connect",
            )
        )