from lxml import etree as ET
import os
import gzip
from digraph import Session,Node
import pdb
import timeit



session = Session()

gzip_file = gzip.open('./data/discogs_20180801_artists.xml.gz','rb')
f_size = os.path.getsize('./data/discogs_20180801_artists.xml.gz')
start = timeit.default_timer()

def parseRaw():
    elem_num = 0
    cur_elem_num = 0
    nodes_maps = []
    commit_counter = 0

    for event, elem in ET.iterparse(gzip_file,events=['end']):
        if (elem.tag == 'artist'):
            cur_dict = {}
            cur_dict['artist_id'] = elem.find('id').text
            cur_dict['artist_name'] = elem.find('name').text
            nodes_maps.append(cur_dict)
            elem.clear()
            cur_elem_num += 1

        if cur_elem_num > 100000:
            elem_num += cur_elem_num
            print(elem_num)
            cur_elem_num = 0
            if (commit_counter == 2):
                session.execute(
                         Node.__table__.insert().values(nodes_maps)
                            )
                #session.commit()
                nodes_maps.clear()
                commit_counter = 0
                print (timeit.default_timer() - start)
                print("Committed")
            else:
                commit_counter += 1 
    session.commit()
    session.close()
    print("Done")

def parseFancy():
    elem_num = 0
    cur_elem_num = 0
    nodes_maps = []
    commit_counter = 0

    for event, elem in ET.iterparse(gzip_file,events=['end']):
        if (elem.tag == 'artist'):
            cur_dict = {}
            cur_dict['artist_id'] = elem.find('id').text
            cur_dict['artist_name'] = elem.find('name').text
            nodes_maps.append(cur_dict)
            elem.clear()
            cur_elem_num += 1

        if cur_elem_num > 100000:
            elem_num += cur_elem_num
            print(elem_num)
            cur_elem_num = 0
            if (commit_counter == 2):
                session.bulk_insert_mappings(Node,nodes_maps)
                session.commit()
                print (timeit.default_timer() - start)
                nodes_maps.clear()
                commit_counter = 0
                print("Committed")
            else:
                commit_counter += 1 
    session.close()
    print("Done")


parseRaw()
