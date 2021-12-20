import urllib.parse, urllib.request, urllib.error, json
from flask import Flask, render_template, request

app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys = True, indent = 2)

url = "https://elephant-api.herokuapp.com/elephants/random"

def get_elephant():
    try:
        result = urllib.request.urlopen(url).read()
        return json.loads(result)
    except urllib.error.URLError as e:
        print('Error trying to retrieve data: HTTP Error %d: %s' %(e.code, e.reason))
        return None

def elephant_list():
    try:
        result = urllib.request.urlopen('https://elephant-api.herokuapp.com/elephants').read()
        return json.loads(result)
    except urllib.error.URLError as e:
        print('Error trying to retrieve data: HTTP Error %d: %s' %(e.code, e.reason))
        return None

@app.route('/', methods = ['GET', 'POST'])
def main_handler():
    if request.method == 'POST':
        random = get_elephant()
        while '__v' in random[0].keys():
            random = get_elephant()
        elephant = {}
        list = elephant_list()
        for e in list:
            if e['_id'] == random[0]['_id']:
                elephant['name'] = e['name']
                elephant['species'] = e['species']
                elephant['sex'] = e['sex']
                elephant['dob'] = e['dob']
                elephant['dod'] = e['dod']
                elephant['image'] = e['image']
                elephant['note'] = e['note']
                return render_template("index.html",
                    elephant = elephant
                )
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host = 'localhost', port = 8080, debug = True)