
from pathlib import Path

import imagej
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QApplication
from sbxreader import sbx_get_metadata, sbx_memmap


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        '''
        create the gui
        '''
        Dialog.setObjectName("Dialog")
        Dialog.resize(378, 252)
        self.FileName = QtWidgets.QLabel(Dialog)
        self.FileName.setGeometry(QtCore.QRect(5, 3, 221, 20))
        self.FileName.setObjectName("FileName")
        self.ToImageJ = QtWidgets.QPushButton(Dialog)
        self.ToImageJ.setGeometry(QtCore.QRect(10, 200, 101, 28))
        self.ToImageJ.setObjectName("ToImageJ")
        self.ChangeFile = QtWidgets.QPushButton(Dialog)
        self.ChangeFile.setGeometry(QtCore.QRect(120, 200, 101, 28))
        self.ChangeFile.setObjectName("ChangeFile")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(240, 204, 118, 20))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.Info = QtWidgets.QLabel(Dialog)
        self.Info.setGeometry(QtCore.QRect(10, 230, 341, 20))
        self.Info.setText("")
        self.Info.setObjectName("Info")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 30, 351, 165))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Frames_text = QtWidgets.QLabel(self.widget)
        self.Frames_text.setObjectName("Frames_text")
        self.gridLayout.addWidget(self.Frames_text, 0, 0, 1, 1)
        self.Frames_start = QtWidgets.QLineEdit(self.widget)
        self.Frames_start.setObjectName("Frames_start")
        self.gridLayout.addWidget(self.Frames_start, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.Frames_end = QtWidgets.QLineEdit(self.widget)
        self.Frames_end.setObjectName("Frames_end")
        self.gridLayout.addWidget(self.Frames_end, 0, 3, 1, 1)
        self.Channels_text = QtWidgets.QLabel(self.widget)
        self.Channels_text.setObjectName("Channels_text")
        self.gridLayout.addWidget(self.Channels_text, 1, 0, 1, 1)
        self.Channels = QtWidgets.QLineEdit(self.widget)
        self.Channels.setObjectName("Channels")
        self.gridLayout.addWidget(self.Channels, 1, 1, 1, 1)
        self.Planes_text = QtWidgets.QLabel(self.widget)
        self.Planes_text.setObjectName("Planes_text")
        self.gridLayout.addWidget(self.Planes_text, 2, 0, 1, 1)
        self.Planes = QtWidgets.QLineEdit(self.widget)
        self.Planes.setObjectName("Planes")
        self.gridLayout.addWidget(self.Planes, 2, 1, 1, 1)
        self.Height_text = QtWidgets.QLabel(self.widget)
        self.Height_text.setObjectName("Height_text")
        self.gridLayout.addWidget(self.Height_text, 3, 0, 1, 1)
        self.Height = QtWidgets.QLineEdit(self.widget)
        self.Height.setObjectName("Height")
        self.gridLayout.addWidget(self.Height, 3, 1, 1, 1)
        self.Width_text = QtWidgets.QLabel(self.widget)
        self.Width_text.setObjectName("Width_text")
        self.gridLayout.addWidget(self.Width_text, 4, 0, 1, 1)
        self.Width = QtWidgets.QLineEdit(self.widget)
        self.Width.setObjectName("Width")
        self.gridLayout.addWidget(self.Width, 4, 1, 1, 1)

        ## grayout Planes, Channels, Width, Height
        self.Planes.setEnabled(False)
        self.Channels.setEnabled(False)
        self.Width.setEnabled(False)
        self.Height.setEnabled(False)
        self.ToImageJ.setEnabled(False)
        self.progressBar.hide()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.directory = None
        self.ij = None
        
        self.Dialog = Dialog
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.FileName.setText(_translate("Dialog", "Filename"))
        self.ChangeFile.setText(_translate("Dialog", "Change File"))
        self.ToImageJ.setText(_translate("Dialog", "To Imagej"))
        self.Frames_text.setText(_translate("Dialog", "Frames"))
        self.label_2.setText(_translate("Dialog", "to"))
        self.Channels_text.setText(_translate("Dialog", "Channels"))
        self.Planes_text.setText(_translate("Dialog", "Planes"))
        self.Height_text.setText(_translate("Dialog", "Height"))
        self.Width_text.setText(_translate("Dialog", "Width"))



    def set_metadata(self):
        '''
        Sets the gui metadata from the sbxinfo
        '''

        
        self.directory = str(Path(self.filepath).parent)
        self.filename = str(Path(self.filepath).name)
        metadata = sbx_get_metadata(self.filepath)


        #set textboxes:
        self.Frames_start.setText('0')
        self.Frames_end.setText(str(metadata['num_frames']))
        self.Planes.setText(str(metadata['num_planes']))
        self.Channels.setText(str(metadata['num_channels']))
        self.Width.setText(str(metadata['frame_size'][1]))
        self.Height.setText(str(metadata['frame_size'][0]))

        self.FileName.setText(self.filename)
        self.ToImageJ.setEnabled(True)

        return

    def load_file(self):
        '''
        Load file dialog
        '''
        dlg = QFileDialog()

        self.filepath = dlg.getOpenFileName(self.Dialog, 'Choose an sbx file to load to ImageJ', self.directory, "SBX Files (*.sbx)")[0]

        self.set_metadata()
        self.progressBar.hide()
        self.Info.setText("")


    def show_imagej(self):
        '''
        Main function that load the sbx file and transfer it to imagej
        '''
        progress_bar = 1 # TODO: add the ability to not show the progress bar      
        
        self.Info.setText("loading sbx file, please wait...")
        sbx_dat = sbx_memmap(self.filepath)

        load_step = min(50,sbx_dat.shape[0]) # TODO: think about a better heuristic for load_step


        #load file to numpy array
        frame_st = int(self.Frames_start.text())
        frame_en = int(self.Frames_end.text())
        
        if progress_bar:
            loaded_data = np.zeros((frame_en-frame_st, int(self.Planes.text()), int(self.Channels.text()), int(self.Height.text()), int(self.Width.text())))
            self.progressBar.show()
            for ind in range(frame_st,frame_en,load_step):
                self.progressBar.setValue(max(ind-3,0)/(frame_en-frame_st)*100)
                QApplication.processEvents()
                loaded_data[ind:min(ind+load_step,frame_en)] = sbx_dat[ind:min(ind+load_step,frame_en)]
            
            self.Info.setText('change datatype')
            self.Info.repaint()
            self.progressBar.setValue(98)
        else:
            loaded_data = sbx_dat[frame_st:frame_en]
        
        self.Info.setText('finished loading sbx, loading imagej')
        self.Info.repaint()

        if self.ij==None:
            self.ij = imagej.init('net.imagej:imagej:2.2.0+net.imglib2:imglib2-unsafe:0.4.1',headless=False)
            self.ij.ui().showUI()
            self.progressBar.setValue(99)
        self.Info.setText("mirroring data to image, please wait")
        self.Info.repaint()
        
        #convert to imagej
        self.ij.ui().show(self.filename, self.ij.py.to_java(loaded_data))
        self.Info.setText("Done")
        self.progressBar.setValue(100)



def main():
    app = QtWidgets.QApplication([])
    Dialog = QtWidgets.QDialog()
    ut = Ui_Dialog()
    ut.setupUi(Dialog)

    ut.ToImageJ.clicked.connect(ut.show_imagej)
    ut.ChangeFile.clicked.connect(ut.load_file)
    ut.load_file()

    Dialog.show()
    app.exec()

if __name__ == '__main__':
    main()


