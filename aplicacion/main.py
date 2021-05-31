import os
import sys
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5 import QtCore
from pathlib import Path

from aplicacion.view import MainScreen

from deoldify.visualize import get_image_colorizer


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

    def on_click_procesar(self):

        image_size = len(self.imgs)
        self.btn_procesar.setDisabled(True)
        self.btn_destino.setDisabled(True)
        self.btn_carga.setDisabled(True)
        for index, image in enumerate(self.imgs):
            render_factor = 30
            path = Path(os.path.normpath(self.folder))
            image_path = self.colorizer.plot_transformed_image(path=image, render_factor=render_factor, compare=True,
                                                               watermarked=False, results_dir=path)

            # Actualizamos barra de progreso
            self.progress_bar_tratamiento.setProperty("value", (100 * (index + 1)) / image_size)
            # Actualizamos tabla
            self.tabla_procesado.insertRow(index)
            self.tabla_procesado.setItem(index, 0, QtWidgets.QTableWidgetItem(os.path.basename(image_path)))
            self.tabla_procesado.setItem(index, 1, QtWidgets.QTableWidgetItem(image_path))
            self.tabla_procesado.model().layoutChanged.emit()

        self.btn_procesar.setDisabled(False)
        self.btn_destino.setDisabled(False)
        self.btn_carga.setDisabled(False)

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
