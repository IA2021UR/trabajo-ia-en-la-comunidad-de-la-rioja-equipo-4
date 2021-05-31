import os
import sys
from threading import Thread
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5 import QtCore
from pathlib import Path

from aplicacion.view import MainScreen

from deoldify.visualize import get_image_colorizer


class ColorThread(QtCore.QThread):
    image = QtCore.pyqtSignal(str)
    end = QtCore.pyqtSignal(list)

    def __init__(self, images, colorizer, folder):
        QtCore.QThread.__init__(self)
        self.images = images
        self.colorizer = colorizer
        self.folder = folder

    def run(self):
        image_paths = []
        for index, image in enumerate(self.images):
            render_factor = 30
            path = Path(os.path.normpath(self.folder))
            image_path = self.colorizer.plot_transformed_image(path=image, render_factor=render_factor, compare=True,
                                                               watermarked=False, results_dir=path)

            self.image.emit(str(image_path))
            image_paths.append(str(image_path))

        self.end.emit(image_paths)


class MainWindow(QtWidgets.QMainWindow, MainScreen):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.btn_procesar.setDisabled(True)
        self.btn_carga.clicked.connect(self.on_click_load_files)
        self.btn_destino.clicked.connect(self.on_click_select_dir)
        self.btn_procesar.clicked.connect(self.on_click_procesar)

        # Imagenes a procesar
        self.imgs = []

        # Imagenes a color path
        self.imgs_color = []

        # Directorio destino
        self.folder = './'

        # Modelos
        self.colorizer = get_image_colorizer(artistic=True)

    def image_processed(self, image):
        self.imgs_color.append(image)
        self.progress_bar_tratamiento.setProperty("value", (100 * len(self.imgs_color)) / len(self.imgs))

    def image_processed_end(self, paths):
        self.btn_procesar.setDisabled(False)
        self.btn_destino.setDisabled(False)
        self.btn_carga.setDisabled(False)

        for index, image in enumerate(paths):
            self.tabla_procesado.insertRow(index)
            self.tabla_procesado.setItem(index, 0, QtWidgets.QTableWidgetItem(os.path.basename(image)))
            self.tabla_procesado.setItem(index, 1, QtWidgets.QTableWidgetItem(str(image)))
        sleep(0.5)
        self.tabla_procesado.model().layoutChanged.emit()

    def on_click_procesar(self):

        self.btn_procesar.setDisabled(True)
        self.btn_destino.setDisabled(True)
        self.btn_carga.setDisabled(True)

        thread = ColorThread(self.imgs, self.colorizer, self.folder)
        thread.image.connect(self.image_processed)
        thread.end.connect(self.image_processed_end)
        sleep(1)
        thread.start()
        sleep(1)

    def on_click_load_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        dialog = QFileDialog()
        dialog.setOptions(options)

        dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)

        dialog.setFileMode(QFileDialog.ExistingFiles)

        dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if dialog.exec_() == QDialog.Accepted:
            rows = int(self.tableWidget.rowCount())

            for index, file in enumerate(dialog.selectedFiles()):
                row_position = index + rows
                self.tableWidget.insertRow(row_position)
                self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(os.path.basename(file)))
                self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(file))

                self.imgs.append(file)
            self.tableWidget.model().layoutChanged.emit()

    def on_click_select_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        dialog = QFileDialog()
        dialog.setOptions(options)

        dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)

        dialog.setFileMode(QFileDialog.DirectoryOnly)

        dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if dialog.exec_() == QDialog.Accepted:
            self.folder = dialog.selectedFiles()[0]
            self.label_destino.setText("Destino: " + str(self.folder))
            self.btn_procesar.setDisabled(False)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
