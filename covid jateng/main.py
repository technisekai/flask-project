import requests
import json
from pymonad.Reader import curry
from flask import Flask, render_template, url_for, request


app = Flask(__name__)
data_kab = {}

# Implementasi studi 5 PyMonad
@curry
def tambah_data(x, y):
	return x + y
@curry
def kurang_data(x, y):
	return x - y
    
# Halaman awal
@app.route('/')
def home():
	data_covid = requests.get('https://api.kawalcorona.com/indonesia/provinsi/').json()
	covid_jateng = [data_covid[3]['attributes']['Kasus_Posi'], data_covid[3]['attributes']['Kasus_Semb'], data_covid[3]['attributes']['Kasus_Meni']]
	return render_template('home.html', info_covid = covid_jateng, judul='Home')
    
# Halaman detail kasus per kabupaten
@app.route('/detail/')
def detail():
	return render_template('detail.html', info_covid=data_kab, judul='Detail')

# Halaman detail kasus per kabupaten
@app.route('/data', methods = ['POST', 'GET'])
def data():	
	# Menerima data
	if request.method == 'POST':
		lokasi = request.form['lokasi']
		positi = int(request.form['positif'])
		sembuh = int(request.form['sembuh'])
		mening = int(request.form['meninggal'])
	
	# Cek data apakah sudah ada sebelumnya (implement PyMonad)
	if lokasi in data_kab:
		naik_p = tambah_data(data_kab[lokasi]['posi'])
		positi = naik_p(positi)
		naik_s = tambah_data(data_kab[lokasi]['semb'])
		sembuh = naik_s(sembuh)
		naik_m = tambah_data(data_kab[lokasi]['meni'])
		mening = naik_m(mening)
	
	# PyNonad multiplication operator
	k_aktif = kurang_data(positi) * tambah_data(sembuh)
			
	# Membuat data per kabupaten format json
	data_kab[lokasi] = {'posi': positi,	'semb': sembuh, 'meni': mening, 'aktif': k_aktif(mening)}
	with open('data_per_kab.json', 'w') as fp:
		json.dump(data_kab, fp)
		
	return render_template('detail.html', info_covid=data_kab, judul='Detail')
	
    
# Halaman untuk menambah data
@app.route('/detail/tambah/')
def tambah():
	return render_template('tambah.html', info_covid = data_kab, judul='Tambah')

# Halaman tentang
@app.route('/tentang/')
def tentang():
    return render_template('tentang.html', judul='Tentang')

if __name__ == '__main__':
	app.run(debug=True)
