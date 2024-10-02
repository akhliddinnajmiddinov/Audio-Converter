from PyQt5 import QtCore, QtGui, QtWidgets
from pydub import AudioSegment
from math import ceil
import shutil
import os

class Widget(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)


        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.select1 = QtWidgets.QComboBox()
        self.select1.setEditable(False)
        self.select1.setMaxVisibleItems(4)
        self.select1.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.select1.addItem("Mp3")
        self.select1.addItem("Wav")
        self.select1.addItem("Ogg")
        self.horizontalLayout.addWidget(self.select1)

        self.image_label = QtWidgets.QLabel()
        self.image_label.setMaximumSize(QtCore.QSize(50, 16777215))
        self.image_label.setText("")
        self.image_label.setPixmap(QtGui.QPixmap("../../Downloads/icon.png"))
        self.horizontalLayout.addWidget(self.image_label)

        self.select2 = QtWidgets.QComboBox()
        self.select2.addItem("Wav")
        self.select2.addItem("Mp3")
        self.select2.addItem("Ogg")
        self.horizontalLayout.addWidget(self.select2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.file_label = QtWidgets.QLabel()
        self.file_label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_label.sizePolicy().hasHeightForWidth())
        self.file_label.setSizePolicy(sizePolicy)
        self.file_label.setTextFormat(QtCore.Qt.RichText)
        self.file_label.setScaledContents(False)
        self.file_label.setWordWrap(False)
        self.file_label.setOpenExternalLinks(False)
        self.file_label.setText("No file chosen")

        self.horizontalLayout_2.addWidget(self.file_label, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.open_file_button = QtWidgets.QPushButton()
        self.open_file_button.setText("Open file")
        self.open_file_button.clicked.connect(self.open_file)
        # self.open_file_button.setMaximumSize(QtCore.QSize(160, 16777215))
        self.horizontalLayout_2.addWidget(self.open_file_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.convert_button = QtWidgets.QPushButton()
        self.convert_button.setText("Convert->")
        self.convert_button.clicked.connect(self.convert_file)
        self.convert_button.setDisabled(True)
        self.verticalLayout.addWidget(self.convert_button)

        # self.pBar = QtWidgets.QProgressBar()
        # self.pBar.setMinimum(0)
        # self.pBar.setMaximum(100)
        # self.pBar.hide()
        # self.verticalLayout.addWidget(self.pBar)

        
        # self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self.save_file)
        self.save_button.hide()
        self.verticalLayout.addWidget(self.save_button)

        self.cancel_button = QtWidgets.QPushButton()
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(self.cancel_converting)
        self.cancel_button.hide()
        self.verticalLayout.addWidget(self.cancel_button)

        # self.horizontalLayout_3.addWidget(self.save_button, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        # self.horizontalLayout_3.addWidget(self.cancel_button, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        # self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.setLayout(self.verticalLayout)



        
    

    def open_file(self):
        try:
            os.remove(self.conMusicName)
        except:
            pass

        file = QtWidgets.QFileDialog.getOpenFileName(parent=None, caption="Open audio file", directory=os.curdir, filter=f"Audio Files(*.{self.select1.currentText().lower()}))")
        self.fileName = file[0]
        try:
            os.chdir(self.fileName.rsplit("/", 1)[0])
            self.convert_button.setDisabled(False)
            self.file_label.setText(self.fileName[:11] + "...")
        except:
            self.file_label.setText("No file chosen")
            self.convert_button.setDisabled(True)


    def convert_file(self):
        extension = self.select1.currentText().lower()
        try:
            pBar = QtWidgets.QProgressDialog("Converting", "Cancel", 0, 100)
            progress_bar = QtWidgets.QProgressBar(pBar)
            # progress_bar.setTextVisible(False)
            pBar.setBar(progress_bar)
            pBar.setWindowModality(QtCore.Qt.WindowModal)
            pBar.setModal(True) 
            pBar.setValue(0)
            pBar.show()

            if extension == "mp3":
                music = AudioSegment.from_mp3(self.fileName)
            elif extension == "wav":
                music = AudioSegment.from_wav(self.fileName)
            else:
                music = AudioSegment.from_ogg(self.fileName)
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error!!!")
            msg.setInformativeText("This audio doesn't meet the demand!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        
        extension2 = self.select2.currentText().lower()

        if extension != extension2:
            perFileName = self.fileName.rsplit(".", 1)[0] + "2." + extension2
            
            
            con_music = None
            dif = 1000
            i = -dif
            folder = self.fileName.rsplit("/", 1)[0]
            while i < len(music):
                i += dif
                print(i)
                chunk = music[i: i + dif]
                # play(chunk)
                chunkName = f"{folder}/{i//dif}.{extension2}"
                chunk.export(chunkName, extension2)
                
                if extension2 == "mp3":
                    con_chunk = AudioSegment.from_mp3(chunkName)
                elif extension2 == "wav":
                    con_chunk = AudioSegment.from_wav(chunkName)
                else:
                    con_chunk = AudioSegment.from_ogg(chunkName)
                try:
                    os.remove(chunkName)
                except:
                    pass

                if con_music == None:
                    con_music = con_chunk
                else:
                    con_music += con_chunk

                pBar.setValue(ceil(i / len(music) * 100))
                if pBar.wasCanceled():
                    return

            con_music.export(perFileName, extension2)
            self.conMusicName = perFileName
            self.convert_button.hide()
            self.save_button.show()
            self.cancel_button.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error!!!")
            msg.setInformativeText(f"Can not convert from {extension} to {extension2}!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def save_file(self):
        toFileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save audio file", os.curdir, f"Audio Files (*.{self.select2.currentText().lower()})")
        try:
            shutil.move(self.conMusicName, toFileName)
            self.parent.statusBar().showMessage("Saved!!!")
            self.cancel_converting()
        except:
            pass



    def cancel_converting(self):
        self.file_label.setText("No file chosen")
        self.convert_button.show()
        self.save_button.hide()
        self.cancel_button.hide()
        self.fileName = ""
        self.convert_button.setDisabled(True)
        os.remove(self.conMusicName)