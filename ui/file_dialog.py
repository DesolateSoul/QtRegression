from PyQt5.QtWidgets import (QFileDialog,
QDialog, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout)


class FileDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Open CSV File", "", "CSV Files (*.csv)")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setAcceptMode(QFileDialog.AcceptOpen)


class CSVSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки CSV")
        self.delimiter = ',' # Значение по умолчанию
        self.has_header = True # Значение по умолчанию

        layout = QVBoxLayout()

        delimiter_layout = QHBoxLayout()
        delimiter_label = QLabel("Разделитель:")
        self.delimiter_edit = QLineEdit(self.delimiter)
        delimiter_layout.addWidget(delimiter_label)
        delimiter_layout.addWidget(self.delimiter_edit)
        layout.addLayout(delimiter_layout)

        self.header_checkbox = QCheckBox("Наличие заголовка")
        self.header_checkbox.setChecked(self.has_header)
        layout.addWidget(self.header_checkbox)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_settings(self):
        self.delimiter = self.delimiter_edit.text()
        self.has_header = self.header_checkbox.isChecked()
        return self.delimiter, self.has_header