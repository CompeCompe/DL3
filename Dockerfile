FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN wget https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip
RUN unzip vosk-model-ru-0.22.zip
RUN mv vosk-model-ru-0.22 model


COPY . .

ENV TELEGRAM_TOKEN put yor own token

CMD [ "python", "bot.py" ]