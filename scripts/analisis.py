# -*- coding: utf-8 -*-
# importamos las librerias necesarias
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Link del dataset
dataset = "https://gist.githubusercontent.com/khanusama20/ee33c2869dd5cf3cebdf020be1ca43f6/raw/sales_sample_2024.csv"

try:
    # utilizamos pandas para leer el archivo csv
    df = pd.read_csv(dataset)
    print("Dataset cargado con exito")
except Exception as e:
    print(f"Error al conectar con la URL: {e}")
    # en el caso de que falle , y tengamos el archivo en local , procedemos a leerlo
    df = pd.read_csv('sales_sample_2024.csv')

# campo sales_date o fecha de venta del dataframe
df['sales_date'] = pd.to_datetime(df['sales_date'])

# Simulamos nombres de productos con su respectiva cantidad dado que el dataset no lo trae.
np.random.seed(42)
productos_posibles = ['Laptop', 'Smartphone', 'Tablet', 'Auriculares', 'Monitor']
df['product'] = np.random.choice(productos_posibles, size=len(df))
df['quantity'] = np.random.randint(1, 5, size=len(df))

# Para calcular las ventas totales aplicando una suma
ventas_totales = df['sales_amount'].sum()

# sumamos las cantidades de cada producto
unidades_por_producto = df.groupby('product')['quantity'].sum()
# obtenemos el producto mas vendido y la cantidad maxima
producto_mas_vendido = unidades_por_producto.idxmax()
cantidad_maxima = unidades_por_producto.max()

# convertimos las fechas en periodos mensuales
df['month'] = df['sales_date'].dt.to_period('M')
# calculamos las ventas mensuales
ventas_por_mes = df.groupby('month')['sales_amount'].sum()

# Imprimimos en pantalla los resultados
print(f"Ventas Totales Historicas: ${ventas_totales:,.2f}")
print(f"Producto mas vendido (Simulado): '{producto_mas_vendido}' ({cantidad_maxima} unidades)")
print("Evolucion de Ventas por Mes:")
for mes, total in ventas_por_mes.items():
    print(f"   {mes}: ${total:,.2f}")

# generamos el grafico
plt.figure(figsize=(10, 5))

meses_x = ventas_por_mes.index.astype(str)
totales_y = ventas_por_mes.values

plt.plot(meses_x, totales_y, marker='o', color='#007acc', linewidth=2.5, label='Evolucion de Ventas')

plt.title('Evolucion Temporal de Ventas - Ciclo 2024', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Meses analizados', fontsize=11)
plt.ylabel('Facturacion Total ($)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)

for i, txt in enumerate(totales_y):
    plt.annotate(f"${txt:,.0f}", (meses_x[i], totales_y[i]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=9)

plt.tight_layout()

# guardamos el grafico en la carpeta resultados
ruta_grafico = os.path.join(os.getcwd(), 'resultados', 'evolucion_ventas.png')
plt.savefig(ruta_grafico, dpi=300)
print(f"\nGrafico exportado exitosamente a: {ruta_grafico}")

# mostramos el grafico
plt.show()
