class Path():
    def __init__(self,artist_ids,path_ids):
        if len(artist_ids) < 2 or len(path_ids) < 1:
            raise ValueError('Path must requires at least two artist_id and \
            one path_id')
        if len(artist_ids) - 1 != len(path_ids):
            raise ValueError('artist_id count must be one more than path_id \
            count, to represent a linear path between nodes')




