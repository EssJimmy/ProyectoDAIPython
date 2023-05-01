import pandas as pd
import matplotlib.pyplot as plt


# Definimos una función que nos deje leer todos los .csvs para poder manejarlos más fácil
# mandamos el directorio de donde están los archivos y el nombre del archivo como parámetro para el comando
# read_csv
def read_file(directory: str, file_name: str) -> pd.DataFrame:
    if file_name.endswith(".csv"):  # checamos que sea un archivo .csv para que no haya ningún tipo de fallo
        file = pd.read_csv(directory+file_name, encoding="UTF-8", header=0)  # definimos la línea 0 como los nombres de
        # cabecera del DataFrame
        data = format_file(file)  # llamo a la función format_file que va a parsear los datos de algunas columnas a los
        # tipos que quiero, así como ordenarlos por fecha
        return data  # regresamos un archivo de tipo DataFrame
    else:
        print("Selected file is not a .csv file!")  # Si falla, indicamos que no es un archivo de tipo .csv


# Función para formatear la entrada al DataFrame como queremos, esta función quita los signos de moneda y cambia la
# columna fecha a un tipo DateTime para que podamos ordenar por fechas
def format_file(data: pd.DataFrame) -> pd.DataFrame:
    data["Close/Last"] = data["Close/Last"].str.strip("$")  # quitamos el signo de moneda para poder parsear la columna
    # como tipo float
    data["Close/Last"] = data["Close/Last"].astype(float)  # parseamos la columna como tipo float
    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")  # parseamos la columna como tipo datetime, además
    # le decimos que el archivo viene en formato mm/dd/yyyy, para que lo cambie a yyyy/mm/dd
    data.sort_values(by="Date", inplace=True)  # ordenamos el archivo por fechas, indicamos que queremos que sea hecho
    # el mismo dataframe con el comando inplace=True

    return data  # regresamos el dataframe con el formato requerido


# Problema 1, 3 y 5 (solo cambiamos el nombre de la columna del que queremos estos valores)
# como el problema 1, 3 y 5 hacen lo mismo podemos utilizar una función con un valor default para esto,
# pedimos como entrada un DataFrame y una cadena, por default su valor será "Close/Last"
def find_month_values(data: pd.DataFrame, column="Close/Last") -> tuple:
    avg_df = data  # copiamos los datos del DataFrame a otro para evitar cosas indeseadas
    avg_df["month"] = pd.to_datetime(avg_df["Date"]).dt.month  # añadimos una columna llamada mes para después
    avg_df["year"] = pd.to_datetime(avg_df["Date"]).dt.year  # lo mismo con el año
    max_value = avg_df.groupby(["year", "month"], as_index=False)[column].max()  # agrupamos el DataFrame para que solo
    # encontremos los valores máximos, mínimos y promedio de ese mes, primero por año y luego por mes
    min_value = avg_df.groupby(["year", "month"], as_index=False)[column].min()
    avg_value = avg_df.groupby(["year", "month"], as_index=False)[column].mean(numeric_only=False)  # numeric_only sirve
    # para indicar que puede que haya valores no numéricos, es necesario señalar esto por que a Python no le gusta tener
    # que adivinar si solo va a haber números o no

    return max_value, min_value, avg_value  # regresamos 3 DataFrames con los valores de máximo, minimo y promedio


# Problema 2
# Esto añade la columna total al DataFrame original
def total_transactions(data: pd.DataFrame):
    data["Volume"] = data["Volume"].astype(float)  # parseamos la columna volumen a un float para poder hacer una
    # multiplicación, no necesitamos quitar en signo de moneda porque no tiene
    data["Total"] = data["Close/Last"] * data["Volume"]  # no necesitamos regresar nada porque ya lo añadimos al
    # DataFrame original con este comando


# Problema 4
# Implementación similar al problema 2
def earnings(data: pd.DataFrame):
    data["Open"] = data["Open"].str.strip("$")  # lo unico que cambia en este método es que parseamos la columna de
    # open para poder hacer las operaciones pertinentes, por lo demás tenemos lo mismo
    data["Open"] = data["Open"].astype(float)
    data["Ganancias"] = data["Open"]/(data["Close/Last"] - 1)  # añadimos la columna ganancias


# Problema 6
# este método busca graficar las diferentes columnas que se nos piden, obtiene para esto los valores máximo, mínimo y
# promedio para ser utilizados
def plot_shares(data: pd.DataFrame, column: str):
    max_value, min_value, avg_value = find_month_values(data, column)  # obtenemos los valores en DataFrames
    if column == "Ganancias":  # checamos si estamos graficando ganancias, para ver si vamos a graficar el valor
        # histórico
        figs, axes = plt.subplots(nrows=2, ncols=2)
        max_value[column].plot(color="g", ax=axes[0][0])
        min_value[column].plot(color="b", ax=axes[0][1])
        avg_value[column].plot(color="r", ax=axes[1][0])
        data[column].hist(ax=axes[1][1])
    else:
        figs, axes = plt.subplots(3)
        max_value[column].plot(color="g", ax=axes[0])
        min_value[column].plot(color="b", ax=axes[1])
        avg_value[column].plot(color="r", ax=axes[2])

    plt.show()
