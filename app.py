from pytubefix import YouTube 
from pytubefix.cli import on_progress
from flask import Flask, render_template,request, redirect, url_for, session

app = Flask(__name__)
urlc = "https://www.youtube.com/watch?v=7X2TAY0U0LI" 
app.secret_key = "une_clef_secrete"

translations = {
    "fr": {
        "title": "AudioPulse",
        "subtitle": "Entrez une URL YouTube, puis téléchargez-la dans le mode de votre choix.",
        "enter_url": "Entrez une URL :",
        "choose_mode": "Choisissez un mode :",
        "download": "Télécharger",
        "placeholder": "https://exemple.com"
    },
    "en": {
        "title": "AudioPulse",
        "subtitle": "Enter a YouTube URL, then download it in the mode of your choice.",
        "enter_url": "Enter a URL:",
        "choose_mode": "Choose a mode:",
        "download": "Download",
        "placeholder": "https://example.com"
    },
    "es": {
        "title": "AudioPulse",
        "subtitle": "Introduce una URL de YouTube y descárgala en el modo que prefieras.",
        "enter_url": "Introduce una URL:",
        "choose_mode": "Elige un modo:",
        "download": "Descargar",
        "placeholder": "https://ejemplo.com"

    },
    "ru": {
        "title": "АудиоПульс",
        "subtitle": "Введите ссылку на YouTube и скачайте в нужном вам режиме.",
        "enter_url": "Введите ссылку:",
        "choose_mode": "Выберите режим:",
        "download": "Скачать",
        "placeholder": "https://пример.com"

    },
    "zh": {
        "title": "音频脉冲",
        "subtitle": "输入一个 YouTube 链接，然后以您选择的模式下载。",
        "enter_url": "输入一个链接：",
        "choose_mode": "选择模式：",
        "download": "下载",
        "placeholder": "https://示例.com"

    }
}

def downloadmp4(url):
    yt = YouTube(url, on_progress_callback=on_progress) 
    print(f"Téléchargement de : {yt.title}") 
    ys = yt.streams.get_highest_resolution() 
    ys.download()
    
def downloadmp3(url):
    yt = YouTube(url, on_progress_callback=on_progress) 
    print(f"Téléchargement de : {yt.title}") 
    ys = yt.streams.get_audio_only() 
    ys.download()
@app.route('/')
def index():
    t = session.get('lang', 'en')
    return render_template('index.html',t=t,translations=translations)

@app.route('/mode',methods=['GET', 'POST'])
def download():
    t = session.get('lang', 'en')  # récupère la langue depuis la session

    if request.method == 'POST':
        url = request.form.get('url')
        mode = request.form.get('mode')
        if not "https://www.youtube.com/watch" in url:
            return render_template('index.html',t=t,translations=translations)

        if mode == 'mp3':
            downloadmp3(url)
        elif mode == 'mp4':
            downloadmp4(url)
    return render_template('index.html',t=t,translations=translations)


@app.route('/langue',methods=['GET', 'POST'])
def set_lang():
    language = request.form.get('language')

    if language in translations:
        session['lang'] = language
    return redirect(url_for('index'))
    


if __name__ == '__main__':
    app.run(debug=True)



