from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QDialog, \
    QMessageBox, QLabel, QHBoxLayout
from data_processing.dataframe_handler import DataFrameHandler
from data_processing.regression_trainer import RegressionTrainer
from ui.file_dialog import FileDialog, CSVSettingsDialog
from db.database import Database
from data_processing.csv_handler import CSVHandler
from ui.missing_values_dialog import MissingValuesDialog
from ui.save_table_dialog import SaveTableDialog
from ui.load_table_dialog import LoadTableDialog
import pandas as pd

from ui.train_regression_dialog import TrainRegressionDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Работа с датасетом")
        self.setFixedSize(1080, 720)
        self.db = Database("mydatabase.db")  # Создаем базу данных

        self.csv_handler = CSVHandler()
        self.dataframe_handler = DataFrameHandler()

        self.load_button = None
        self.table_widget = None
        self.layout = None
        self.btn_layout = None
        self.info_widget = None
        self.info_text = None
        self.model_info_label = None

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.btn_layout = QHBoxLayout(central_widget)

        self.load_button = QPushButton("Загрузить датасет")
        self.load_button.clicked.connect(self.showFileDialog)
        self.layout.addWidget(self.load_button)

        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.layout.addWidget(self.table_widget)

        self.dataframe_handler = DataFrameHandler()  # Добавили

        remove_button = QPushButton("Удалить пропущенные значения")
        remove_button.clicked.connect(self.removeMissingValues)
        remove_button.setFixedSize(500, 30)
        self.layout.addWidget(remove_button)
        self.layout.setAlignment(remove_button, Qt.AlignRight)

        save_button = QPushButton("Сохранить в базу данных")
        save_button.clicked.connect(self.saveTableToDatabase)
        save_button.setFixedSize(500, 30)
        self.layout.addWidget(save_button)
        self.layout.setAlignment(save_button, Qt.AlignRight)

        load_button = QPushButton("Загрузить из базы данных")
        load_button.clicked.connect(self.loadTableFromDatabase)
        load_button.setFixedSize(500, 30)
        self.layout.addWidget(load_button)
        self.layout.setAlignment(load_button, Qt.AlignRight)

        train_button = QPushButton("Обучить модель регрессии")
        train_button.clicked.connect(self.trainRegressionModel)
        train_button.setFixedSize(500, 30)
        self.layout.addWidget(train_button)
        self.layout.setAlignment(train_button, Qt.AlignRight)

        self.model_info_label = QLabel("")  # Добавлено для отображения информации о модели
        self.layout.addWidget(self.model_info_label)
        # self.layout.setAlignment(self.model_info_label, Qt.AlignBottom | Qt.AlignRight)
        self.model_info_label.move(200, 200)

    def showFileDialog(self):
        dialog = FileDialog(self)
        if dialog.exec_() == FileDialog.Accepted:
            filepath = dialog.selectedFiles()[0]
            self.loadCSV(filepath)

    def loadCSV(self, filepath):
        dialog = CSVSettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            delimiter, has_header = dialog.get_settings()
            try:
                data = self.csv_handler.read_csv(filepath, delimiter, has_header)
                if data:
                    conn = self.db.get_connection()
                    df = self.dataframe_handler.create_dataframe(data, has_header)
                    column_names = df.columns.tolist()
                    self.db.create_table(column_names)
                    self.dataframe_handler.save_to_sql(df, conn)  # Сохраняем через DataFrame
                    self.displayData(data)

                    if self.info_widget:
                        self.layout.removeWidget(self.info_widget)
                        self.info_widget.deleteLater()
                        self.info_widget = None

                    self.info_text = self.dataframe_handler.get_info(df)
                    self.info_widget = self.dataframe_handler.display_info(self.info_text)
                    self.layout.addWidget(self.info_widget)
                    self.layout.setAlignment(self.info_widget, Qt.AlignTop | Qt.AlignLeft)

                    self.db.close()
                else:
                    print("Ошибка: CSV файл пустой или некорректный.")
            except Exception as e:
                print(f"Ошибка загрузки CSV: {e}")

    def displayData(self, data):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data[0]) if data else 0)
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                item_widget = QTableWidgetItem(str(item))
                item_widget.setTextAlignment(Qt.AlignCenter)  # Выравнивание текста
                self.table_widget.setItem(i, j, item_widget)

    def removeMissingValues(self):
        try:
            dialog = MissingValuesDialog(self.dataframe_handler.df.columns.tolist(), self)
        except Exception as e:
            print("Ошибка при удалении: ", e)
            return

        if dialog.exec_() == QDialog.Accepted:
            columns_to_remove, remove_all_rows = dialog.get_settings()
            try:
                conn = self.db.get_connection()
                new_df = self.dataframe_handler.remove_missing_values(columns_to_remove, remove_all_rows)
                self.dataframe_handler.df = new_df
                self.dataframe_handler.save_to_sql(new_df, conn)  # Сохраняем изменения в БД
                self.displayData(list([new_df.columns]) + new_df.values.tolist())  # Перерисовка таблицы

                if self.info_widget:
                    self.layout.removeWidget(self.info_widget)
                    self.info_widget.deleteLater()
                    self.info_widget = None

                self.info_text = self.dataframe_handler.get_info(new_df)
                self.info_widget = self.dataframe_handler.display_info(self.info_text)

                self.layout.addWidget(self.info_widget)
                self.layout.setAlignment(self.info_widget, Qt.AlignTop | Qt.AlignLeft)

                self.db.close()

            except Exception as e:
                print(f"Ошибка при удалении пропущенных значений: {e}")

    def saveTableToDatabase(self):
        if self.dataframe_handler is None:
            return
        dialog = SaveTableDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            table_name = dialog.get_table_name()
            if table_name:
                try:
                    conn = self.db.get_connection()
                    self.dataframe_handler.save_to_sql(self.dataframe_handler.df, conn,
                                                       table_name=table_name)
                    QMessageBox.information(self, "Успех", f"Таблица '{table_name}' успешно сохранена.")
                    self.db.close()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения таблицы: {e}")

    def loadTableFromDatabase(self):
        dialog = LoadTableDialog(self.db.db_name, self)
        if dialog.exec_() == QDialog.Accepted:
            table_name = dialog.get_selected_table()
            if table_name:
                try:
                    conn = self.db.get_connection()
                    new_df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    self.dataframe_handler.df = new_df
                    self.displayData(new_df.values.tolist())

                    if self.info_widget:
                        self.layout.removeWidget(self.info_widget)
                        self.info_widget.deleteLater()
                        self.info_widget = None

                    self.info_text = self.dataframe_handler.get_info(new_df)
                    self.info_widget = self.dataframe_handler.display_info(self.info_text)

                    self.layout.addWidget(self.info_widget)
                    self.layout.setAlignment(self.info_widget, Qt.AlignTop | Qt.AlignLeft)
                    self.db.close()

                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки таблицы: {e}")

    def trainRegressionModel(self):
        if self.dataframe_handler is None:
            return
        dialog = TrainRegressionDialog(self.dataframe_handler.df.columns.tolist(), self)
        if dialog.exec_() == QDialog.Accepted:
            target_column, test_size, model_name = dialog.get_settings()
            try:
                trainer = RegressionTrainer()
                model_name, accuracy, mae, mse, rmse = trainer.train_model(self.dataframe_handler.df, target_column, test_size,
                                                           model_name)
                self.model_info_label.setText(f"Модель: {model_name}\n"
                                              f"Точность: {accuracy:.4f}\nMAE: {mae}\nMSE: {mse}\nRMSE: {rmse}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка обучения модели: {e}")