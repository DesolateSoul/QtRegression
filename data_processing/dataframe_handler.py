import io

import pandas as pd
from PyQt5.QtWidgets import QTextEdit

class DataFrameHandler:
    def __init__(self):
        self.df = None

    def create_dataframe(self, data, has_header=True):
        if has_header:
            self.df = pd.DataFrame(data[1:], columns=data[0])
        else:
            self.df = pd.DataFrame(data, columns=[f"C{i}" for i in range(len(data[0]))])
        return self.df

    def get_info(self, df):
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_text = "\n".join(buffer.getvalue().split('\n')[2:])
        buffer.close()
        return info_text

    def display_info(self, info_text):
        info_widget = QTextEdit()
        info_widget.setReadOnly(True)
        info_widget.setText(info_text)
        return info_widget

    def save_to_sql(self, df, db_connection, table_name="mydata"):
        try:
            df.to_sql(table_name, db_connection, if_exists='replace',
                      index=False)  # index=False предотвращает добавление индекса в таблицу
        except Exception as e:
            print(f"Ошибка сохранения в базу данных: {e}")

    def remove_missing_values(self, columns_to_remove, remove_all_rows):
        df = self.df.copy()
        if columns_to_remove:
            df = df.drop(columns=columns_to_remove)
        if remove_all_rows:
            df = df.dropna()
        return df
