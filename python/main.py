import sys

import matplotlib
import numpy as np
import serial
import serial.tools.list_ports as ports

from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from gui import Ui_MainWindow


matplotlib.use("qtagg")


class Interfaz(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize GUI elements.
        self.setupUi(self)

        # Disable maximize button.
        self.setWindowFlag(
            QtCore.Qt.WindowType.WindowMaximizeButtonHint,
            False,
        )

        # Serial connection.
        self.serialPort = serial.Serial(
            port=None,
            baudrate=9600,
            timeout=0.1,
        )

        # Load available serial ports.
        self.COMPorts = [
            port.device
            for port in ports.comports()
        ]

        self.puertos.addItems(self.COMPorts)

        self.connected_flag = False

        # Timers.
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.leerdatos)

        self.timer_2 = QtCore.QTimer(self)
        self.timer_2.timeout.connect(self.grafica)

        # LED control is disabled until a serial connection is established.
        self.dial.setEnabled(False)

        # Matplotlib graph.
        self.sc = MplCanvas(
            self,
            width=10,
            height=6,
            dpi=100,
        )

        self.graph.addWidget(
            NavigationToolbar(
                self.sc,
                self,
            )
        )

        self.graph.addWidget(
            self.sc
        )

        # Data acquisition configuration.
        self.samples = 90

        self.t = np.arange(
            self.samples
        )

        self.y_1 = np.zeros(
            self.samples
        )

        self.counter = 0
        self.startAnimation = False

        self.grafica()

    # ========================================================
    # Serial connection
    # ========================================================

    def connect(self):
        try:
            if not self.connected_flag:
                selected_port = self.puertos.currentText()

                if not selected_port:
                    print("No serial port selected.")
                    return

                self.serialPort.port = selected_port

                self.serialPort.open()

                self.connected_flag = True

                self.conectar.setText(
                    "Disconnect"
                )

                self.dial.setEnabled(
                    True
                )

                self.setTimer()

                print(
                    f"Connected to serial port: {selected_port}"
                )

            else:
                self.disconnect_serial()

        except serial.SerialException as error:
            print(
                f"Serial connection error: {error}"
            )

    # ========================================================
    # Timer configuration
    # ========================================================

    def setTimer(self):
        # Check serial data frequently.
        self.timer.setInterval(20)

        # Update the graph every 100 ms.
        self.timer_2.setInterval(100)

        self.timer.start()
        self.timer_2.start()

    # ========================================================
    # Animation
    # ========================================================

    def animation(self):
        if not self.startAnimation:
            self.boton.setText(
                "Stop Animation"
            )

            self.movie = QtGui.QMovie(
                "animacion.gif"
            )

            self.gif.setMovie(
                self.movie
            )

            self.movie.start()

            self.startAnimation = True

        else:
            self.movie.stop()

            self.startAnimation = False

            self.boton.setText(
                "Start Animation"
            )

    # ========================================================
    # Serial sensor data
    # ========================================================

    def leerdatos(self):
        if not self.serialPort.is_open:
            return

        try:
            if self.serialPort.in_waiting <= 0:
                return

            raw_value = (
                self.serialPort
                .readline()
                .decode("utf-8", errors="ignore")
                .strip()
            )

            if not raw_value:
                return

            sensor_value = float(
                raw_value
            )

            # Update LCD display.
            self.lcd_co2.display(
                sensor_value
            )

            # Store sensor value.
            self.y_1[self.counter] = sensor_value

            self.counter += 1

            if self.counter >= self.samples:
                self.counter = 0

        except (
            ValueError,
            serial.SerialException,
        ) as error:
            print(
                f"Serial data error: {error}"
            )

    # ========================================================
    # Graph
    # ========================================================

    def grafica(self):
        self.sc.axes_1.clear()

        self.sc.axes_1.set_xlim(
            0,
            self.samples - 1,
        )

        self.sc.axes_1.set_ylim(
            0,
            1023,
        )

        self.sc.axes_1.set_title(
            "MQ-135 Sensor Reading"
        )

        self.sc.axes_1.set_xlabel(
            "Sample"
        )

        self.sc.axes_1.set_ylabel(
            "Analog value"
        )

        self.sc.axes_1.plot(
            self.t,
            self.y_1,
        )

        self.sc.draw()

    # ========================================================
    # LED intensity control
    # ========================================================

    def writeDial(self, value):
        if not self.serialPort.is_open:
            return

        try:
            message = f"{value}\n"

            self.serialPort.write(
                message.encode("utf-8")
            )

        except serial.SerialException as error:
            print(
                f"Could not send LED value: {error}"
            )

    # ========================================================
    # Serial disconnection
    # ========================================================

    def disconnect_serial(self):
        self.timer.stop()
        self.timer_2.stop()

        if self.serialPort.is_open:
            port_name = self.serialPort.port

            self.serialPort.close()

            print(
                f"Serial port {port_name} disconnected."
            )

        self.connected_flag = False

        self.conectar.setText(
            "Connect"
        )

        self.dial.setEnabled(
            False
        )

    # ========================================================
    # Window close event
    # ========================================================

    def closeEvent(self, event):
        self.disconnect_serial()

        if (
            hasattr(self, "movie")
            and self.movie is not None
        ):
            self.movie.stop()

        event.accept()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(
        self,
        parent=None,
        width=3,
        height=3,
        dpi=100,
    ):
        self.fig = Figure(
            figsize=(width, height),
            dpi=dpi,
        )

        self.axes_1 = self.fig.add_subplot(
            111
        )

        self.fig.tight_layout(
            pad=5
        )

        super().__init__(
            self.fig
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(
        sys.argv
    )

    main_window = Interfaz()
    main_window.show()

    sys.exit(
        app.exec()
    )