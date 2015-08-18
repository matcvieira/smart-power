from smartpower.gui import simulador
from PySide import QtCore, QtGui
import sys

def main():
    app = QtGui.QApplication(sys.argv)
    mySW = simulador.ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

