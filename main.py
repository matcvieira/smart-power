from smartpower.gui import simulador

def main():
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

