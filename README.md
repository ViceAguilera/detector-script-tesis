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

<details>
   <summary>Linux</summary>

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
   
8. Se desinstala pytorch
    ```bash
    pip uninstall -y torch torchvision torchaudio
    ```

8. Se instala CUDA Pytorch
    ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

9. Para el envio de datos se debe crear archivo .env, siguiendo el ejemplo de `.env.example`

10. Se solicita el token de la [API](https://github.com/camjasaez/app-tesis.git) y se agrega al archivo `.env`

11. Se descarga los modelos de [Yolov8n](https://drive.google.com/file/d/192QNeCFvm4U-vIagpz0ch6JWcYaOEhG2/view?usp=sharing) y [License Plate](https://drive.google.com/file/d/15urX7tBdBMS8U-yiwdZS0SEx8xvJwKc8/view?usp=sharing) y se agregan a la carpeta `model`

12. Se ejecuta el script
    ```bash
    python3.9 main.py
    ```
</details>

<details>
  <summary>Windows</summary>

1. Se clona el repositorio de GitHub
    ```bash
    git clone https://github.com/ViceAguilera/detector-script-tesis.git detector-script
    ```
  
2. Se ingresa a la carpeta del proyecto
    ```bash
    cd detector-script
    ```
  
3. Se crea un entorno virtual
    ```bash
    python -m venv venv
    ```
    
4. Se activa el entorno virtual
    ```bash
    ./venv/Scripts/activate
    ```
   
5. Se instala los requerimientos del proyecto
    ```bash
    pip install -r requirements.txt
    ```
6. Se desinstala pytorch
    ```bash
    pip uninstall -y torch torchvision torchaudio
    ```

7. Se instala CUDA Pytorch
    ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

8. Para el envio de datos se debe crear archivo .env, siguiendo el ejemplo de `.env.example`

10. Se solicita el token de la [API](https://github.com/camjasaez/app-tesis.git) y se agrega al archivo `.env`

11. Se descarga los modelos de [Yolov8n](https://drive.google.com/file/d/192QNeCFvm4U-vIagpz0ch6JWcYaOEhG2/view?usp=sharing) y [License Plate](https://drive.google.com/file/d/1jnWNCFfGbEt28cYrH8P74t2FguwCD3vP/view?usp=sharing) y se agregan a la carpeta `model`

12. Se ejecuta el script
    ```bash
    python main.py
    ```
</details>
   
## Licencia 📄

Este proyecto está bajo el _GNU AFFERO GENERAL PUBLIC LICENSE_ - mira el archivo [LICENSE](LICENSE) para detalles

## Autores ✒️

[**Camilo Sáez Garrido**](https://github.com/camjasaez) & [**Vicente Aguilera Arias**](https://github.com/ViceAguilera)