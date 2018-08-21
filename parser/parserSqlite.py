import os
import gzip
from lxml import etree as ET
from database import Database
import timeit


db = Database('./data/music_sep.db')
db.conn.execute("""CREATE TABLE IF NOT EXISTS artist(
                    id integer PRIMARY KEY,
                    name text);""")

db.conn.execute("""DELETE FROM artist""")

gzip_file = gzip.open('./data/discogs_20180801_artists.xml.gz','rb')
f_size = os.path.getsize('./data/discogs_20180801_artists.xml.gz')
start = timeit.default_timer()

idPath = ET.XPath('child::id')
namePath = ET.XPath('child::name')

def parseArtist():
    elem_num = 0
    cur_elem_num = 0
    nodes_tuples = set()
    commit_counter = 0

    for event, elem in ET.iterparse(gzip_file,events=['end'],tag='artist'):

        #nodes_tuples.add((idPath(elem)[0].text,namePath(elem)[0].text))
        nodes_tuples.add((elem.find('id').text,elem.find('name').text))
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        cur_elem_num += 1

        if cur_elem_num > 100000:
            elem_num += cur_elem_num
            print(elem_num)
            cur_elem_num = 0
            if (commit_counter == 10):
                db.conn.executemany("""insert into artist(id,name) values (?,?)""",nodes_tuples)
                db.conn.commit()
                nodes_tuples.clear()
                commit_counter = 0
                print (timeit.default_timer() - start)
                print("Committed")
            else:
                commit_counter += 1 
    db.conn.executemany("""insert into artist(id,name) values (?,?)""",nodes_tuples)
    db.conn.commit()
    print("Done")

parseArtist()

