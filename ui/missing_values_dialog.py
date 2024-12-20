from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt

class MissingValuesDialog(QDialog):
    def __init__(self, column_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удаление пропущенных значений")
        self.columns_to_remove = []
        self.remove_all_rows = False

        layout = QVBoxLayout()

        label = QLabel("Выберите столбцы для удаления:")
        layout.addWidget(label)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.addItems(column_names)
        layout.addWidget(self.list_widget)

        self.remove_all_rows_checkbox = QCheckBox("Удалить все строки с пропущенными значениями")
        layout.addWidget(self.remove_all_rows_checkbox)

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
        for item in self.list_widget.selectedItems():
            self.columns_to_remove.append(item.text())
        self.remove_all_rows = self.remove_all_rows_checkbox.isChecked()
        return self.columns_to_remove, self.remove_all_rows
