from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
from sbxreader import sbx_get_metadata, sbx_memmap
from tqdm.auto import tqdm,trange
import numpy as np

def test_dialog():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        return filenames


def show_imagej(file_path):
    
    print("loading sbx file, please wait...")
    sbx_dat = sbx_memmap(file_path)
    
    if progress_bar:
        loaded_data = []
        for ind in trange(len(sbx_dat)):#chunking did increase speed
            loaded_data.append(sbx_dat[ind])
        loaded_data = np.array(loaded_data)
    else:
        loaded_data = np.array(sbx_dat[:])
    
    print('finished loading sbx, loading imagej')
    
    import imagej
    ij = imagej.init(headless=False)
    ij.ui().showUI()
    
    print("mirroring data to image")
    ij.ui().show(file_path, ij.py.to_java(loaded_data))
    
    

if __name__ == '__main__':
    progress_bar = True # ~3x faster with false, can probably fix it.
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    filename = test_dialog()
    assert len(filename)==1, 'Please select a single file'
    assert filename[0].endswith('.sbx'), 'File extension must be sbx'
    
    if 1:
        show_imagej(filename[0])


