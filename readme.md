# Proyecto de DAI en Pandas

El proyecto consiste en el análisis de datos mediante el uso de la libreria `pandas` en Python. Para evitar hacer un código más limpio y legible, dividí esto en dos clases, una llamada `Proyecto.py` que contiene todos los métodos que resuelven los problemas indicados, y otra llamada `main.py` que ejecuta el código dentro del anterior archivo mencionado. Enfoquémonos en la clase proyecto, ya que es la que contiene la algorítmica utilizada para la resolución de problemas:

## Métodos y funciones en `proyecto.py`
### Librerías utilizadas
Primero empezamos con las librerias que necesitamos para hacer el proyecto funcionar, que serán `pandas` y `pyplot`, el segundo siendo un paquete dentro de la librería `matplotlib`. Los importamos de la siguiente manera:
```python
import pandas as pd
from matplotlib import pyplot as plt
```
Pandas nos da el acceso a nuevas estructuras de datos como `Series` y `DataFrames` que funcionan como vectores y tablas respectivamente, para este proyecto utilizaremos `DataFrames` debido a la cantidad de información que requerimos manejar. Pyplot nos sirve para graficar, y dado que las gráficas de Pandas se basan en pyplot, también podemos utilizar métodos de pyplot para mejorar las gráficas y su legibilidad.

### Lectura y formato del archivo para su utilización
El problema nos requiere leer datos desde un archivo tipo `.csv` y desde ahí manejar toda la información que queremos, para se plantearon dos métodos, el primero es `read_file` que toma como parámetros el directorio del archivo y su nombre, y revisa su extensión para asegurarse que sea un tipo `.csv`, en dado caso de que no lo sea, nos lo hace saber.

El segundo se llama `format_file`, que toma como parámetro a un `DataFrame` y se encarga de darle el formato necesario a algunas columnas que lo requieren, estas son: 
  * Date: tenemos que cambiar el tipo de datos de string a datetime, esto para poder encontrar cosas por mes, año, día, etcétera y los ordena por fecha.
  * Close/Last: quitamos los signos de peso y cambiamos de tipo string a float, para poder realizar operaciones matemáticas para resolver otros problemas.

Los dos métodos devuelven un DataFrame, y su código documentado es el siguiente:
```python
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
```

### Encontrar el total de transacciones de las acciones de la empresa
El problema dos nos pide encontrar el número total de transacciones de las acciones de la empresa, esto lo hacemos multiplicando el volumen de la acciones por el precio de cierre de la acción por día, además nos pide que añadamos estos resultados a una columna nueva del `DataFrame` original llamada `Total`.

Para esto se planteó un método llamado `total_transactions` que recibe como parámetro el `DataFrame` original al que le queremos hacer las operaciones anteriormente mencionadas. Para resolver este problema, tomamos la columna `Volume` del `DataFrame` y cambiamos su tipo, del original a `float`, para evitarnos problemas de multiplicación, ya que esto nos podría llegar a dar una excepción del interprete, después de eso, simplemente lo múltiplicamos por la columna `Close/Last` y le asignamos los valores a la columna `Total`, si no existe se agrega automáticamente, sin ningún problema, el código documentado de este método es el siguiente:
```python
# Problema 2
# Esto añade la columna total al DataFrame original
def total_transactions(data: pd.DataFrame):
    data["Volume"] = data["Volume"].astype(float)  # parseamos la columna volumen a un float para poder hacer una
    # multiplicación, no necesitamos quitar el signo de moneda porque no tiene
    data["Total"] = data["Close/Last"] * data["Volume"]  # no necesitamos regresar nada porque ya lo añadimos al
    # DataFrame original con este comando
```

### Encontrar las ganancias de las acciones de la empresa
Similar al método anterior, se nos pide calcular las ganancias por día de la empresa y añadirlas a una columna de nombre `ganancia`, esto se hace con la formula $\frac{open}{close/last - 1}$, donde 'open' significa el precio al que abrio la acción y 'close/last' el precio de cierre de la acción.

Como en el método previo, primero tenemos que asegurarnos que tengamos valores de tipo `float`, así que le hacemos un cambio de tipo a la columna `Open`, pero primero le quitaremos el signo de moneda, esto para evitar problemas con el interprete de Python. Después de hacer esto, procedemos a aplicar la fórmula anterior y añadirsela a la columna `Ganancias`, si no existe, entonces se creará de manera automática.

El código de este método es el siguiente:
```python
# Problema 4
# Implementación similar al problema 2
def earnings(data: pd.DataFrame):
    data["Open"] = data["Open"].str.strip("$")  # lo unico que cambia en este método es que parseamos la columna de
    # open para poder hacer las operaciones pertinentes, por lo demás tenemos lo mismo
    data["Open"] = data["Open"].astype(float)
    data["Ganancias"] = data["Open"] / (data["Close/Last"] - 1)  # añadimos la columna ganancias
```

### Encontrar los valores máximos, mínimos y promedio por mes de diferentes columnas
Este problema nos pide encontrar valores por mes, por lo que el paso inicial de darle un formato específico a la columna `Date` nos viene muy bien, primero copiaremos el `DataFrame` original a uno extra, ya que vamos a añadir las columnas `month` y `year` para hacer operaciones de agrupamiento por mes y año para encontrar los valores que requerimos, y ya que no queremos tocar el `DataFrame` original esto es necesario. Después de esto, procedemos a agrupar por año primero, y después por mes, y utilizamos los comandos `.max()`, `.min()` y `.mean()` para encontrar los valores queridos, esto lo añadimos a `DataFrames` individuales cada uno por los comandos que utilizamos, quedando así el código.

Recibimos como parámetros el `DataFrame` original, el nombre de la columna del que vamos a encontrar su valor, que por defecto será 'Close/Last' para evitar problemas con el interprete o accidentes de dedo, y se nos regresará una tupla con tres `DataFrames` uno para los valores máximos, uno para los mínimos y el último para los promedio.

**Nota 1:** para evitar que `pandas` ordene por índice los meses y los años, y que los tome de la forma en la que se los dimos (ya ordenados cronológicamente) utilizamos el atributo `as_index=False` dentro del comando `.groupby()`.

**Nota 2:** el método `.mean()` tiene como atributo a `numeric_only=False`, esto le indica al comando que en el `DataFrame` puede haber valores de tipo `NaN - Not a Number`, en el caso de que no pongamos esto y el interpreté se encuentre un tipo `NaN`va a lanzar una excepción, en el caso de `.min()`y `.max()`, automáticamente ignoran estos tipos, así que no hay problema.

Aquí el código documentado del método:
```python
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
```

### Graficado de los valores promedio, máximos y mínimos por mes, además del valor histórico de las ganancias
El problema 6 nos pide las gráficas de las columnas:
  * Close/Last: valores máximos, mínimos y promedio mensuales.
  * Total: valores máximos, mínimos y promedio mensuales.
  * Ganancias: valores máximos, mínimos y promedio mensuales, además del valor histórico en un histograma.

Para hacer esto empezamos definiendo un método auxiliar que nos ayudará a obtener las fechas en formato yyyy-mm, esto para poder señalar en los ejes las fechas de los periodos. El método se llama `get_months` y toma como parámetros un `DataFrame`, devuelve una lista con las fechas del periodo analizado.

Para hacer esto, hacemos una copia del `DataFrame`, y creamos la columna `month` y `year` que nos ayudará a tener los datos de manera más accesible, la forma en la que podemos hacer esto es como el código del anterior inciso, obteniendo desde un tipo `datetime`, un tipo `month` y un tipo `year`. Desde ahí usamos las listas auxiliares `mon` y `yr` para meter todos los valores de los meses y los años, después estas dos listas las juntaremos en una lista que contenga un formato yyyy-mm, esta lista se llama `str_aux`, de ahí haremos un cambio de lista a un conjunto, para poder quitar los repetidos, volvemos a hacer un cambio a lista y ordenamos los elementos dentro de esta, ya que al cambiar la lista original a un conjunto se desordenaron, por lo que podemos utilizar `.sort()`. El código de este método auxiliar es el siguiente:
```python
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
```

El método principal para graficar utiliza el método antes mencionado, pero es más complejo. El método se llama `plot_shares` y utiliza como parámetros una lista de `DataFrames`, una cadena `columna` que indica la columna del `DataFrame` que será graficada y una lista `names`, que contiene el nombre de las compañías a las que se va a graficar. Empezamos usando el método antes definido para obtener los meses para los títulos del eje. Después de eso, definiremos tres (cuatro en dado caso de que estemos graficando la columna 'Ganancias') figuras y tres (cuatro) ejes para graficar sobre ellos, usaremos el comando `plt.setp()` para fijar el eje sobre el que queremos los títulos que obtuvimos al principio. Después, utilizaremos un ciclo `for` para recorrer la lista de `DataFrames`, obteniendo el valor máximo de estos para el primer eje, el valor mínimo para el segundo eje, y el valor promedio en el tercer eje (el cuarto eje tendría el valor históricio de las ganancias en un histograma, pero esto solo pasa si estamos graficando la columna 'Ganancias'). Asignamos los valores del título de la figura, que en este caso será: 'Valor máximo/mínimo/promedio de la "Columna"', además de que al comando `.plot()` le asignaremos los atributos `ax` y `labels` para indicar el eje sobre el que se graficará, y los nombres que tomaran cada gráfica, esto es, que significaran los colores dentro de gráfica, por último, utilizamos `plt.show()` para mostrar la gráfica y `plt.legend()` para mostrar los nombres de los colores de línea antes mencionados. Dicho todo esto, el código del método es el siguiente:
```python
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
```