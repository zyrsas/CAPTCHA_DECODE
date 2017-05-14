# coding: utf-8
import sys
import os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
from train_authcode import get_pic, split_pic, convert_to_bw
from shutil import copyfile
from identify import d

app = QtGui.QApplication(sys.argv)


#setting the path variable for icon
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'cap_logo.jpg')


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('window.ui', self)

        self.setWindowTitle('CAPTCHA_DECODE')
        self.setWindowIcon(QtGui.QIcon(path))

        self.pushButton.clicked.connect(self.open_captcha)
        self.recognizeBtn.clicked.connect(self.recognize_captcha)

    def open_captcha(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', r"e:/origin/")

        vuvupic = QtGui.QPixmap(self.fname)
        self.label = QtGui.QLabel(self)
        self.label.setPixmap(vuvupic)
        self.label.move(20, 25)
        self.label.setScaledContents(True)
        self.label.setFixedWidth(210)
        self.label.setFixedHeight(90)
        self.label.show()

    def recognize_captcha(self):
        self.absolute_fname = os.path.basename(str(self.fname))
        copyfile(self.fname, os.getcwd() + "\\" + self.absolute_fname)
        self.edtRecognizeText.setText(split_pic(convert_to_bw(get_pic(str(self.absolute_fname)))))
        label = [self.label_letter1, self.label_letter2, self.label_letter3, self.label_letter4]
        matrix = [self.matrix_1, self.matrix_2, self.matrix_3, self.matrix_4]
        for i in range(0, 4):
            vuvupic = QtGui.QPixmap(self.get_subpic(self.absolute_fname, str(i)))
            label[i].setPixmap(vuvupic)
            label[i].setScaledContents(True)
            label[i].setFixedWidth(80)
            label[i].setFixedHeight(50)
            matrix[i].append(str(d.keys()[d.values().index(self.edtRecognizeText.text()[i])]))

    def get_subpic(self, fname, count):
        return fname.replace('.jpg', '_' + count + '.png')

mw = MainWindow()
mw.show()
app.exec_()
