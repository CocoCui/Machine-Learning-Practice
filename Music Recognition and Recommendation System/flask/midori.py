from flask import Flask, render_template, request, redirect
import subprocess, os
import scipy.io.wavfile as wav
import json
app = Flask(__name__, static_url_path='/static')

songsName = {}
recommendation = {}
@app.route('/')
def index():
    return render_template('index.html')

def generateInput():
    output = open("./tmp/input.txt","w")
    (rate,sig) = wav.read("./tmp/x.wav")
    output.write(str(rate) + "\t")
    for i in sig:
        output.write(str(i[0]) + " ")
    output.close()


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        #return json.dumps(zip(range(1,11),range(1,11)))
        file.save('./tmp/x.wav')
        generateInput()
        os.system("hdfs dfs -rm /input.txt")
        os.system("hdfs dfs -put tmp/input.txt /")
        result = os.popen('spark-submit search.py').read()
        print '--------'
        print result
        print '--------'
        result = [(int(x), songsName[int(x)]) for x in result.split('\n') if str.isdigit(x)]
        return json.dumps(result)

@app.route('/song/<int:songId>')
def song(songId, songsName=songsName):
    name = songsName[songId]
    print name
    name = unicode(name, 'utf8')
    songsList = recommendation[songId]
    songsName = [unicode(songsName[x], 'utf8') for x in songsList]
    return render_template('song.html', name=name, songsList=songsList, songsName=songsName)

if __name__ == '__main__':
    with open('songlist', 'r') as fin:
        for line in fin.readlines():
            x, y = line.split('\t')
            songsName[int(y)] = x
    
    with open('recommendall', 'r') as fin:
        for line in fin.readlines():
            x = map(int, line.split())
            recommendation[x[0]] = x[1:]
            
    app.run(debug=True, port=8888, threaded=True)
