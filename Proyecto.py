import pandas as pd
import matplotlib.pyplot as plt


def read_file(directory: str, file_name: str):
    if file_name.endswith(".csv"):
        file = pd.read_csv(directory+file_name, encoding="UTF-8", header=0)
        data = sort_by_date(file)
        return data
    else:
        print("Selected file is not a .csv file!")


def sort_by_date(data: pd.DataFrame):
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
    data.sort_values(by="Date", inplace=True)

    return data


# Problema 1, 3 y 5 (solo cambiamos el nombre de la columna del que queremos estos valores)
def find_month_values(data: pd.DataFrame, column="Close/Last"):
    if column == "Close/Last":
        data[column] = data[column].str.strip("$")
        data[column] = data[column].astype(float)

    avg_df = data
    avg_df["month"] = pd.to_datetime(avg_df["Date"]).dt.month
    avg_df["year"] = pd.to_datetime(avg_df["Date"]).dt.year
    max_value = avg_df.groupby(["year", "month"], as_index=False)[column].max()
    min_value = avg_df.groupby(["year", "month"], as_index=False)[column].min()
    avg_value = avg_df.groupby(["year", "month"], as_index=False)[column].mean(numeric_only=False)

    return max_value, min_value, avg_value


# Problema 2
def total_transactions(data: pd.DataFrame):
    data["Total"] = data["Close/Last"] * data["Volume"]


# Problema 4
def earnings(data: pd.DataFrame):
    data["Ganancias"] = data["Open"]/(data["Close/Last"] - 1)


# Problema 6
def plot_shares(data: pd.DataFrame, column: str):
    values = []

    if column == "Close/Last" or "Total" or "Ganancia":
        max_value, min_value, avg_value = find_month_values(data, column)
        values.append(data.index.get_loc(max_value))
        values.append(data.index.get_loc(min_value))
        values.append(data.index.get_loc(avg_value))

    data[column].plot(x=column, y="Valor", title=column, markevery=values)
    plt.show()
