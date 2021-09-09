
import os
from pathlib import Path

import imagej
import numpy as np
import configparser
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog
from sbxreader import sbx_get_metadata, sbx_memmap


class Ui_Dialog(object):
    def load_ini(self):
        '''
        Load/Create ini settings file
        '''
        self.ini_path = Path(os.path.expanduser("~") + "/.config/sbx2imagej.ini")
        try:
            if not os.path.isfile(self.ini_path):
                os.makedirs(self.ini_path.parent, exist_ok=True)
                config = configparser.ConfigParser()
                config.add_section('settings')
                config['settings']['imagej'] = 'default'
                config['settings']['directory'] = 'None'
                config['settings']['first_run'] = 'yes'
                with open(self.ini_path, 'w') as f:
                    config.write(f)
            
            config = configparser.ConfigParser()
            config.read(self.ini_path)
            self.directory = None if config['settings']['directory'] == 'None' else config['settings']['directory']
            self.ij = None if config['settings']['imagej'] == 'default' else config['settings']['imagej']
            self.first_run = config['settings']['first_run']
        except Exception as e:
            #print(e)
            print("Could not Read/save settings")
            self.directory = None
            self.ij = None
            self.ij = 'no'

    def save_config(self, ij=[], directory=[], first_run = []):
        try:
            config = configparser.ConfigParser()
            config.read(self.ini_path)
            if ij != []:
                config['settings']['imagej'] = ij
            if directory != []:
                config['settings']['directory'] = directory
            if first_run != []:
                config['settings']['first_run'] = 'no'
            with open(self.ini_path, 'w') as f:
                config.write(f)
        except:
            print("Could not read/Save settings")


    def setupUi(self, Dialog):
        '''
        create the gui
        '''
        Dialog.setObjectName("Dialog")
        Dialog.resize(378, 252)
        self.FileName = QtWidgets.QLabel(Dialog)
        self.FileName.setGeometry(QtCore.QRect(5, 3, 221, 20))
        self.FileName.setObjectName("FileName")
        self.FileName.setText("Filename")


        self.ToImageJ = QtWidgets.QPushButton(Dialog)
        self.ToImageJ.setGeometry(QtCore.QRect(10, 200, 101, 28))
        self.ToImageJ.setObjectName("ToImageJ")
        self.ToImageJ.setText("To Imagej")

        self.ChangeFile = QtWidgets.QPushButton(Dialog)
        self.ChangeFile.setGeometry(QtCore.QRect(120, 200, 101, 28))
        self.ChangeFile.setObjectName("ChangeFile")
        self.ChangeFile.setText("Change File")

        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(240, 204, 118, 20))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.Info = QtWidgets.QLabel(Dialog)
        self.Info.setGeometry(QtCore.QRect(10, 227, 361, 25))
        self.Info.setText("")
        self.Info.setObjectName("Info")
        self.Info.setAlignment(QtCore.Qt.AlignTop)

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 30, 351, 165))
        self.widget.setObjectName("widget")
        
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.Frames_text = QtWidgets.QLabel(self.widget)
        self.Frames_text.setObjectName("Frames_text")
        self.Frames_text.setText("Frames")

        self.gridLayout.addWidget(self.Frames_text, 0, 0, 1, 1)
        self.Frames_start = QtWidgets.QLineEdit(self.widget)
        self.Frames_start.setObjectName("Frames_start")
        self.gridLayout.addWidget(self.Frames_start, 0, 1, 1, 1)
        
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("to")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        
        self.Frames_end = QtWidgets.QLineEdit(self.widget)
        self.Frames_end.setObjectName("Frames_end")
        self.gridLayout.addWidget(self.Frames_end, 0, 3, 1, 1)
        
        self.Channels_text = QtWidgets.QLabel(self.widget)
        self.Channels_text.setObjectName("Channels_text")
        self.Channels_text.setText("Channels")
        self.gridLayout.addWidget(self.Channels_text, 1, 0, 1, 1)

        self.Channels = QtWidgets.QLineEdit(self.widget)
        self.Channels.setObjectName("Channels")
        self.gridLayout.addWidget(self.Channels, 1, 1, 1, 1)
        
        self.Planes_text = QtWidgets.QLabel(self.widget)
        self.Planes_text.setObjectName("Planes_text")
        self.Planes_text.setText("Planes")
        self.gridLayout.addWidget(self.Planes_text, 2, 0, 1, 1)
        
        self.Planes = QtWidgets.QLineEdit(self.widget)
        self.Planes.setObjectName("Planes")
        self.gridLayout.addWidget(self.Planes, 2, 1, 1, 1)
        
        self.Height_text = QtWidgets.QLabel(self.widget)
        self.Height_text.setObjectName("Height_text")
        self.Height_text.setText("Height")
        self.gridLayout.addWidget(self.Height_text, 3, 0, 1, 1)
        
        self.Height = QtWidgets.QLineEdit(self.widget)
        self.Height.setObjectName("Height")
        self.gridLayout.addWidget(self.Height, 3, 1, 1, 1)
        
        self.Width_text = QtWidgets.QLabel(self.widget)
        self.Width_text.setObjectName("Width_text")
        self.Width_text.setText("Width")
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

        #self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        
        self.Dialog = Dialog
        Dialog.setWindowTitle("SBX to ImageJ")

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

        self.save_config(directory=self.directory)
        return

    def load_file(self):
        '''
        Load file dialog
        '''
        dlg = QFileDialog()
        self.filepath = ''
        while not self.filepath.endswith('sbx'):
            self.filepath = dlg.getOpenFileName(self.Dialog, 'Choose an sbx file to load to ImageJ', self.directory, "SBX Files (*.sbx)")[0]

        self.set_metadata()
        self.progressBar.hide()
        self.Info.setText("")


    def show_imagej(self):
        '''
        Main function that load the sbx file and transfer it to imagej
        '''
        progress_bar = 1 # TODO: add the ability to not show the progress bar      
        
        self.Info.setText("Loading sbx file, please wait...")
        sbx_dat = sbx_memmap(self.filepath)



        #load file to numpy array
        frame_st = int(self.Frames_start.text())
        frame_en = int(self.Frames_end.text())

        step_size = int((frame_en-frame_st)/20) 

        if progress_bar:
            loaded_data = np.zeros((frame_en-frame_st, int(self.Planes.text()), int(self.Channels.text()), int(self.Height.text()), int(self.Width.text())))
            self.progressBar.show()
            for j,ind in enumerate(range(frame_st,frame_en,step_size)):
                self.progressBar.setValue(max(j*step_size-3,0)/(frame_en-frame_st)*100)
                QApplication.processEvents()
                loaded_data[j*step_size:min((j+1)*step_size, loaded_data.shape[0])] = sbx_dat[ind:min(ind+step_size,frame_en)]
            
            self.Info.setText('Changing datatype')
            self.Info.repaint()
            self.progressBar.setValue(98)
        else:
            loaded_data = sbx_dat[frame_st:frame_en]
        
        self.Info.setText('Loading ImageJ, please wait...')
        self.Info.repaint()
        if self.first_run == 'yes':
            self.Info.setText('First initialization! Will take a few minutes...')
            self.Info.repaint()

        if self.ij==None:
            self.ij = imagej.init('net.imagej:imagej:2.2.0+net.imglib2:imglib2-unsafe:0.4.1',headless=False)
            self.ij.ui().showUI()
            self.progressBar.setValue(99)
        self.Info.setText("Mirroring data to ImageJ")
        self.Info.repaint()
        
        #convert to imagej
        self.ij.ui().show(self.filename, self.ij.py.to_java(loaded_data))
        self.Info.setText("Done")
        self.progressBar.setValue(100)

        self.save_config(first_run='no')



def main():
    app = QtWidgets.QApplication([])
    Dialog = QtWidgets.QDialog()
    ut = Ui_Dialog()
    ut.load_ini()
    ut.setupUi(Dialog)

    ut.ToImageJ.clicked.connect(ut.show_imagej)
    ut.ChangeFile.clicked.connect(ut.load_file)
    ut.load_file()

    Dialog.show()
    app.exec()

if __name__ == '__main__':
    main()

