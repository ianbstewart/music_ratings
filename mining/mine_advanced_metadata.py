"""
Using artist id, mine MusicBrainz 
for advanced metadata like
number of albums.
HAS SCIENCE GONE TOO FAR??!
"""
import csv
import musicbrainzngs as mb
from mine_metadata import setup_creds
import numpy as np
import time

QUERY_DELAY = 1.0
if __name__ == '__main__':
    # set user agent??
    user_creds_file = 'musicbrainz_creds.txt'
    setup_creds(user_creds_file)
    # now load data
    data_file_name = '../Data/artist_metadata.tsv'
    # and simultaneously write to file ;_;
    out_file_name = '../Data/artist_advanced_metadata.tsv'
    # we can join metadata files later -_-
    out_data_names = ['artist_id', 
                      'recordings', 'recording_lengths',
                      'releases', 'track_counts']
    include_list = ['recordings', 'releases']
    with open(out_file_name, 'wb') as out_file:
        writer = csv.DictWriter(out_file,
                                fieldnames=out_data_names,
                                delimiter='\t')
        writer.writeheader()
        with open(data_file_name, 'r') as data_file:
            reader = csv.DictReader(data_file,
                                    delimiter='\t')
            ctr = 0
            for r in reader:
                artist_id = r['id']
                # collect data using MusicBrainz
                query_success = False
                while(not query_success):
                    try:
                        result = mb.get_artist_by_id(artist_id,
                                                     includes=include_list)
                        query_success = True
                    # if we can't query, sleep and try again
                    except Exception, e:
                        print(('sleep for %.2f sec b/c '+
                              'rate limiting error %s')%
                              (QUERY_DELAY, e))
                        time.sleep(QUERY_DELAY)
                artist_info = result['artist'] 
                recording_count = artist_info['recording-count']
                recordings = artist_info['recording-list']
                recording_lengths = []
                if(len(recordings) > 0):
                    print('got recordings %s'%
                          (recordings))
                    recording_lengths = [r.get('length')
                                         for r in recordings
                                         if r.get('length') 
                                         is not None]
                release_count = artist_info['release-count']
                releases = artist_info['release-list']
                track_counts = []
                if(len(releases) > 0):
                    track_counts = [str(r['medium-list']
                                                [0]['track-count'])
                                            for r in releases]
                # now write to file ;_;
                artist_data = {
                    'artist_id' : artist_id,
                    'recordings' : recording_count,
                    'recording_lengths' : ','.join(recording_lengths),
                    'releases' : release_count,
                    'track_counts' : ','.join(track_counts),
                    }
                writer.writerow(artist_data)
                ctr += 1
                if(ctr % 100 == 0):
                    print('%d artists processed'%
                          (ctr))
                
