
import os
from flask import render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from app import app
import soundcloud
from pydub import AudioSegment


@app.route('/')
def layout():
	return render_template('layout.html')

@app.route('/toSoundCloud', methods=['GET','POST'])
def toSoundCloud():
    if request.method == 'POST':
        file_name = request.form.get('filename', 'POST')     
        # create client object with app credentials
        client = soundcloud.Client(client_id='ba6a642eb34899653d0a7765594ba454',client_secret='6e9ac7bfb12d3a8f4e0491a4f315a826',username = 'acejang', password = 'Jbh591411')
        # upload audio file
        track = client.post('/tracks', track={'title': 'new ' + file_name,'asset_data': open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'rb')})
        # print track.permalink_url
    return render_template('layout.html')


# @app.route('/changed')
# def change():
#     AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
#     song = AudioSegment.from_mp3("Pharrell_Williams_Happy.mp3")
#     seconds = 2000
#     #  .duration_seconds
#     first = song[:seconds]
#     middle = song[seconds:-seconds]
#     last = song[-seconds:]

#     new_song = last + middle+ first
#     new_song.export("newSong.mp3", format="mp3")

#     return render_template('changed.html', filename=filename)


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            

            AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
            song = AudioSegment.from_mp3(file_path)
            seconds = 2000
            #  .duration_seconds
            first = song[:seconds]
            middle = song[seconds:-seconds]
            last = song[-seconds:]

            new_song = last + middle+ first
            new_song.export(file_path, format="mp3")


            return render_template('layout.html', filename=filename)
    return render_template('layout.html')
 
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)