import pandas as pd
import matplotlib.pyplot as plt


def read_file(directory: str, file_name: str):
    if file_name.endswith(".csv"):
        file = pd.read_csv(directory+file_name, encoding="UTF-8", header=0)
        data = format_file(file)
        return data
    else:
        print("Selected file is not a .csv file!")


def format_file(data: pd.DataFrame):
    data["Close/Last"] = data["Close/Last"].str.strip("$")
    data["Close/Last"] = data["Close/Last"].astype(float)
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
    data.sort_values(by="Date", inplace=True)

    return data


# Problema 1, 3 y 5 (solo cambiamos el nombre de la columna del que queremos estos valores)
def find_month_values(data: pd.DataFrame, column="Close/Last"):
    avg_df = data
    avg_df["month"] = pd.to_datetime(avg_df["Date"]).dt.month
    avg_df["year"] = pd.to_datetime(avg_df["Date"]).dt.year
    max_value = avg_df.groupby(["year", "month"], as_index=False)[column].max()
    min_value = avg_df.groupby(["year", "month"], as_index=False)[column].min()
    avg_value = avg_df.groupby(["year", "month"], as_index=False)[column].mean(numeric_only=False)

    return max_value, min_value, avg_value


# Problema 2
def total_transactions(data: pd.DataFrame):
    data["Volume"] = data["Volume"].astype(float)
    data["Total"] = data["Close/Last"] * data["Volume"]


# Problema 4
def earnings(data: pd.DataFrame):
    data["Open"] = data["Open"].str.strip("$")
    data["Open"] = data["Open"].astype(float)
    data["Ganancias"] = data["Open"]/(data["Close/Last"] - 1)


# Problema 6
def plot_shares(data: pd.DataFrame, column: str):
    max_value, min_value, avg_value = find_month_values(data, column)
    if column == "Ganancias":
        fig, axes = plt.subplots(nrows=2, ncols=2)
        max_value[column].plot(color="g", ax=axes[0][0])
        min_value[column].plot(color="b", ax=axes[0][1])
        avg_value[column].plot(color="r", ax=axes[1][0])
        data[column].plot(color="c", subplots=True, ax=axes[1][1])
    else:
        max_value[column].plot(color="g")
        min_value[column].plot(color="b")
        avg_value[column].plot(color="r")

    plt.show()
