import requests
import base64
import json
from telegram.ext import MessageHandler, CommandHandler, Filters

if __name__ == "__main__":
    from telegram.ext import Updater
    updater = Updater(token='625197724:AAHQQFZqHv_6GGx1Y0-1O0lTPZXyfC8ul7I')
    dispatcher = updater.dispatcher

    script = []

    def update_script(bot, update, args):
        global script
        script = args
        text = "Script:\n{}".format(" && ".join(script))
        bot.send_message(chat_id=update.message.chat_id, text=text)
    
    def add_script(bot, update, args):
        script.extend(args)
        text = "Script:\n{}".format(" && ".join(script))
        bot.send_message(chat_id=update.message.chat_id, text=text)

    def analyze_audio(bot, update):
        formatted_script = []
        for root_t in script:
            formatted_script.append(root_t.split('|'))
        voice = update.message.voice
        binary_voice = voice.get_file().download_as_bytearray()
        b64_voice = base64.b64encode(binary_voice).decode()
        rsp = requests.post("http://127.0.0.1:5000", json={"voice": b64_voice, "words": formatted_script})
        data = rsp.json()
        text = "RESULTS\nText: {}\nQuality: {}%\nNot found: {}".format(data['text'], int(data['quality'] * 100), ", ".join(data['not_found']))
        bot.send_message(chat_id=update.message.chat_id, text=text)

    update_script_handler = CommandHandler('update', update_script, pass_args=True)
    add_script_handler = CommandHandler('add', add_script, pass_args=True)
    analyze_audio_handler = MessageHandler(Filters.voice, analyze_audio)
    dispatcher.add_handler(update_script_handler)
    dispatcher.add_handler(add_script_handler)
    dispatcher.add_handler(analyze_audio_handler)
    updater.start_polling()