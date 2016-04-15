# Music Ratings Project

Basic, sloppy code to mine some metadata about musical artists to compare with user-generated ratings. Get that .tsv data file in your Data/ dir and we'll go from there.
Should use virtualenv for dependencies (I'm probably doing this wrong...should be a way to include all local dependencies):

virtualenv .
source ./bin/activate
./bin/pip2.7 install sparqlwrapper
./bin/pip2.7 install musicbrainzngs
./bin/pip2.7 install numpy
