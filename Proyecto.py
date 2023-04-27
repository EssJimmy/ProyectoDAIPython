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
# Esto tiene que ser cambiado por completo, ya que estoy haciendo un ejercicio que no me pidieron
# Lo que pide es que ploteemos el promedio, maximo y minimo de tres columnas, no de todas las columnas hay
# del único que tenemos que plotear histórico es de la ganancia, pero eso ya está ez
def plot_shares(data: pd.DataFrame, column: str):
    values = []
    x = []

    if column == "Close/Last" or "Total" or "Ganancia":
        max_value, min_value, avg_value = find_month_values(data, column)
        for value in max_value["Close/Last"].astype(float).values:
            values.append(value)

        for value in min_value["Close/Last"].astype(float).values:
            values.append(value)

        for value in values:
            index = find_index_values(data, column, value)
            for i in index:
                x.append(i)

        for value in avg_value["Close/Last"].astype(float).values:
            values.append(value)

    print(len(x))
    print(len(values))
    data[column].plot(x=column, y="Valor", title=column)

    plt.show()


def find_index_values(data: pd.DataFrame, column: str, value: float):
    return data[data[column] == value].index.values.tolist()
