# Tarea1IA
Para correr el programa basta con escribir el siguiente comando en la terminal:
```
python3 main.py
```
Esto imprimirá en la terminal el resultado de la ejecución del programa, siendo esto:
```
Nombre del Método
Si encontró solución
Path de la solución
Numeros de nodos expandidos por cada nodo
Numero total de nodos expandidos
Costo del camino
En caso de ser optimo, lo dirá
```

En caso de querer cambiar el archivo de entrada, basta con cambiar el nombre del archivo en la linea 5 del archivo main.py
```
file = open("nombreArchivo.txt", "r")
```

El archivo de entrada debe tener el siguiente formato:
```
Init: X
Goal: Y
Nombre_nodo Valor_heuristico
Nombre_nodo Valor_heuristico
Nombre_nodo Valor_heuristico
Nombre_nodo Valor_heuristico
Nombre_nodo Valor_heuristico
Nombre_nodo Valor_heuristico
Nombre_nodo Nombre_nodo Costo_viaje
Nombre_nodo Nombre_nodo Costo_viaje
Nombre_nodo Nombre_nodo Costo_viaje
Nombre_nodo Nombre_nodo Costo_viaje
Nombre_nodo Nombre_nodo Costo_viaje
```