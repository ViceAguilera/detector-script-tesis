FROM python:3.9

WORKDIR /app

COPY ./ /app

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx

CMD ["python3.9", "test_video.py"]
