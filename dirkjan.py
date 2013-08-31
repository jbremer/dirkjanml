import bs4
import hashlib
import os
import requests
import sqlite3


DJ_URL = ''
DJ_SECRET = ''


def insert_strip(date, title, fname):
    try:
        c.execute('INSERT INTO strips VALUES (?, ?, ?, ?)',
                  (None, date, title, fname))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def submit_strip(title, url):
    """Because we send the email from another box.."""
    data = {'title': title, 'url': url, 'secret': DJ_SECRET}
    assert requests.get(DJ_URL, params=data).status_code == 200


def latest_strips():
    r = requests.get('http://www.veronicamagazine.nl/entertainment/strips')
    assert r.status_code == 200

    r = bs4.BeautifulSoup(r.content)

    for div in r.find_all('div', attrs={'class': 'strips'}):
        img_src = div.find('img').attrs['src']
        img_src = 'http://www.veronicamagazine.nl' + img_src
        date = div.find('meta', itemprop='datePublished').attrs['content']
        title = div.find('meta', itemprop='name').attrs['content']

        img_content = requests.get(img_src).content
        fname = hashlib.md5(img_content).hexdigest() + '.jpg'
        fname = os.path.join('strips', fname)

        open(fname, 'wb').write(img_content)
        if insert_strip(date, title, fname):
            submit_strip(title, img_src)


if __name__ == '__main__':
    if not os.path.exists('strips'):
        os.mkdir('strips')

    conn = sqlite3.connect('dirkjan.db')
    c = conn.cursor()

    try:
        c.execute('CREATE TABLE strips (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                  'date TEXT UNIQUE, title TEXT UNIQUE, fname TEXT UNIQUE)')
    except sqlite3.OperationalError:
        pass

    latest_strips()

    c.close()
    conn.close()
