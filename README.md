# Detector de patentes para el control de acceso en tiempo real

###### **🚧 V1.0 Deta development.🚧🔨**

_Sistema de reconocimiento automático de matrículas vehiculares y API para el control de acceso en tiempo real_

## Construido con 🛠️

- [Python v3.9](https://www.python.org/) - Lenguaje de programación

### Pre-requisitos de desarrollo 📋

Para poder ejecutar el proyecto se necesita tener instalado:

- [Git](https://git-scm.com/downloads) - Control de versiones de código

_El entorno de desarrollo utilizado fue Windows 10 Version 22H2 (OS Build 19045.3208)_

## Configuraciones de ejecución para entorno de produccion

### Instalacion

- Se debe instalar venv
  ```bash
  sudo apt-get install python3.9-venv
  ```
  
- Se debe instalar un packete para OpenCV
  ```bash
  sudo apt-get update && apt-get install -y libgl1-mesa-glx
  ```

- Se clona el repositorio de GitHub
  ```bash
  git clone https://github.com/ViceAguilera/detector-script-tesis.git detector-script
  ```
  
- Se ingresa a la carpeta del proyecto
  ```bash
  cd detector-script
  ```
  
- Se crea un entorno virtual
  ```bash
  python3.9 -m venv venv
  ```
  
- Se activa el entorno virtual
  ```bash
  source venv/bin/activate
  ```

- Se instala los requerimientos del proyecto
  ```bash
  pip install -r requirements.txt
  ```
  
- Se ejecuta el script
  ```bash
  python3.9 main.py
  ```

## Construido con 
- [OpenCV](https://opencv.org/) - Librería de visión artificial
- [Ultralytics](https://ultralytics.com/) - Librería de modelo de detección de objetos
- [DepthAI](https://docs.luxonis.com/en/latest/) - Librería de cámara OAK-1 POE

## Licencia 📄

Este proyecto está bajo el MIT License - mira el archivo [LICENSE](LICENSE) para detalles

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](CONTRIBUTING.md) para mas detalles.