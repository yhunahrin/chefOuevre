import sys
import h5py
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QLabel, QMenu, QMenuBar, QAction,QFileDialog,QGroupBox,QVBoxLayout,QToolBar,QMainWindow
from PyQt5.QtGui import QIcon,QPixmap,QPainter,QPen,QImage
from tensorflow import keras
import tensorflow as tf
import os
import numpy as np
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras import backend as keras
import cv2 as cv
import ast
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Gui(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setUI()

    def setUI(self):
        self.SetMenu()
        self.setGeometry(300, 300, 1100, 600)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('ex.png'))
        self.setWindowTitle('SegmentPhoto')
        self.label = QLabel()
        self.canvas = QGroupBox(self)
        self.canvas.setStyleSheet("QGroupBox { background-color: white ;border: 1px solid #9F9B9B}")
        self.canvas.move(100, 55)
        self.canvas.resize(900, 400)
        self.mPixmap = QPixmap()
        layout = QVBoxLayout(self.canvas)
        layout.addWidget(self.label)
        self.image_Path = QFileDialog
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False
    def SetMenu(self):
        menuBar = self.menuBar()
        file = menuBar.addMenu("&File")
        edit = menuBar.addMenu("&Edit")
        image = menuBar.addMenu("&Image")
        view = menuBar.addMenu("&View")
        help = menuBar.addMenu("&Help")


        file.addAction("New...")

        open = QAction('Open..', self)
        open.triggered.connect(self.openImage)
        file.addAction(open)

        save = QAction("Save..", self)
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.saveImage)
        file.addAction(save)

        saveAs = QAction("SaveAs..", self)
        saveAs.triggered.connect(self.saveAs)
        file.addAction(saveAs)

        toolbar = self.addToolBar("ToolBar")
        iconSelect = QIcon()
        iconSelect.addPixmap(QPixmap("C:\\Users\\aduongng\\Desktop\\image61.bmp"), QIcon.Selected, QIcon.On)
        select = toolbar.addAction(iconSelect, "&Select")
        select.triggered.connect(self.selectImage)

        iconCrop = QIcon()
        iconCrop.addPixmap(QPixmap("C:\\Users\\aduongng\\Desktop\\chems.jpg"), QIcon.Selected, QIcon.On)
        crop = toolbar.addAction(iconCrop, "&Crop")
        crop.triggered.connect(self.cropImage)

        iconMask = QIcon()
        iconMask.addPixmap(QPixmap("C:\\Users\\aduongng\\Desktop\\chems.jpg"), QIcon.Selected, QIcon.On)
        mask = toolbar.addAction(iconMask, "&Mask")
        mask.triggered.connect(self.maskImage)

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        print(imagePath)
        self.pixmap = QPixmap(imagePath)
        self.mPixmap = self.pixmap
        self.label.setPixmap( self.mPixmap)
        self.canvas.resize( self.mPixmap.width(),  self.mPixmap.height())
        self.image_Path = imagePath
    def saveImage(self):
        self.mPixmap.save(self.image_Path)
    def saveAs(self):
        self.image_Path, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "BMP(*.bmp);;PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if self.image_Path == "":
            return
        self.mPixmap.save(self.image_Path)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            event.accept()
        else:

            event.ignore()
    def readData(self):
        [images_paths, labels]=self.readDataset()
        label = QLabel()
        print(images_paths[1])
        pixmap = QPixmap(images_paths[1])
        self.label.setPixmap(pixmap)
        self.canvas.resize(pixmap.width(), pixmap.height())
    def readDataset(self):
        images_paths, labels = list(), list()
        dataset = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        file = os.listdir(dataset)
        count =0
        for data in file:
            images_paths.append( dataset+data)
            labels.append(count)
            count+=1
        return images_paths,labels
    def cropImage(self):
         rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
         cropped = self.mPixmap.copy(rect)
         self.mPixmap = cropped
         self.label.setPixmap(self.mPixmap)
         self.canvas.resize(self.mPixmap.width(),self.mPixmap.height())
    def selectImage(self):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)
    def maskImage(self):
        imagePath = os.path.normpath(self.image_Path)
        print(imagePath)
        im_color = cv.imread(imagePath)
        print(im_color)
        i, im = cv.threshold(im_color, 10, 255, cv.THRESH_BINARY_INV)
        height, width, channel = im.shape
        bytesPerLine = 3 * width
        qImg = QImage(im.data, width, height,bytesPerLine, QImage.Format_RGB888)
        self.mPixmap = QPixmap.fromImage(qImg)
        print(self.mPixmap)
        self.label.setPixmap(self.mPixmap)
        self.canvas.resize(self.mPixmap.width(), self.mPixmap.height())
        self.image_Path = imagePath
    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        print("hihi")
    def mouseReleaseEvent(self, event):
        self.flag = False
    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
    def Ex(self):
        dataset = tf.data.Dataset.from_tensor_slices()
        unet = keras.models.load_model(filepath='\\FinalDocuments\\Trained_models\\UNET_b_160_IOU.h5')
        vgg = keras.models.load_model(filepath='\\FinalDocuments\\Trained_models\\VGG8_160_IOU.h5')

    def get_unet():
        print("hihi")
        # Contracting Path
        c1 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(input_img)
        c1 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c1)
        p1 = MaxPooling2D((2, 2))(c1)

        c2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p1)
        c2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c2)
        p2 = MaxPooling2D((2, 2))(c2)

        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p2)
        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c3)
        p3 = MaxPooling2D((2, 2))(c3)

        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p3)
        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c4)
        d4 = Dropout(0.5)(c4)
        p4 = MaxPooling2D((2, 2))(d4)

        c5 = Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p4)
        c5 = Conv2D(1024, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c5)
        d5 = Dropout(0.5)(c5)

        up6 = Conv2D(512, 2, activation='relu', padding='same', kernel_initializer='he_normal')(UpSampling2D(size=(2, 2))(d5))
        m6 = concatenate([d4, up6], axis=3)
        c6 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(m6)
        c6 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c6)

        up7 = Conv2D(256, 2, activation='relu', padding='same', kernel_initializer='he_normal')(UpSampling2D(size=(2, 2))(c6))
        m7 = concatenate([c3, up7], axis=3)
        c7 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(m7)
        c7 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c7)

        up8 = Conv2D(128, 2, activation='relu', padding='same', kernel_initializer='he_normal')(UpSampling2D(size=(2, 2))(c7))
        m8 = concatenate([c2, up8], axis=3)
        c8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(m8)
        c8 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c8)

        up9 = Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(UpSampling2D(size=(2, 2))(c8))
        m9 = concatenate([c1, up9], axis=3)
        c9 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(m9)
        c9 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c9)

        output_img = Conv2D(1, (1, 1), activation='sigmoid')(c9)
        print("hihi")
        model = Model(inputs=[input_img], outputs=[output_img])
        return output_img

    def get_vgg8():
        c1 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(input_img)

        p1 = MaxPooling2D((2,2))(c1)
        c2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p1)

        p2 = MaxPooling2D((2, 2))(c2)
        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p2)

        p3 = MaxPooling2D((2, 2))(c3)
        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p3)
        d4 = Dropout(0.5)(c4)

        p4 = MaxPooling2D((2, 2))(d4)
        c5 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p4)
        d5 = Dropout(0.5)(c5)

        p5 = MaxPooling2D((2, 2))(d5)
        f1 = Flatten()(p5)
        fe6 = Dense(units=4096, activation="relu")(f1)
        d6 = Dropout(0.5)(fe6)

        fe7 = Dense(units=4096, activation="relu")(d6)
        d7 = Dropout(0.5)(fe7)
        return
    def get_vgg11():
        c1 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(input_img)

        p1 = MaxPooling2D((2,2))(c1)
        c2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p1)

        p2 = MaxPooling2D((2, 2))(c2)
        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p2)
        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c3)

        p3 = MaxPooling2D((2, 2))(c3)
        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p3)
        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c4)
        d4 = Dropout(0.5)(c4)

        p4 = MaxPooling2D((2, 2))(d4)
        c5 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p4)
        c5 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c5)
        d5 = Dropout(0.5)(c5)

        p5 = MaxPooling2D((2, 2))(d5)
        f1 = Flatten()(p5)
        fe6 = Dense(units=4096, activation="relu")(f1)
        d6 = Dropout(0.5)(fe6)

        fe7 = Dense(units=4096, activation="relu")(d6)
        d7 = Dropout(0.5)(fe7)
        return

    def get_vgg16():
        c1 = Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(input_img)

        p1 = MaxPooling2D((2, 2))(c1)
        c2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p1)
        c2 = Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c2)

        p2 = MaxPooling2D((2, 2))(c2)
        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p2)
        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c3)
        c3 = Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c3)

        p3 = MaxPooling2D((2, 2))(c3)
        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p3)
        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c4)
        c4 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c4)
        d4 = Dropout(0.5)(c4)

        p4 = MaxPooling2D((2, 2))(d4)
        c5 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(p4)
        c5 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c5)
        c5 = Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(c5)
        d5 = Dropout(0.5)(c5)

        p5 = MaxPooling2D((2, 2))(d5)
        f1 = Flatten()(p5)
        fe6 = Dense(units=4096, activation="relu")(f1)
        d6 = Dropout(0.5)(fe6)

        fe7 = Dense(units=4096, activation="relu")(d6)
        d7 = Dropout(0.5)(fe7)
        return
def main():

    app = QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
