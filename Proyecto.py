import pandas as pd
from matplotlib import pyplot as plt


# Definimos una función que nos deje leer todos los .csvs para poder manejarlos más fácil
# mandamos el directorio de donde están los archivos y el nombre del archivo como parámetro para el comando
# read_csv
def read_file(directory: str, file_name: str) -> pd.DataFrame:
    if file_name.endswith(".csv"):  # checamos que sea un archivo .csv para que no haya ningún tipo de fallo
        file = pd.read_csv(directory + file_name, encoding="UTF-8",
                           header=0)  # definimos la línea 0 como los nombres de
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
    aux_df = data  # copiamos los datos del DataFrame a otro para evitar cosas indeseadas
    aux_df["month"] = pd.to_datetime(aux_df["Date"]).dt.month  # añadimos una columna llamada mes para después
    aux_df["year"] = pd.to_datetime(aux_df["Date"]).dt.year  # lo mismo con el año
    max_value = aux_df.groupby(["year", "month"], as_index=False)[column].max()  # agrupamos el DataFrame para que solo
    # encontremos los valores máximos, mínimos y promedio de ese mes, primero por año y luego por mes
    min_value = aux_df.groupby(["year", "month"], as_index=False)[column].min()
    avg_value = aux_df.groupby(["year", "month"], as_index=False)[column].mean(numeric_only=False)  # numeric_only sirve
    # para indicar que puede que haya valores no numéricos, es necesario señalar esto por que a Python no le gusta tener
    # que adivinar si solo va a haber números o no

    return max_value, min_value, avg_value  # regresamos 3 DataFrames con los valores de máximo, minimo y promedio


# Problema 2
# Esto añade la columna total al DataFrame original
def total_transactions(data: pd.DataFrame):
    data["Volume"] = data["Volume"].astype(float)  # parseamos la columna volumen a un float para poder hacer una
    # multiplicación, no necesitamos quitar el signo de moneda porque no tiene
    data["Total"] = data["Close/Last"] * data["Volume"]  # no necesitamos regresar nada porque ya lo añadimos al
    # DataFrame original con este comando


# Problema 4
# Implementación similar al problema 2
def earnings(data: pd.DataFrame):
    data["Open"] = data["Open"].str.strip("$")  # lo unico que cambia en este método es que parseamos la columna de
    # open para poder hacer las operaciones pertinentes, por lo demás tenemos lo mismo
    data["Open"] = data["Open"].astype(float)
    data["Ganancias"] = data["Open"] / (data["Close/Last"] - 1)  # añadimos la columna ganancias


# Problema 6
# este método busca graficar las diferentes columnas que se nos piden, obtiene para esto los valores máximo, mínimo y
# promedio para ser utilizados
def plot_shares(data: list[pd.DataFrame], column: str, names: list[str]):
    dates = get_months(data[0])  # obtenemos las fechas tipo yyyy/mm para poder añadir los títulos en x

    fig1, ax1 = plt.subplots()  # definimos una nueva figura sobre la que graficar y un eje en el que usamos .plot()
    plt.setp(ax1, xticklabels=[dates[0], dates[9], dates[19], dates[34], dates[29], dates[39], dates[49],
                               dates[59]])  # fijamos los nombres de los puntos de los ejes
    for i in range(len(data)):
        fig1.suptitle(f"Valor máximo de {column}")  # título general del plot
        max_value = find_month_values(data[i], column)[0]  # valores máximos por mes de la columna
        max_value[column].plot(ax=ax1, label=names[i])  # graficamos sobre el eje 1 y le asignamos el nombre de empresa
    plt.legend()  # muestra una simbología indicando que color de línea toma cada empresa
    plt.show()  # muestra el plot en la figura designada

    fig2, ax2 = plt.subplots()  # definimos una nueva figura sobre la que graficar y un eje en el que usamos .plot()
    plt.setp(ax2, xticklabels=[dates[0], dates[9], dates[19], dates[29], dates[34], dates[39], dates[49],
                               dates[59]])  # fijamos los nombres de los puntos de los ejes
    for i in range(len(data)):
        fig2.suptitle(f"Valor mínimo de {column}")  # título general del plot
        min_value = find_month_values(data[i], column)[1]  # valores mínimos por mes de la columna
        min_value[column].plot(ax=ax2, label=names[i])  # graficamos sobre el eje 2 y le asignamos el nombre de empresa
    plt.legend()  # muestra una simbología indicando que color de línea toma cada empresa
    plt.show()  # muestra el plot en la figura designada

    # definimos un plot para el valor promedio
    fig3, ax3 = plt.subplots()  # definimos una nueva figura sobre la que graficar y un eje en el que usamos .plot()
    plt.setp(ax3, xticklabels=[dates[0], dates[9], dates[19], dates[29], dates[34], dates[39], dates[49],
                               dates[59]])  # fijamos los nombres de los puntos de los ejes
    for i in range(len(data)):
        fig3.suptitle(f"Valor promedio de {column}")  # título general del plot
        avg_value = find_month_values(data[i], column)[2]  # valores promedio por mes de la columna
        avg_value[column].plot(ax=ax3, label=names[i])  # graficamos sobre el eje 3 y le asignamos el nombre de empresa
    plt.legend()  # muestra una simbología indicando que color de línea toma cada empresa
    plt.show()  # muestra el plot en la figura designada

    # en dado caso de que estemos graficando la columna ganancias tenemos que hacer un histograma
    if column == "Ganancias":
        fig4, ax4 = plt.subplots(len(names), figsize=(20, 20))  # definimos una nueva figura sobre la que graficar y un
        # eje en el que usamos .plot()
        plt.setp(ax4, xticklabels=[dates[0], dates[9], dates[19], dates[29], dates[34], dates[39], dates[49],
                                   dates[59]])  # fijamos los nombres de los puntos de los ejes
        for i in range(len(data)):
            fig4.suptitle("Valor histórico de las ganancias")  # título general del plot
            data[i][column].hist(ax=ax4[i])  # graficamos los valores históricos de las ganancias por cada subplot
            ax4[i].set_title(names[i])  # fijamos los títulos de cada subplot para señalar las diferencias
        plt.show()  # muestra el plot en la figura designada


def get_months(data: pd.DataFrame) -> list:
    df_aux = data  # copiamos los datos del DataFrame a otro para evitar cosas indeseadas
    df_aux["month"] = pd.to_datetime(df_aux["Date"]).dt.month  # añadimos una columna llamada mes para después
    df_aux["year"] = pd.to_datetime(df_aux["Date"]).dt.year  # lo mismo con el año

    mon = []  # usamos una lista para llenar todos los meses posibles
    for month in df_aux["month"].values:
        aux = str(month)  # parseamos el tipo datetime a str
        if len(aux) == 1:  # si es un mes con solo un dígito añadimos un 0 para evitar que Python haga de las suyas
            aux = "0" + aux
        mon.append(aux)

    # hacemos lo mismo que hicimos con mes pero ahora con año
    yr = []
    for year in df_aux["year"].values:
        yr.append(str(year))

    # añadimos los valores de mes y año en formato yyyy-mm, si fuera yyyy-m, Python lo acomoda como quiere, por lo que
    # tenemos que ponerlo en ese formato para evitar problemas
    str_aux = []
    for i in range(len(mon)):
        str_aux.append(yr[i] + "-" + mon[i])

    set_aux = set(str_aux)  # cambiamos a un set para poder eliminar los duplicados
    ans = list(set_aux)  # cambiamos a una lista para manejarla de manera más sencilla
    ans.sort()  # al cambiar a set los valores se desordenan, por lo que tenemos que ordenarlos

    return ans  # regresamos la lista ya ordenada
