import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, jsonify

Name_mapping = [
    {'id': 0, 'title': 'The Basic'}, 
    {'id': 1, 'title': 'Basic Dart'}, 
    {'id': 2, 'title': 'The Stable'}, 
    {'id': 3, 'title': 'The Buzz'}, 
    {'id': 4, 'title': 'The Sprinter'},
    {'id': 5, 'title': 'The Sea Glider'}, 
    {'id': 6, 'title': 'Hunting Flight'}, 
    {'id': 7, 'title': 'Heavy-Nosed Plane'}, 
    {'id': 8, 'title': 'Royal Wing'}, 
    {'id': 9, 'title': 'Gliding Plane'}, 
    {'id': 10, 'title': 'Tailed Plane'}, 
    {'id': 11, 'title': 'Star Wing'}, 
    {'id': 12, 'title': 'Water Plane'}, 
    {'id': 13, 'title': 'The UFO'}, 
    {'id': 14, 'title': 'Cross Wing'}, 
    {'id': 15, 'title': 'Spin Plane'}, 
    {'id': 16, 'title': 'Stunt Plane'}, 
    {'id': 17, 'title': 'The Square'}, 
    {'id': 18, 'title': 'Origami Plane'}, 
    {'id': 19, 'title': 'Eagle Eye'}, 
    {'id': 20, 'title': 'White Dove'}, 
    {'id': 21, 'title': 'Fast Hawk'}, 
    {'id': 22, 'title': 'King Bee'}, 
    {'id': 23, 'title': 'Zip Dart'}, 
    {'id': 24, 'title': 'Jet Fighter'}, 
    {'id': 25, 'title': 'Underside Plane'}, 
    {'id': 26, 'title': 'Sailor Wing Plane'}, 
    {'id': 27, 'title': 'Lock-Bottom Plane'}, 
    {'id': 28, 'title': 'The Bird'}, 
    {'id': 29, 'title': 'Fast Swallow'}, 
    {'id': 30, 'title': 'Soaring Eagle'},
    {'id': 31, 'title': 'Navy Plane'}, 
    {'id': 32, 'title': 'Canard Plane'}, 
    {'id': 33, 'title': 'Tail Spin'}, 
    {'id': 34, 'title': 'Lift Off'}, 
    {'id': 35, 'title': 'V-Wing'}, 
    {'id': 36, 'title': 'Vulture'}, 
    {'id': 37, 'title': 'Sonic Jet'},
    {'id': 38, 'title': 'Spinner Plane'}, 
    {'id': 39, 'title': 'Stealth Glider'},
    {'id': 40, 'title': 'Light Spinner'}, 
    {'id': 41, 'title': 'Fun Flyer'}, 
    {'id': 42, 'title': 'Loop Plane'}, 
    {'id': 43, 'title': 'Wedge Plane'}, 
    {'id': 44, 'title': 'Fast Glider'}, 
    {'id': 45, 'title': 'The Arrow'}, 
    {'id': 46, 'title': 'The Raven'}
]

app = Flask(__name__)

@app.route('/plane/all')
def get_plane_all():

    response = requests.get('https://www.foldnfly.com/#/1-1-1-1-0-0-0-0-2')
    print (response.status_code)

    response.encoding = 'utf-8' # Optional: requests infers this internally
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.find_all('div', id=re.compile("^p"))
    p404 = soup.find_all('div', class_='plane plane404')
    links.pop(0)

    #print(p404) #Secret plane

    data = []

    id = 0

    for plane in links:
    
        diff = plane.find_all('span', class_='diff')
        specs = plane.find_all('div', class_='tags')

        Plane = {
            'id' : id,
            'title' : plane.b.text,
            'desc' : plane.a.attrs['title'],
            'img' : plane.img.attrs['src'],
            'diff' : diff[0].text,
            'specs' : specs[0].text
        }

        id += 1
        data.append(Plane)
        print(Plane)

    return jsonify(data)

@app.route('/plane/find/<number>')
def get_plane(number):

    response = requests.get('https://www.foldnfly.com/' + number + '.html')
    print (response.status_code)

    response.encoding = 'utf-8' # Optional: requests infers this internally
    soup = BeautifulSoup(response.text, 'lxml')
    header = soup.find_all('div', id='hero')
    desc = header[0].find_all('div', class_='description')

    specs_ = {
        'diff_' : desc[0].find_all('i', class_='icon-star')[0].parent.text,
        'nb_fold' : desc[0].find_all('i', class_='icon-fold')[0].parent.text,
        'tag' : desc[0].find_all('i', class_='icon-tag')[0].parent.text,
        #'dist' : desc[0].find_all('i', class_='icon-distance')[0].parent.text,
        #'time' : desc[0].find_all('i', class_='icon-clock')[0].parent.text
    }


    print(specs_)
    return jsonify(specs_)

if __name__ == '__main__':
    app.run() 