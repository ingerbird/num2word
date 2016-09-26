import sqlite3

from loadDictionary import DATABASE_DIR, DATABASE_NAME


def get_word_by_num(num_str, limit = 10):
    con = sqlite3.connect(DATABASE_DIR + DATABASE_NAME)
    cur = con.cursor()
    cur.execute('SELECT value_text FROM words WHERE value_num = ? LIMIT ?', [num_str, limit])
    return cur.fetchall()


def recur_collect_result(phrase, shift):
    res = []
    if len(get_word_by_num(phrase)) > 0:
        res.append([shift, shift + len(phrase), get_word_by_num(phrase)])
        return res
    else:
        found = 0
        m = len(phrase) - 1 if len(phrase) > 1 else 0
        while m >= 1 or m == 0:
            for k in range(0, len(phrase) - m + 1):
                if len(get_word_by_num(phrase[k:k+m])) > 0:
                    res.append([shift + k, shift + k + m, get_word_by_num(phrase[k:k+m])])
                    found = 1
                    break
            if found == 1:
                break
            m -= 1
        if found == 1:
            if k > 0:
                res.append(recur_collect_result(phrase[0:k], shift))
            elif k == 0 or k + m < len(phrase):
                res.append(recur_collect_result(phrase[k+m:], shift + k+m))
        return res

str = '89268288230'
print(recur_collect_result(str, 0))