from gtts import gTTS

text_val = 'Hello, how can I assist you today?'
language = 'en'

my_obj = gTTS(text=text_val, lang=language, slow=False)

my_obj.save("welcome.mp3")