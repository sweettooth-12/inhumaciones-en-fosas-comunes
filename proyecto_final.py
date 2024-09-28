# EXPLORACIÓN DE LOS DATOS

# Implementación de las librerias utilizadas.
from IPython.display import display # Para mostrar múltiples resultados en una sola celda.
import pandas as pd
import numpy as np

# Variable con el nombre del archivo
archivo = "https://comisionacionaldebusqueda.gob.mx/wp-content/uploads/2024/05/Mo%CC%81dulo-de-Fosas-Comunes_actualizacion26abr2024_VD.xlsx"
df = pd.read_csv(archivo)
df.head(5)

# Obtenemos un panorama general de los datos.
def info_general_df(df):
  print('Información general del DataFrame\n')
  print(f'Cantidad de filas y columnas: {df.shape}')
  print("*"*50)
  print(f'Cantidad de datos nulos por columna: \n{df.isnull().sum()}')
  print("*"*50)
  print(f'Tipos de datos por columna: \n{df.dtypes}')

info_general_df(df)

df_actual = df.copy()

# LIMPIEZA DE DATOS

# Se filtran las filas de personas repetidas las cuales tienen '_' en su ID
df_actual = df[~df['ID'].str.contains('_')]

# Se le asigna 'Desconocido' a los valores vacíos y nulos de la columna 'Nombre_completo'
df_actual['Nombre_completo'] = df_actual['Nombre_completo'].replace('  ','Desconocido')
df_actual['Nombre_completo'] = df_actual['Nombre_completo'].fillna('Desconocido')

# Convierte la columna "Fecha_inhumación" a tipo de dato "datetime"
df_actual['Fecha_inhumación'] = pd.to_datetime(df_actual['Fecha_inhumación'], format='%d/%m/%Y', errors='coerce')

# Convierte la columna "Fecha_defunción" a tipo de dato "datetime"
df_actual['Fecha_defunción'] = pd.to_datetime(df_actual['Fecha_defunción'], format='%d/%m/%Y', errors='coerce')

# Convierte la columna "Marca temporal" a tipo de dato "datetime"
df_actual['Marca_temporal'] = pd.to_datetime(df_actual['Marca_temporal'], format='%d/%m/%Y', errors='coerce')

# Se cambian el domininio de los valores de la columna 'Conocido_Desconocido'
# Asignando 1 si el valor es 'Conocido' y 0 si es 'Desconocido'
df_actual['Conocido_Desconocido'] = df_actual['Conocido_Desconocido'].replace({'Desconocido': 0, 'Conocido': 1})

# Función para manejar los valores de la columna 'Edad' que no estan en años
def edades_cero(edad):
    try:
        # Intentamos convertir el valor a entero
        return int(edad)
    except:
        # Si el valor es NaN o S/D, lo dejamos como está
        if pd.isna(edad) or edad == 'S/D':
            return edad
        # Si no se puede convertir y no es NaN ni S/D, lo convertimos a 0
        return 0

# Aplicamos la función a la columna 'Edad'
df_actual['Edad'] = df_actual['Edad'].apply(edades_cero)

# Convertirmos el tipo de dato de la columna 'Edad' a numerico
df_actual['Edad'] = pd.to_numeric(df_actual['Edad'], errors='coerce')

# Asignamos a los valores NaN el valor de la media de las demás edades
media_edad = df_actual['Edad'].mean()
df_actual['Edad'].fillna(media_edad, inplace=True)

# Convertimos a entero la columna de 'Edad'
df_actual['Edad'] = df_actual['Edad'].astype(int)

# Elimina la columna "Datos_alternativos", "Rdoc", "Nombre(s)", "Primer_apellido" y "Segundo_apellido".
df_actual = df_actual.drop(columns=["Datos alternativos", "Rdoc", "Nombre(s)", "Primer_apellido", "Segundo_apellido"], axis=1)

df_actual.head(5)

# Se imprime la lista de los nombres de las columnas del DataFrame
lista_col_actuales=df_actual.columns.tolist()
print(lista_col_actuales)

# Se crea el diccionario con los nuevos nombres de las columnas
mapeo_nombre_columna = {
    'ID': 'id',
    'Nombre_completo': 'nombre_completo',
    'Estado_origen': 'estado_origen',
    'Municipio_origen': 'municipio_origen',
    'Panteón_origen': 'panteon_origen',
    'Estatus_FC': 'estatus',
    'Fecha_inhumación': 'fecha_inhumacion',
    'Fecha_defunción': 'fecha_defuncion',
    'Restos_tipo': 'restos_tipo',
    'Sexo': 'sexo',
    'Edad': 'edad',
    'Conocido_Desconocido': 'conocido',
    'Institución_origen': 'institucion_origen',
    'Marca_temporal': 'marca_temporal',
}

# Se renombran las columnas de nuestro dataset
df_actual.rename(columns=mapeo_nombre_columna, inplace=True)

df_actual.head(2)

info_general_df(df_actual)

# ANÁLISIS DE DATOS
# Preguntas
# a) ¿Cuantás inhumaciones han sido reportadas por cada panteón?

inhumaciones_por_panteon = df_actual[df_actual["estatus"] == "Inhumación"].groupby("panteon_origen")["estatus"].count()
print(inhumaciones_por_panteon)

# b) ¿Qué Estados están reportados en el módulo?
# Funcion para imprimir una lista elemento por elemento
def print_lista(lista):
  for elemento in lista:
    print(elemento)

# c) ¿En qué estados hay más inhumaciones?
# Se agrupa el número de inhumaciones reportadas por estado
inhumaciones_por_estado = df_actual[df_actual["estatus"] == "Inhumación"].groupby("estado_origen")["estatus"].count()
print(inhumaciones_por_estado)

# Se obtiene el número máximo de inhumaciones
num_max_inhumaciones_por_estado = inhumaciones_por_estado.max()

# Se filtran los estados que tienen el numero máximo de ihumaciones
estados_con_max_inhumaciones = inhumaciones_por_estado[inhumaciones_por_estado == num_max_inhumaciones_por_estado].index.tolist()
print('Los estados con el máximo de inhumaciones son:')
print_lista(estados_con_max_inhumaciones)

# (d) ¿En qué estados hay menos inhumaciones?
# Se obtiene el número mínimo de inhumaciones
num_min_inhumaciones_por_estado = inhumaciones_por_estado.min()

# Se filtran los estados que tienen el numero mínimo de ihumaciones
estados_con_min_inhumaciones = inhumaciones_por_estado[inhumaciones_por_estado == num_min_inhumaciones_por_estado].index.tolist()
print('Los estados con el mínimo de inhumaciones son:')
print_lista(estados_con_min_inhumaciones)

# (e) ¿Cuántos restos son conocidos y cuántos desconocidos?
# Contamos el número de restos conocidos (valores 1)
cant_restos_conocidos = df_actual['conocido'].sum()
# Calculamos la cantidad de restos desconocidos
cant_restos_desconocidos = len(df_actual) - cant_restos_conocidos
print(f'Hay {cant_restos_conocidos} restos registrados como conocidos')
print(f'Hay {cant_restos_desconocidos} restos registrados como desconocidos')

# (f) ¿Cuáles son los tipos de restos registrados en el módulo y cuántos registros hay de cada tipo?
tipos_de_restos = df_actual.groupby('restos_tipo')['id'].count()
print('Tipos de restos registrados en el módulo y su frecuencia:')
print(tipos_de_restos)