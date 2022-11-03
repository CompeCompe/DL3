import os
import telebot
import requests
import subprocess
import ffmpeg

from vosk import Model, KaldiRecognizer
import wave
import json

token = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)
model = Model('model')

def audio_to_text(input_file: str):

    # open audio file
    wf = wave.open(input_file, "rb")
    
    # Initialize model
    rec = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000) # use buffer of 4000
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            pass

    # Get final bits of audio and flush the pipeline
    final_result = json.loads(rec.FinalResult())

    return final_result["text"]

@bot.message_handler(content_types=['voice'])
def get_audio_messages(message):
    try:
        # Get file from TG
        file_info = bot.get_file(message.voice.file_id)
        path = os.path.splitext(file_info.file_path)[0] 
        fname = os.path.basename(path)
        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path)) 
        with open(fname+'.oga', 'wb') as f:
            f.write(doc.content)
        # Transform from OGA to WAV
        process = subprocess.run(['ffmpeg', '-i', fname+'.oga', fname+'.wav'])
        # Calling ASR func
        result = audio_to_text(fname+'.wav') 
        bot.send_message(message.from_user.id, format(result))
    finally:
        os.remove(fname + '.wav')
        os.remove(fname + '.oga')

bot.polling(none_stop=True, interval=0)