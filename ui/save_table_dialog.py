from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout


class SaveTableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Сохранение таблицы")
        self.table_name = ""

        layout = QVBoxLayout()
        label = QLabel("Введите имя таблицы:")
        layout.addWidget(label)

        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def get_table_name(self):
        self.table_name = self.line_edit.text()
        return self.table_name
