# Proyecto-final_WBDS

## 1. Instalación

### Paquetes requeridos para ejecutar el código:

os: Este paquete proporciona una manera de utilizar funciones dependientes del sistema operativo, como la interacción con el sistema de archivos, la lectura y escritura de variables de entorno y la ejecución de comandos del sistema.

pandas: Este paquete proporciona estructuras de datos de alto rendimiento y herramientas de análisis de datos. Utilizado para la manipulación y análisis de datos.

    pip install pandas

sklearn.metrics: Este paquete es parte de scikit-learn y proporciona herramientas para el cálculo de diversas métricas, aquí hacemos uso del Error absoluto medio (MAE), del Error cuadrático medio (MSE) y del R-cuadrado (R2).

    pip install scikit-learn

math: Este paquete proporciona funciones matemáticas comunes, lo utilizamos para calcular la raíz del Error cuadrático medio (RMSE)

shutil: Este paquete proporciona una interfaz de alto nivel para la copia y eliminación de archivos y directorios, lo utilizamos para mover los archivos generados al directorio de análisis.

matplotlib.pyplot: Este paquete proporciona una manera fácil de crear distintos tipos de gráficos.

    pip install matplotlib

Los paquetes "os", "math" y "shutil" son módulos integrados de Python y no requieren instalación adicional.

## 2. Corrida:

Descargar y descomprimir *compare.zip*

* Opción 1: modificar la linea 18 del script *regression_metrics.py* con la dirección al directorio “*compare*”

* Opción 2: ejecutar el script e ingresar por terminal la dirección al directorio “*compare*”

Seguir las indicaciones que se imprimen en pantalla

Al final del análisis se crea un directorio “*analysis*” dentro del directorio “*compare*” donde se encuentran los archivos de salida.
