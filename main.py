import sys
import h5py
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QLabel, QMenu, QMenuBar, QAction,QFileDialog,QGroupBox,QVBoxLayout
from PyQt5.QtGui import QIcon,QPixmap

class Gui(QWidget):

    def __init__(self):
        super().__init__()

        self.setUI()

    def setUI(self):
        self.SetMenu()
        self.setGeometry(300, 250, 1100, 600)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('ex.png'))
        self.setWindowTitle('SegmentPhoto')
        self.label = QLabel()
        self.canvas = QGroupBox(self)
        self.canvas.setStyleSheet("QGroupBox { background-color: white ;border: 1px solid #9F9B9B}")
        self.canvas.move(100, 30)
        self.canvas.resize(900, 400)
        layout = QVBoxLayout(self.canvas)
        layout.addWidget(self.label)
    def SetMenu(self):
        bar = QMenuBar(self)
        file = bar.addMenu("&File")
        edit = bar.addMenu("&Edit")
        image = bar.addMenu("&Image")
        view = bar.addMenu("&View")
        help = bar.addMenu("&Help")
        file.addAction("New...")
        open = QAction('Open..', self)
        open.triggered.connect(self.openImage)
        file.addAction(open)
        file.addAction("Save...")
        save = QAction("Save", self)
        save.setShortcut("Ctrl+S")
        file.addAction(save)
        file.addAction("Save As...")
    def openImage(self):
        label = QLabel()
        imagePath, _ = QFileDialog.getOpenFileName()
        print(imagePath)
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)
        self.canvas.resize(pixmap.width(), pixmap.height())
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            event.accept()
        else:

            event.ignore()


def main():

    app = QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()