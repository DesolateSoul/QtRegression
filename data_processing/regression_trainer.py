import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, root_mean_squared_error
from sklearn.preprocessing import StandardScaler


class RegressionTrainer:
    def train_model(self, df, target_column, test_size, model_name):
        X = df.drop(columns=[target_column])
        y = df[target_column]

        #Масштабирование данных
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        if model_name == "LinearRegression":
            model = LinearRegression()
        elif model_name == "DecisionTreeRegressor":
            model = DecisionTreeRegressor(random_state=42)
        elif model_name == "RandomForestRegressor":
            model = RandomForestRegressor(random_state=42)
        else:
            raise ValueError("Неизвестная модель")

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = root_mean_squared_error(y_test, y_pred)
        return model_name, accuracy, mae, mse, rmse
