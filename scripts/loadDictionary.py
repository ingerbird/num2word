import os
from urllib import request
from zipfile import ZipFile
import sqlite3

DATABASE_DIR = '../database/'
DATA_FILES_DIR = DATABASE_DIR + 'data_files/'
DATABASE_NAME = 'num2word.db'
LETTER_DICT_RU = {'н': '0', 'м': '0', 'г': '1', 'ж': '1', 'д': '2', 'т': '2', 'к': '3', 'х': '3', 'ч': '4', 'щ': '4',
      'п': '5', 'б': '5', 'ш': '6', 'л': '6', 'с': '7', 'з': '7', 'в': '8', 'ф': '8', 'р': '9', 'ц': '9'}

def calc_word2num(word):
    num = ''
    for l in word:
        num += LETTER_DICT_RU.get(l, '')
    return num

def load_dictionary_files():
    try:
        f = open('../conf/dictionary_RU.txt')
        for url in f:
            if url[0] == '#' or url == '':
                continue
            print(url)
            if not os.path.exists(DATA_FILES_DIR):
                os.mkdir(DATA_FILES_DIR)
            dest = DATA_FILES_DIR + url.split('/')[-1]
            request.urlretrieve(url, dest)
            zip = ZipFile(dest)
            zip.extractall(DATA_FILES_DIR)
            zip.close()
            os.remove(zip.filename)
    finally:
        f.close()


def load_file_to_database(filename):
    if not os.path.exists(filename):
        exit()
    con = sqlite3.connect(DATABASE_DIR + DATABASE_NAME)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS words")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value_text TEXT NOT NULL,
            value_num TEXT NOT NULL
        )

        ''')
    #data = [[row.split('\t'), 121] for row in open(filename, 'r').readlines()]
    data = []
    for row in open(filename, 'r'):
        data.append([row, calc_word2num(row)])
    #data = [[1, 1], [2, 2]]
    #print(data[:10])
    cur.executemany("INSERT INTO words (value_text, value_num) VALUES (?, ?);", data)
    con.commit()