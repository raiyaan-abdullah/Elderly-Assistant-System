import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone(1) as source:
    print('Listening.....')
    r.pause_threshold = 1
    r.energy_threshold = 4000
    audio = r.listen(source)
    query = r.recognize_google(audio, language='en-in')
    print(query)