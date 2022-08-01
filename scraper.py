"""
Este programa convierte la información de JHU a series de tiempo
usando un algoritmo detransposición.
"""

import csv
from datetime import datetime

import requests


ARCHIVOS_CSV = {
    "confirmados": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "defunciones": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
}


def main():

    # Obtenemos nuestras estructuras con valores en ceros.
    data_dict, dates_dict = generate_list()

    for tipo, url in ARCHIVOS_CSV.items():

        with requests.get(url) as respuesta:

            # Convertir la respuesta a un objeto csv.DictReader
            lector = csv.DictReader(respuesta.text.splitlines())

            for fila in lector:

                for k, v in dates_dict.items():

                    llave_temporal = f"{v}_{fila['Country/Region']}"

                    if tipo == "confirmados":
                        data_dict[llave_temporal][0] += int(fila[k])
                    elif tipo == "defunciones":
                        data_dict[llave_temporal][1] += int(fila[k])

    datos = [["isodate", "pais", "confirmados", "defunciones"]]

    # Convertimos nuestro diccionario enuna lista para ser guardado en CSV.
    for k, v in data_dict.items():
        isodate, pais = k.split("_")
        datos.append([isodate, pais, v[0], v[1]])

    with open("./data.csv", "w", encoding="utf-8", newline="") as archivo_csv:
        csv.writer(archivo_csv).writerows(datos)


def generate_list():
    """
    Esta función crea la estructura para nuestro archivo CSV.

    Esto nos creará una estructura con valores cero que después serán
    rellenados con valores reales.
    """

    data_dict = dict()
    fechas_dict = dict()
    paises = set()

    # Leeremos la url de casos confirmados de COVID-19.
    url = ARCHIVOS_CSV["confirmados"]

    with requests.get(url) as respuesta:

        # Convertir la respuesta a un objeto csv.DictReader
        lector = csv.DictReader(respuesta.text.splitlines())

        # Escogemos todas las columnas excepto las primeras 4.
        columnas = lector.fieldnames[4:]

        # Extramoes todas las fechas disponibles.
        for columna in columnas:

            # Convertimos la fecha a un formato estandarizado y guardamos el formato original.
            fecha_temporal = datetime.strptime(columna, "%m/%d/%y")
            fechas_dict[columna] = f"{fecha_temporal:%Y-%m-%d}"

        # Agregamos todos los países/regiones a nuestro set.
        for fila in lector:
            paises.add(fila["Country/Region"])

        # Convertimos nuestro set de países en lista y lo ordenamos.
        paises = sorted(list(paises))

        for fecha in fechas_dict.values():

            for pais in paises:

                # Creamos llaves únicas para cada páis y fecha disponibles.
                llave_temporal = f"{fecha}_{pais}"

                data_dict[llave_temporal] = [0, 0]

        return data_dict, fechas_dict


if __name__ == "__main__":

    main()
