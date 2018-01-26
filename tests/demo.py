import requests
import sys

url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5001'

pan_tadeusz = requests.get('https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt').text
result = requests.get(url, data={'text': pan_tadeusz})
result.raise_for_status()
print('Took %s' % result.json()['time'])

result = requests.get(url + '/simple', data={'list': ['Ala ma kota! Kot ma Alę.', 'Ciemne pociągi mają dziwne odnogi']})
result.raise_for_status()
print('Result: %s' % result.json()['list'])
print('Took %s' % result.json()['time'])
