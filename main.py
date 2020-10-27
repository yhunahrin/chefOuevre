import sys
import h5py
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QLabel, QMenu, QMenuBar, QAction,QFileDialog,QGroupBox,QVBoxLayout
from PyQt5.QtGui import QIcon,QPixmap
from tensorflow import keras
import tensorflow as tf
import os
import numpy as np
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras import backend as keras
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
        save = QAction("Save..", self)
        save.setShortcut("Ctrl+S")
        file.addAction(save)
        saveAs = QAction("SaveAs..", self)
        saveAs.triggered.connect(self.saveAs)
        file.addAction(saveAs)
    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        print(imagePath)
        self.pixmap = QPixmap(imagePath)
        self.label.setPixmap( self.pixmap)
        self.canvas.resize( self.pixmap.width(),  self.pixmap.height())
        return imagePath
    def saveImage(self):
        imagePath = self.openImage()
        if imagePath == "":
            return
        self.pixmap.save(imagePath)
    def saveAs(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "BMP(*.bmp);;PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        self.pixmap.save(filePath)

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

def main():

    app = QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
    im_color = cv.imread("lena.png", cv.IMREAD_COLOR)
    im_gray = cv.cvtColor(im_color, cv.COLOR_BGR2GRAY)
    _, mask = cv.threshold(im_gray, thresh=180, maxval=255, type=cv.THRESH_BINARY)
    cv.imshow("binary mask", mask)
if __name__ == '__main__':
    main()
