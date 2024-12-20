from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import pandas as pd


class TrainRegressionDialog(QDialog):
    def __init__(self, column_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Обучение модели регрессии")
        self.target_column = ""
        self.test_size = 0.2
        self.model_name = ""

        layout = QVBoxLayout()

        label_target = QLabel("Выберите целевой столбец:")
        layout.addWidget(label_target)
        self.combo_target = QComboBox()
        self.combo_target.addItems(column_names)
        layout.addWidget(self.combo_target)

        label_test = QLabel("Размер тестовой выборки (%):")
        layout.addWidget(label_test)
        self.spin_test = QSpinBox()
        self.spin_test.setRange(1, 99)
        self.spin_test.setValue(20)
        layout.addWidget(self.spin_test)

        label_model = QLabel("Выберите модель:")
        layout.addWidget(label_model)
        self.combo_model = QComboBox()
        self.combo_model.addItems(["LinearRegression", "DecisionTreeRegressor", "RandomForestRegressor"]) # Добавить другие модели по необходимости
        layout.addWidget(self.combo_model)


        button_layout = QHBoxLayout()
        ok_button = QPushButton("Обучить")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_settings(self):
        self.target_column = self.combo_target.currentText()
        self.test_size = self.spin_test.value() / 100.0
        self.model_name = self.combo_model.currentText()
        return self.target_column, self.test_size, self.model_name
