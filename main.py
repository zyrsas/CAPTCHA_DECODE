# coding: utf-8
import sys
import os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
from train_authcode import get_pic, split_pic, convert_to_bw
from shutil import copyfile
from identify_picture import standard_dict
from train_authcode import get_train_set
import time

app = QtGui.QApplication(sys.argv)

#setting the path variable for icon
path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'cap_logo.jpg')


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('window.ui', self)

        self.fname = ''

        self.setWindowTitle('CAPTCHA_DECODE')
        self.setWindowIcon(QtGui.QIcon(path))

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        self.setFixedSize(self.size())

        self.pushButton.clicked.connect(self.open_captcha)
        self.recognizeBtn.clicked.connect(self.recognize_captcha)
        self.open_folder.clicked.connect(self.open_for_train)
        self.btnStartTrain.clicked.connect(self.start_train)

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
        if not self.fname:
            pass
        else:
            # clear textBrowser
            self.clear()
            # copy img curr dirrectory
            self.absolute_fname = os.path.basename(str(self.fname))
            copyfile(self.fname, os.getcwd() + "\\" + self.absolute_fname)
            self.edtRecognizeText.setText(split_pic(convert_to_bw(get_pic(str(self.absolute_fname)))))
            # list of textBrowser and image label
            label = [self.label_letter1, self.label_letter2, self.label_letter3, self.label_letter4]
            matrix = [self.matrix_1, self.matrix_2, self.matrix_3, self.matrix_4]
            # create split image
            for i in range(0, 4):
                vuvupic = QtGui.QPixmap(self.get_subpic(self.absolute_fname, str(i)))
                label[i].setPixmap(vuvupic)
                label[i].setScaledContents(True)
                label[i].setFixedWidth(80)
                label[i].setFixedHeight(50)
                # matrix[i].append(str(d.keys()[d.values().index(self.edtRecognizeText.text()[i])]))
                matrix[i].append(str(standard_dict[ str(self.edtRecognizeText.text()[i])]))

    def open_for_train(self):
        self.fname_train = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lblFolder.setText(self.fname_train)
        path, dirs, files = os.walk(self.fname_train).next()
        self.lblCount.setText(str(len(files)))
        self.lblCurrent.setText('0')
        self.progressBar.maximum = len(files)

    def start_train(self):
        path, dirs, files = os.walk(self.fname_train).next()
        count = len(files)

        # list of textBrowser and image label
        label = [self.label_letter1, self.label_letter2, self.label_letter3, self.label_letter4]
        matrix = [self.matrix_1, self.matrix_2, self.matrix_3, self.matrix_4]

        for i in range(0, 15):

            self.update(0, 1116, 0, 537)
            self.repaint()
            time.sleep(1)

            self.clear()


            path = self.fname_train + "\\" + str(i) + ".jpg"
            self.absolute_fname = os.path.basename(str(path))
            copyfile(path, os.getcwd() + "\\" + self.absolute_fname)

            self.lblCurrent.setText(str(i))
            self.lblStatus.setText("Good")
            self.lblName.setText(self.absolute_fname)
            self.progressBar.setValue(i)
            
            vuvupic = QtGui.QPixmap(self.absolute_fname)
            self.label = QtGui.QLabel(self)
            self.label.setPixmap(vuvupic)
            self.label.move(20, 25)
            self.label.setScaledContents(True)
            self.label.setFixedWidth(210)
            self.label.setFixedHeight(90)
            self.label.show()

            self.edtRecognizeText.setText(split_pic(convert_to_bw(get_pic(str(self.absolute_fname)))))
            # list of textBrowser and image label
            label = [self.label_letter1, self.label_letter2, self.label_letter3, self.label_letter4]
            matrix = [self.matrix_1, self.matrix_2, self.matrix_3, self.matrix_4]
            # create split image
            for j in range(0, 4):
                vuvupic = QtGui.QPixmap(self.get_subpic(self.absolute_fname, str(j)))
                label[j].setPixmap(vuvupic)
                label[j].setScaledContents(True)
                label[j].setFixedWidth(80)
                label[j].setFixedHeight(50)
                # matrix[i].append(str(d.keys()[d.values().index(self.edtRecognizeText.text()[i])]))
                try:
                    matrix[j].append(str(standard_dict[str(self.edtRecognizeText.text()[j])]))
                except KeyError:
                    self.lblStatus.setText("Bad")



    def update_form(self):
        label = [self.label_letter1, self.label_letter2, self.label_letter3, self.label_letter4]
        matrix = [self.matrix_1, self.matrix_2, self.matrix_3, self.matrix_4]
        for i in range(0, 4):
            label[i].setEnabled(False)
            matrix[i].setEnabled(False)
        for i in range(0, 4):
            label[i].setEnabled(True)
            matrix[i].setEnabled(True)


    def clear(self):
        matrix = [self.matrix_1, self.matrix_2, self.matrix_3, self.matrix_4]
        for i in range(0, 4):
             matrix[i].clear()

    def get_subpic(self, fname, count):
        return fname.replace('.jpg', '_' + count + '.png')

mw = MainWindow()
mw.show()
app.exec_()
