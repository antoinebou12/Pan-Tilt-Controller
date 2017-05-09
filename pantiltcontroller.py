import sys
import serial
import time
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import QMainWindow, QAction,qApp, QApplication, QWidget, QFileDialog, QLineEdit, QPushButton,QLabel, QColumnView, QFileSystemModel, QSplitter, QTreeView, QListView, QTextEdit,QDialog, QVBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
from PyQt5.QtCore import QDir, Qt, QEvent

global positionPan
global positionTilt
positionPan = 0
positionTilt = 0


widthScreen = GetSystemMetrics(0)
heightScreen = GetSystemMetrics(1)
widthApp = widthScreen/1.5
heightApp = heightScreen/1.5


global ser
ser = serial.Serial('COM3', 9600, timeout=1)
ser.xonxoff = True
ser.isOpen()
ser.write('v' + '\r\n')
ser.write('pb' + '\r\n')
ser.write('tb' + '\r\n')
ser.write('pd100' + '\r\n')
ser.write('td100' + '\r\n')
ser.write('pb100' + '\r\n')
ser.write('tb100' + '\r\n')
ser.write('rd' + '\r\n')
ser.write('pp0' + '\r\n')
ser.write('tp0' + '\r\n')
ser.write('pxu1500' + '\r\n')
ser.write('pnu-1000' + '\r\n')
ser.write('tnu-850' + '\r\n')
ser.write('txu585' + '\r\n')
ser.write('pp'+ '\r\n')
ser.write('tp'+ '\r\n')


class DialogControl(QDialog,QWidget):
    def __init__(self,parent=None):
        super(DialogControl, self).__init__(parent)
        qApp.installEventFilter(self)

    def eventFilter(self, source, event):
        global positionPan
        global positionTilt
        if event.type() == QEvent.KeyPress:
            #print(event.key())
            if event.key()== 16777235:  # QtCore.Qt.Key_Escape is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
                #print 'up'
                positionTilt = int(positionTilt + 5)
                #print 'tp' + str(positionTilt) + '\r\n'
                ser.write('tp' + str(positionTilt - 10) + '\r\n')
            elif event.key() == 16777237:
                #print 'down'
                positionTilt = int(positionTilt - 5)
                #print 'tp' + str(positionTilt) + '\r\n'
                ser.write('tp' + str(positionTilt - 10) + '\r\n')
            elif event.key() == 16777234:
                #print 'left'
                positionPan = int(positionPan - 5)
                #print 'pp' + str(positionPan) + '\r\n'
                ser.write('pp' + str(positionPan) + '\r\n')
            elif event.key() == 16777236:
                #print 'right'
                positionPan = int(positionPan + 5)
                #print 'pp' + str(positionPan) + '\r\n'
                ser.write('pp' + str(positionPan) + '\r\n')

        return super(DialogControl, self).eventFilter(source, event)

    def Control(self):
        global positionPan
        global positionTilt
        self.addDialog = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.addDialog.setWindowTitle('Control')
        self.addDialog.setWindowIcon(QIcon('image\Algolux.png'))
        self.addDialog.resize(100, 100)
        layout = QGridLayout()
        self.up = QPushButton(u'\u25b2')
        self.down = QPushButton(u'\u25bc')
        self.left =QPushButton(u'\u25c0')
        self.right =QPushButton(u'\u25b6')
        self.ok = QPushButton('OK')
        layout.addWidget(self.up)
        layout.addWidget(self.down)
        layout.addWidget(self.left)
        layout.addWidget(self.right)
        layout.addWidget(self.ok)
        self.addDialog.setLayout(layout)
        self.up.clicked.connect(lambda: self.buttonClick(self.up))
        self.down.clicked.connect(lambda: self.buttonClick(self.down))
        self.left.clicked.connect(lambda: self.buttonClick(self.left))
        self.right.clicked.connect(lambda: self.buttonClick(self.right))
        self.ok.clicked.connect(lambda: self.buttonClick(self.ok))
        self.addDialog.show()
    def buttonClick(self,button):
        global positionPan
        global positionTilt
        if button == self.up:
            print 'up'
            positionTilt = int(positionTilt - 10)
            print 'pp' + str(positionTilt) + '\r\n'
            ser.write('tp' + str(positionTilt) + '\r\n')
        if button == self.down:
            positionTilt = int(positionTilt + 10)
            print 'pp' + str(positionTilt) + '\r\n'
            ser.write('tp' + str(positionTilt) + '\r\n')

        if button == self.left:
            positionPan = int(positionPan - 10)
            print 'pp' + str(positionPan) + '\r\n'
            ser.write('pp' + str(positionPan) + '\r\n')

        if button == self.right:
            positionPan = int(positionPan + 10)
            print 'pp' + str(positionPan) + '\r\n'
            ser.write('pp' + str(positionPan) + '\r\n')
        if button == self.ok:
            self.addDialog.reject()





class MenuFile(QMainWindow,DialogControl):
    def __init__(self, parent=None):
        super(MenuFile, self).__init__(parent)
        self.setCentralWidget(FormWidget(self))

        self.Menu()

    def Menu(self):

        openFile = QAction('Control', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Control')
        openFile.triggered.connect(self.Control)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Control')
        fileMenu.addAction(openFile)

        self.resize(widthApp, heightApp)
        self.move(0, 0)
        self.setWindowTitle('PTC')
        self.setWindowIcon(QIcon('image\Algolux.png'))


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.UI()

    def UI(self):
        self.textBox()
        global positionPan
        global positionTilt
        self.panLabel = QLabel('Pan')
        self.pan = QLineEdit()
        self.tiltLabel = QLabel('Tilt')
        self.tilt = QLineEdit()
        self.logView = QTextEdit()
        self.ok = QPushButton('Ok')
        self.reset = QPushButton('Reset')
        layout = QGridLayout()
        layout.addWidget(self.panLabel)
        layout.addWidget(self.pan)
        layout.addWidget(self.tiltLabel)
        layout.addWidget(self.tilt)
        layout.addWidget(self.logView)
        layout.addWidget(self.ok)
        layout.addWidget(self.reset)
        self.setLayout(layout)
        self.textBox()
        self.ok.clicked.connect(lambda: self.buttonClick(self.ok))
        self.reset.clicked.connect(lambda: self.buttonClick(self.reset))
        self.textBox()

    def textBox(self):
        self.out = ''
        time.sleep(1)
        while ser.inWaiting() > 0:
            self.out += ser.read(1)
        if self.out != '':
            self.out =  self.out
        self.logView.append(self.out)
        QApplication.processEvents()

    def buttonClick(self, button):
        global positionPan
        global positionTilt
        self.textBox()
        if button ==  self.ok:
            panText = self.pan.text()
            tiltText = self.tilt.text()
            panInput = str('pp' + panText)
            tiltInput = str('tp' + tiltText)
            ser.write(panInput + '\r\n')
            ser.write(tiltInput + '\r\n')
            positionPan = panText
            positionTilt = tiltText
            self.textBox()

        elif button == self.reset:
            ser.write('pp0' + '\r\n')
            ser.write('tp0' + '\r\n')
            positionPan = 0
            positionTilt = 0
            self.textBox()




def main():
    app = QApplication([])
    ex = MenuFile()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()







