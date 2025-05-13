import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from statistics import mean, median, mode, stdev, variance

# coneccion con la api
serie_dolar = "SF43718"  # Tipo de cambio FIX
fecha_fin = datetime.today().strftime("%Y-%m-%d")
fecha_inicio = (datetime.today() - timedelta(days=7*365)).strftime("%Y-%m-%d")


with open("token.txt", "r") as archivo:
    personal_token = archivo.read()


token =personal_token
url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie_dolar}/datos/{fecha_inicio}/{fecha_fin}"
headers = {"Bmx-Token": token}

respuesta = requests.get(url, headers=headers)
datos = respuesta.json()["bmx"]["series"][0]["datos"]

# eestructura datos
df = pd.DataFrame(datos)
df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
df["dato"] = pd.to_numeric(df["dato"], errors="coerce")

# estadistica
valores = df["dato"].dropna()
media = mean(valores)
mediana = median(valores)
moda = mode(valores)
desviacion = stdev(valores)
varianza = variance(valores)
maximo = valores.max()
fecha_max = df.loc[df["dato"].idxmax(), "fecha"]

print("Análisis Estadístico del dólar (últimos 7 años):")
print(f"Media: {media:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Moda: {moda:.2f}")
print(f"Desviación estándar: {desviacion:.2f}")
print(f"Varianza: {varianza:.2f}")
print(f"Precio máximo: {maximo:.2f} el {fecha_max.date()}")

# Mandarlo a excel
df.to_excel("dolar_banxico_7anios.xlsx", index=False)

#ver los datos en la grafica
plt.figure(figsize=(12,6))
plt.plot(df["fecha"], df["dato"], color="blue")
plt.title("Precio del dólar en los últimos 7 años")
plt.xlabel("Fecha")
plt.ylabel("Precio en pesos mexicanos")
plt.tight_layout()
plt.show()


