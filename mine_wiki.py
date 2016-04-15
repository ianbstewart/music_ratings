"""
Using artist name, mine
Wikipedia (via DBPedia) for advanced 
metadata like artist genre.
science has gone too far
"""
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import time

def query(artist_name, sparql):
    """
    Query DBPedia for artist 
    infobox information.
    We have to do this one at a time
    b/c there's no way to isolate 
    musical artists by database attribute.

    params:
    artist_name = str
    sparql = SPARQLWrapper.SPARQLWrapper
    """
    sparql.setQuery("""
                    PREFIX dbpo:<http://dbpedia.org/property/>
                    SELECT ?genre ?label
                    WHERE {
                    <http://dbpedia.org/resource/%s> dbo:genre ?genre .
                    <http://dbpedia.org/resource/%s> dbo:recordLabel ?label .
                    }
                    """%
                    ((artist_name,)*2))
    results = sparql.query()
    results = results._convertJSON()
    #print('raw results %s'%(results))
    results = results['results']['bindings']
    #print('bindings %s'%(results))
    genre = 'unk'
    label = 'unk'
    if(len(results) > 0):
        results = results[0]
        genre = results['genre']
        if(len(genre) > 0):
            genre = genre['value'].split('/')[-1]
        label = results['label']
        if(len(label) > 0):
            label = label['value']
    info = {
        'genre' : genre,
        'label' : label,
        }
    return info

QUERY_DELAY = 1.0
if __name__ == '__main__':
    # now load data
    data_file_name = 'Data/artist_metadata.tsv'
    # and simultaneously write to file ;_;
    out_file_name = 'Data/artist_wiki_metadata.tsv'
    # we can join metadata files later -_-
    out_data_names = ['artist_name',
                      'genre', 'label']
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    with open(out_file_name, 'wb') as out_file:
        writer = csv.DictWriter(out_file,
                                fieldnames=out_data_names,
                                delimiter='\t')
        writer.writeheader()
        with open(data_file_name, 'r') as data_file:
            reader = csv.DictReader(data_file,
                                    delimiter='\t')
            ctr = 0
            start_ctr = -1
            for r in reader:
                if(ctr > start_ctr):
                    artist_name = r['name']
                    # capitalize and replace space w/ underscore...and remove quotes
                    artist_name = '_'.join(list(map(str.title, artist_name.split(' '))))
                    artist_name = artist_name.replace('"', '')
                    #print('bout to query artist %s'%
                    #      (artist_name))
                    query_ctr = 0
                    query_thresh = 1
                    info = {}
                    while(query_ctr < query_thresh):
                        try:
                            info = query(artist_name, sparql)
                            query_ctr = query_thresh
                        # if we can't query, 
                        # sleep and try again
                        except Exception as e:
                            #print(('could not query artist %s b/c error %s')%
                            #      (artist_name, e))
                            query_ctr += 1
                            # if name error, reset and retry
                            if(',' in artist_name):
                                artist_name = artist_name.replace(',','')
                                query_ctr = 0
                            # 404 error => STAHP
                            if('404' in str(e)):
                                query_ctr = query_thresh
                    genre = info.get('genre')
                    label = info.get('label')
                    # now write to file ;_;
                    artist_data = {
                        'artist_name' : artist_name,
                        'genre' : genre,
                        'label' : label,
                        }
                    writer.writerow(artist_data)
                ctr += 1
                if(ctr % 100 == 0):
                    print('%d artists processed'%
                          (ctr))
