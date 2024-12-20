from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import sqlite3


class LoadTableDialog(QDialog):
    def __init__(self, db_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Загрузка таблицы")
        self.selected_table = ""
        self.db_name = db_name

        layout = QVBoxLayout()
        label = QLabel("Выберите таблицу:")
        layout.addWidget(label)

        self.combo_box = QComboBox()
        self.populate_combo_box()
        layout.addWidget(self.combo_box)

        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def populate_combo_box(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
        self.combo_box.addItems(tables)
        conn.close()

    def get_selected_table(self):
        self.selected_table = self.combo_box.currentText()
        return self.selected_table
