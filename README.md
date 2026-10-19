# Detector de patentes para control de acceso en tiempo real

Script de reconocimiento automático de patentes vehiculares (ANPR) para control de acceso, desarrollado como parte de un proyecto de tesis.

![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=flat&logo=python&logoColor=white)
![Ultralytics](https://img.shields.io/badge/Ultralytics-YOLOv8-00FFFF?style=flat)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![Estado](https://img.shields.io/badge/estado-terminado-blue?style=flat)
![Licencia](https://img.shields.io/badge/licencia-AGPL--3.0-blue?style=flat)
![Último commit](https://img.shields.io/github/last-commit/ViceAguilera/detector-script-tesis?style=flat)

<!-- Demo: agrega una captura o GIF en docs/demo.gif y descomenta la línea siguiente -->
<!-- <p align="center"><img src="docs/demo.gif" alt="Demostración del detector de patentes" width="800"></p> -->

## Tabla de contenidos

- [Descripción](#descripción)
- [Estado del proyecto](#estado-del-proyecto)
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Licencia](#licencia)
- [Autores](#autores)

## Descripción

El script detecta vehículos y patentes en un flujo de video, rastrea los vehículos, lee el texto de la patente con OCR y determina si el vehículo entra o sale según su posición en el cuadro. Los registros (patente, confianza, dirección y fotografías) se envían a una API del proyecto de tesis. La fuente de video puede ser una cámara OAK-1 POE o un archivo de video de demostración. Se realizó en colaboración con Camilo Sáez Garrido.

## Estado del proyecto

**Terminado.** Proyecto de tesis de Ingeniería de Ejecución en Computación e Informática (Universidad del Bío-Bío). La última versión publicada es la 2.0 beta y no recibe mantenimiento activo.

## Características

- Detección de vehículos (clases COCO 2 y 7: automóvil y camión) con YOLOv8n.
- Detección de patentes con un modelo YOLO propio (`best.pt`).
- Seguimiento de vehículos con SORT y asociación de cada patente a su vehículo.
- Lectura de la patente con EasyOCR sobre la imagen en escala de grises y realzada.
- Clasificación entrada/salida según la mitad del cuadro en que aparece la patente.
- Filtro de patentes repetidas o muy similares a la última registrada.
- Envío de registros e imágenes a la API configurada por variables de entorno.
- Limpieza diaria de las carpetas de fotografías.
- Modo demostración con video (`test_video.py`), que no requiere cámara ni API.

## Tecnologías

- Python 3.9
- [Ultralytics](https://ultralytics.com/) 8.0.208 (YOLOv8)
- [OpenCV](https://opencv.org/) 4.8.1.78
- [DepthAI](https://docs.luxonis.com/en/latest/) 2.22.0.0 (cámara OAK-1 POE)
- [EasyOCR](https://www.jaided.ai/easyocr/) 1.7.1
- [SORT](https://github.com/abewley/sort) y filterpy para el seguimiento
- python-dotenv, NumPy, Pillow, Matplotlib

## Requisitos

- Python 3.9
- Cámara OAK-1 POE (solo para `main.py`)
- Token de la [API del proyecto](https://github.com/camjasaez/app-tesis.git) (solo para `main.py`)
- Modelos [YOLOv8n](https://drive.google.com/file/d/192QNeCFvm4U-vIagpz0ch6JWcYaOEhG2/view?usp=sharing) (`yolov8n.pt`) y [License Plate](https://drive.google.com/file/d/15urX7tBdBMS8U-yiwdZS0SEx8xvJwKc8/view?usp=sharing) (`best.pt`), que se guardan en la carpeta `model/`
- GPU NVIDIA con CUDA 11.8 opcional

## Instalación

```bash
git clone https://github.com/ViceAguilera/detector-script-tesis.git
cd detector-script-tesis
python -m venv venv
source venv/bin/activate        # En Windows: ./venv/Scripts/activate
pip install -r requirements.txt
```

En Linux, OpenCV puede requerir `sudo apt-get install -y libgl1-mesa-glx`.

Para PyTorch con CUDA 11.8 (opcional):

```bash
pip uninstall -y torch torchvision torchaudio
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Configuración

Copia `.env.example` a `.env` y completa las variables:

```
HOST=       # Dominio del servidor
PORT=       # Puerto del servidor
API_URL=    # URL de la API (si se define, se usa en lugar de HOST y PORT)
TOKEN=      # Token de la cámara
```

Descarga los modelos indicados en Requisitos y colócalos en `model/` como `yolov8n.pt` y `best.pt`.

## Uso

Con la cámara OAK-1 POE conectada (por PoE o por USB con cable de red; ver la [guía de Luxonis](https://docs.luxonis.com/projects/hardware/en/latest/pages/guides/getting-started-with-poe/#getting-started-with-oak-poe-devices)):

```bash
python main.py
```

Demostración con el video incluido (`video.mp4`):

```bash
python test_video.py
```

Presiona `q` para cerrar la ventana de video.

## Estructura del proyecto

```
main.py          # Flujo en tiempo real con cámara OAK-1 POE y envío a la API
test_video.py    # Demostración con video, sin API
util.py          # OCR, asociación vehículo-patente, envío HTTP y utilidades
sort/            # Implementación del seguimiento SORT
model/           # Modelos YOLO (se descargan aparte)
photos/          # Capturas de vehículos y patentes
video.mp4        # Video de demostración
.env.example     # Plantilla de variables de entorno
```

## Licencia

Distribuido bajo la licencia GNU AGPL-3.0. Ver [LICENSE](LICENSE).

## Autores

**Vicente Aguilera Arias** — [Portafolio](https://portfolio.iamsirius.cl) · [GitHub](https://github.com/ViceAguilera) · [LinkedIn](https://www.linkedin.com/in/vicenteaguilera/)

Colaborador: [Camilo Sáez Garrido](https://github.com/camjasaez)
