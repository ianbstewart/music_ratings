"""
Mine artist metadata by querying
music database for artist name. 
Can you say "yikes"?
"""
import csv
import musicbrainzngs as mb

def setup_creds(user_creds_file):
    """
    Set up credentials for database mining.
    
    params:
    creds_file = str
    """
    # load credentials from "secure" file
    creds = {}
    with open(user_creds_file) as user_creds_file:
        for l in user_creds_file:
            name, val = l.split('=')
            creds[name] = val
    mb.auth(creds['username'], creds['password'])
    app = 'test app'
    version = '0.1'
    mb.set_useragent(app, version)

if __name__ == '__main__':
    # set user agent??
    user_creds_file = 'musicbrainz_creds.txt'
    setup_creds(user_creds_file)
    # now load data
    data_file_name = '../Data/artist_names.tsv'
    fieldnames = ['ydata_id','artist_name']
    # and simultaneously write to file ;_;
    out_file_name = 'Data/artist_metadata.tsv'
    out_data_names = ['start', 'end', 'id', 'name', 
                      'guess_name', 'country', 'score', 'best_tag']
    with open(out_file_name, 'wb') as out_file:
        writer = csv.DictWriter(out_file,
                                fieldnames=out_data_names,
                                delimiter='\t')
        writer.writeheader()
        with open(data_file_name, 'r') as data_file:
            reader = csv.DictReader(data_file,
                                    fieldnames=fieldnames,
                                    delimiter='\t')
            # skip first two rows
            ctr = 0
            for r in reader:
                ctr += 1
                if(ctr == 2):
                    break
            # now onto the actual artists
            start_ctr = 41219
            ctr = 0
            for r in reader:
                if(ctr > start_ctr and 
                   len(r) == len(fieldnames)):
                    name = r['artist_name']
                    # collect data using MusicBrainz
                    results = mb.search_artists(artist=name,
                                               type='group')
                    results = results['artist-list']
                    #print('artist %s got results %s'%
                    #      (name, results))
                    if(len(results) > 0):
                        best_guess = results[0]
                        lifespan = best_guess['life-span']
                        start = lifespan.get('begin')
                        if(start is None):
                            start = 'unk'
                        end = lifespan.get('end')
                        if(end is None):
                            end = 'unk'
                        country = best_guess.get('country')
                        if(country is None):
                            country = 'unk'
                        # tags for genre/category
                        taglist = best_guess.get('tag-list')
                        best_tag = 'none'
                        if(taglist is not None):
                            taglist = sorted(taglist, 
                                             key=lambda x:x['count'],
                                             reverse=True)
                            taglist = [x['name'] for x 
                                       in taglist]
                            best_tag = taglist[0]
                            if(type(best_tag) is unicode):
                                best_tag = best_tag.encode('utf-8')
                        new_name = best_guess.get('name')
                        if(type(new_name) is unicode):
                            new_name = new_name.encode('utf-8')
                        if(type(name) is unicode):
                            new_name = name.encode('utf-8')
                        # now write to file ;_;
                        user_data = {
                            'start' : start,
                            'end' : end,
                            'id' : best_guess.get('id'),
                            'name' : name,
                            'guess_name' : new_name,
                            'country' : country,
                            'score' : best_guess.get('ext:score'),
                            'best_tag' : best_tag,
                            }
                        writer.writerow(user_data)
                    else:
                        print(('searching for artist %s '+
                               'yielded no results :('))
                # how to handle problem rows...
                #else:
                #    print('problem row %s'%
                #          (r))
                ctr += 1
                if(ctr % 100 == 0):
                    print('%d artists processed'%
                          (ctr))
                
