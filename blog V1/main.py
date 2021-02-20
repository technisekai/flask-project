from flask import Flask, render_template, url_for
from flask_flatpages import FlatPages
from datetime import datetime

app = Flask(__name__)
app.config['FLATPAGES_EXTENSION'] = '.md'

pages = FlatPages(app)

@app.route('/')
def home():
	return render_template('home.html', judul='Home')
    
@app.route('/artikel/')
def artikel():
	posts = [p for p in pages if "date" in p.meta]
	sorted_pages=sorted(posts, reverse=True, key=lambda page: datetime.strptime(page.meta["date"], "%d %b %y"))
	return render_template('artikel.html', pages=sorted_pages, judul='Artikel')
    
@app.route('/tentang/')
def tentang():
    return render_template('tentang.html', judul='Tentang')
    
@app.route('/artikel/<path:path>.html')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page, judul=path)

if __name__ == '__main__':
	app.run(debug=True)
