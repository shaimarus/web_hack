import json
import random
import time
from datetime import datetime

from flask import Flask, Response, render_template, stream_with_context,request,send_from_directory

import subprocess as sp
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('1.html')

@app.route('/start/')
def index2():
   return render_template('1.html')

@app.route('/upload')
def upload_file():
   return render_template('1.html')

@app.route("/",methods = ['GET', 'POST'])
def get_value_type_file():
    if request.method == 'POST':

        print(request.form.get('type of file'))

        #if request.form['type'] == 'type of file':
        #    print('aaaaaaaaaa')
        #    print(request.form.get('Укажите тип файла'))

    return render_template('1.html')        


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))

      sp.run(['/opt/JohnTheRipper/run/rar2john /opt/hashcat/'+str(f.filename)+' > hassss.txt'], shell=True)
        
      with open('hassss.txt') as f:
          contents = f.read()
    
      with open('hash.txt', 'w') as f:
          f.write(contents[contents.find('.rar:')+5:-1])
      

      return 'Файл успешно загружен! Далее чтобы получить пароль, нажмите кнопку Запустить расшифровку.'



@app.route('/', methods=['GET'])
def dropdown():
    colours = [1, 2, 3, 4]
    return render_template('1.html', colours=colours)

@app.route("/key6.jpg", methods=["GET"])
def image():          
    return send_from_directory('/templates/key6.jpg', 'key6.jpg')

@app.route('/min11', methods=['POST', 'GET'])
def min11():
    if request.method=="POST":
        select_min = request.form.get('min1_value')
        #print(select_min)

    return render_template('1.html',min1=select_min)# just to see what select is

    #print(request.form.items())
    # for key, value in request.form.items():
    #     print("key: {0}, value: {1}".format(key, value))

@app.route('/max11', methods=['POST', 'GET'])
def max11():
    if request.method=="POST":
        select_max = request.form.get('max1_value')
        #print(select_min)
        return render_template('1.html',max1=select_max)# just to see what select is

@app.route('/check_box', methods=['POST', 'GET'])
def box():
    if request.method=="POST":
        print(request.form.get('a'))
        print(request.form.get('b'))
        print(request.form.get('c'))
        print(request.form.get('d'))
   
        #print(select_min)
        return render_template('1.html')# just to see what select is



@app.route('/start/', methods=['POST', 'GET'])
def start():

    result=''
    if request.method == "POST":
        t=sp.check_output(["hashcat","-a","3","-m","13000","/opt/hashcat/hash.txt","-i","--increment-min=1","--increment-max=8","--potfile-disable","-1","?l?u?d",'?1?1?1?1?1?1?1?1'])

        with open('hash_result.txt', 'wb') as f:
            f.write(t)

        with open('hash.txt') as f:
            hash = f.read()

        with open('hash_result.txt') as f:
            contents = f.read()

        l0=contents.rfind('Cracked')
        l1=contents[:l0].rfind(hash)
        l2=contents[l1:][len(hash)+1:].find('\n')
        result=contents[l1:][len(hash)+1:][:l2]
        #print(result)

        #l1=contents.rfind(hash)
        #l2=contents[:l1][contents[:l1].rfind(hash)+len(hash)+1:]
        #result=l2[:l2.find('\n')]
        #print(result)

    try:
        os.remove("/opt/hashcat/my.pot")
    except Exception:
        pass

    #print("iiiiiii")

    #print(t)
    #lines = ['Readme', 'How to write text files in Python']

    return render_template('1.html',password=result)

def get_gpu_memory():
    command = "nvidia-smi --query-gpu=memory.free --format=csv"
    memory_free_info = sp.check_output(command.split()).decode('ascii').split('\n')[:-1][1:]
    memory_free_values = [int(x.split()[0]) for i, x in enumerate(memory_free_info)]
    return memory_free_values

    
@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': get_gpu_memory()})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000,debug=True,threaded=True)

    