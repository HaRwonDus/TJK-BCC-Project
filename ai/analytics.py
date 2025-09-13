import pandas as pd
from pathlib import Path

class Analytics:
    def __init__(self, data_input_path="data-input", data_output_path="data-output"):
        self.data_input_path = Path(data_input_path)
        self.data_output_path = Path(data_output_path)

    def load_csv(self, filename):
        """Загрузка датасета"""
        file_path = self.data_input_path / filename
        return pd.read_csv(file_path)

    def clean_data(self, df, date_col="date", amount_col="amount"):
        """Очистка датасета"""
        df = df.dropna()  # убираем пустые строки
        df = df.drop_duplicates()
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        if amount_col in df.columns:
            df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
            df = df[df[amount_col] > 0]  # убираем отрицательные/нулевые транзакции
        return df

    def analyze_client(self, client_code):
        """Аналитика по конкретному клиенту"""
        transfers = self.load_csv(f"client_{client_code}_transfers_3m.csv")
        transactions = self.load_csv(f"client_{client_code}_transactions_3m.csv")

        transfers = self.clean_data(transfers)
        transactions = self.clean_data(transactions)

        # Получаем базовую информацию о клиенте
        name = transfers["name"].iloc[0] if not transfers.empty else transactions["name"].iloc[0]
        city = transfers["city"].iloc[0] if not transfers.empty else transactions["city"].iloc[0]
        status = transfers["status"].iloc[0] if not transfers.empty else transactions["status"].iloc[0]
        
        # Вычисляем средний месячный баланс (примерная оценка)
        total_income = transfers.loc[transfers["direction"] == "in", "amount"].sum()
        avg_monthly_balance = total_income / 3  # 3 месяца данных
        
        result = {
            "client_code": client_code,
            "name": name,
            "city": city,
            "status": status,
            "age": 30,  # По умолчанию, так как возраст не указан в данных
            "avg_monthly_balance_KZT": avg_monthly_balance,
            "total_transfer_in": transfers.loc[transfers["direction"] == "in", "amount"].sum(),
            "total_transfer_out": transfers.loc[transfers["direction"] == "out", "amount"].sum(),
            "transaction_sum": transactions["amount"].sum(),
            "transaction_avg": transactions["amount"].mean(),
            "top_categories": transactions.groupby("category")["amount"].sum().sort_values(ascending=False).head(5).to_dict()
        }
        return result

    def analyze_all(self, clients: list[int]):
        """Аналитика по всем клиентам"""
        all_data = []
        for client in clients:
            try:
                client_data = self.analyze_client(client)
                all_data.append(client_data)
            except FileNotFoundError:
                print(f"[WARN] Нет данных для клиента {client}")
        return pd.DataFrame(all_data)

    def save_report(self, df, filename="analytics_report.csv"):
        """Сохраняем отчет"""
        out_path = self.data_output_path / filename
        df.to_csv(out_path, index=False)
        print(f"[INFO] Отчет сохранен: {out_path}")
