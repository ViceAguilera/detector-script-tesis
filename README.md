# Detector de patentes para el control de acceso en tiempo real

###### **🚧 V2.0 Beta development.🚧🔨**

_Sistema de reconocimiento automático de matrículas vehiculares y API para el control de acceso en tiempo real_

## Construido con 🛠️

- [Python v3.9](https://www.python.org/) - Lenguaje de programación
- [OpenCV](https://opencv.org/) - Librería de visión artificial
- [Ultralytics](https://ultralytics.com/) - Librería de modelo de detección de objetos
- [DepthAI](https://docs.luxonis.com/en/latest/) - Librería de cámara OAK-1 POE
- [Easy OCR](https://www.jaided.ai/easyocr/) - Librería de reconocimiento óptico de caracteres

## Comenzando 🚀

### Instalacion  🔧

1. Se debe instalar venv
    ```bash
    sudo apt-get install python3.9-venv
    ```
  
2. Se debe instalar un packete para OpenCV
    ```bash
    sudo apt-get update && apt-get install -y libgl1-mesa-glx
    ```

3. Se clona el repositorio de GitHub
    ```bash
    git clone https://github.com/ViceAguilera/detector-script-tesis.git detector-script
    ```
  
4. Se ingresa a la carpeta del proyecto
    ```bash
    cd detector-script
    ```
  
5. Se crea un entorno virtual
    ```bash
    python3.9 -m venv venv
    ```
    
6. Se activa el entorno virtual
    ```bash
    source venv/bin/activate
    ```

7. Se instala los requerimientos del proyecto
    ```bash
    pip install -r requirements.txt
    ```

8. Para el envio de datos se debe crear archivo .env, siguiendo el ejemplo de `.env.example`
  

9. Se ejecuta el script
    ```bash
    python3.9 main.py
    ```
   
## Licencia 📄

Este proyecto está bajo el _GNU AFFERO GENERAL PUBLIC LICENSE_ - mira el archivo [LICENSE](LICENSE) para detalles

## Autores ✒️

[**Camilo Sáez Garrido**](https://github.com/camjasaez) & [**Vicente Aguilera Arias**](https://github.com/ViceAguilera)