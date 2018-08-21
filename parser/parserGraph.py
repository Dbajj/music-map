import csv
from lxml import etree as ET
import xml.etree.ElementTree as ETC
import gzip
import timeit
import pdb
import pickle


start = timeit.default_timer()

def buildMasterDict():
    release_dict = dict()
    master_file = open('./data/discogs_20180101_masters.xml','rb')
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
            print(elem_num)

    pickle.dump(release_dict,open('obj/release_dict.pkl','wb'),pickle.HIGHEST_PROTOCOL)



def parseArtist():
    gzip_file = gzip.open('./data/discogs_20180801_artists.xml.gz','rb')
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
    release_dict = pickle.load(open('obj/release_dict.pkl','rb'))
    gzip_file = gzip.open(fileName,'rb')
    cur_writer = csv.writer(open('./data/csv/release.csv','w'),delimiter=',')
    elem_num = 0
    cur_elem_num = 0
    commit_counter = 0
    nodes_tuples = []

    for event, elem in ET.iterparse(gzip_file,events=['end'],tag='release'):
        release_id = elem.get('id')
        if (release_id is not None and release_id in release_dict):
            parseReleaseElemAlt(elem,nodes_tuples,release_dict)
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


def countReleases():
    gzip_file = gzip.open('./data/discogs_20180701_releases.xml.gz','rb')
    cur_writer = csv.writer(open('./data/csv/release.csv','w'),delimiter=',')
    tree = ET.parse(gzip_file)
    num_elems = tree.xpath("count(//release)")

master_path = ET.XPath('child::master_id')
artist_id_path = ET.XPath('artists/artist/id')
extra_artists_path = ET.XPath('child::extraartists/artist')
            

def parseReleaseElem(elem,batch):
    master_id = master_path(elem)[0].text
    main_artist_id = artist_id_path(elem)[0].text
    for extra in extra_artists_path(elem):
        extra_id = extra.find('id').text
        if (extra.find('role').text == "Featuring" and extra_id != main_artist_id):    
            batch.append((main_artist_id,master_id,extra_id))

    return

def parseReleaseElemAlt(elem,batch,release_dict):
    master_id = release_dict[elem.get('id')]
    main_artist_id = elem.find('artists/artist/id').text
    for extra in elem.findall('.//extraartists/artist'):
        extra_id = extra.find('id').text
        if (extra.find('role').text == "Featuring" and extra_id != main_artist_id):    
            batch.append((main_artist_id,master_id,extra_id))
    return




def printFile(name):
    gzip_file = gzip.open(name,'r')
    for line in gzip_file:
        print(line)

#buildMasterDict()
parseReleases("./data/discogs_20180701_releases.xml.gz")
