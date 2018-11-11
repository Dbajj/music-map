import csv
from lxml import etree as ET
import xml.etree.ElementTree as ETC
import gzip
import os
import sys
import timeit
import pdb
import pickle
import argparse


start = timeit.default_timer()

def buildMasterDict(masterxml_path):
    print('Building master dictionary')
    print(masterxml_path)
    print(os.getcwd())
    release_dict = dict()
    master_file = gzip.open(masterxml_path,'rb')
    elem_num = 0
    cur_elem_num = 0
    for event, elem in ET.iterparse(master_file,events=['end'],tag='master'):
        release_dict[elem.find('main_release').text] = elem.get('id')
        cur_elem_num +=1 
        elem.clear()
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        if(cur_elem_num > 10000):
            elem_num += cur_elem_num
            cur_elem_num = 0
            sys.stdout.write('\r'+str(elem_num))
            sys.stdout.flush()

    os.makedirs(os.path.dirname('./obj/release_dict.pkl'),exist_ok=True)
    pickle.dump(release_dict,open('obj/release_dict.pkl','wb'),pickle.HIGHEST_PROTOCOL)
    print('Done')



def parseArtist(artistxml_path):
    print('Parsing artists')
    gzip_file = gzip.open(artistxml_path,'rb')

    os.makedirs(os.path.dirname('./data/csv/artist.csv'),exist_ok=True)
    cur_writer = csv.writer(open('./data/csv/artist.csv', 'w'), dialect='unix',quoting=csv.QUOTE_NONNUMERIC)
    elem_num  = 0
    cur_elem_num = 0
    nodes_tuples = []
    commit_counter = 0

    for event, elem in ET.iterparse(gzip_file,events=['end'],tag='artist'):
        name = elem.find('name').text 
        id = int(elem.find('id').text)

        nodes_tuples.append((id,name,'Artist'))
        elem.clear()
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        cur_elem_num += 1

        if cur_elem_num > 10000:
            elem_num += cur_elem_num
            print(elem_num)
            cur_elem_num = 0
            if (commit_counter == 10):
                cur_writer.writerows(nodes_tuples)
                nodes_tuples.clear()
                commit_counter = 0
                print (timeit.default_timer() - start)
                print("Committed")
            else:
                commit_counter += 1 
    print("Done")


def parseReleases(fileName):
    print('Parsing releases')
    release_dict = pickle.load(open('obj/release_dict.pkl','rb'))

    gzip_file = gzip.open(fileName,'rb')
    os.makedirs(os.path.dirname('./data/csv/release.csv'),exist_ok=True)
    cur_writer = csv.writer(open('./data/csv/release.csv','w'),delimiter=',')
    elem_num = 0
    cur_elem_num = 0
    commit_counter = 0
    nodes_tuples = []

    for event, elem in ET.iterparse(gzip_file,events=['end'],tag='release'):
        release_id = elem.get('id')
        if (release_id is not None and release_id in release_dict):
            parseReleaseElem(elem,nodes_tuples,release_dict)
        cur_elem_num += 1
        elem.clear()
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        if  len(nodes_tuples) > 1000:
            elem_num += cur_elem_num
            print(elem_num)
            cur_elem_num = 0
            cur_writer.writerows(nodes_tuples)
            nodes_tuples.clear()
            del nodes_tuples[:]
            commit_counter = 0
            print (timeit.default_timer() - start)
            print("Committed")

    cur_writer.writerows(nodes_tuples)
    nodes_tuples.clear()
    del nodes_tuples[:]
    print('Done')


def countReleases():
    gzip_file = gzip.open('./data/discogs_20180701_releases.xml.gz','rb')
    cur_writer = csv.writer(open('./data/csv/release.csv','w'),delimiter=',')
    tree = ET.parse(gzip_file)
    num_elems = tree.xpath("count(//release)")

def getElemText(elem, find_string):
    find_elem = elem.find(find_string)

    if find_elem is not None:
        return find_elem.text
    else:
        return None

def parseReleaseElem(elem,batch,release_dict):
    master_id = release_dict[elem.get('id')]
    main_artist_id = getElemText(elem, 'artists/artist/id')
    title = getElemText(elem, 'title')
    year = getElemText(elem, 'released')
    for extra in elem.findall('.//extraartists/artist'):
        extra_id = extra.find('id').text
        if (extra.find('role').text == "Featuring" and extra_id != main_artist_id):    
            batch.append((main_artist_id,master_id,title,year,extra_id))
    return




def printFile(name):
    gzip_file = gzip.open(name,'r')
    for line in gzip_file:
        print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description ="""Parse discogs xml data 
            into csv files""")
    parser.add_argument('masters_path',metavar="M",type=str,help="""path of masters xml
            file""")
    parser.add_argument('artists_path',metavar="A",type=str,help="""path of masters xml
            file""")
    parser.add_argument('releases_path',metavar="R",type=str,help="""path of masters xml
            file""")

    args = parser.parse_args()
#    buildMasterDict(args.masters_path)
#    parseArtist(args.artists_path)
    parseReleases(args.releases_path)


