"""
Download and process the 400,000+ comments the FCC received on Net Neutrality.
The files are available here: http://www.fcc.gov/files/ecfs/14-28/
Also at that location are the XSD and description of fields documents
"""
#MODULES
import gzip
import datetime
from urllib.request import urlopen, Request, urlretrieve

#GLOBALS
TODAY = str(datetime.date.today()).replace('-','')
URL_BASE = "http://www.fcc.gov/files/ecfs/14-28/"
SAVE_TO = "/home/potterzot/nn_comments.xml.tgz"
FILES = [
    "14-28-RAW-Solr-1.xml"
    , "14-28-RAW-Solr-2.xml"
    , "14-28-RAW-Solr-3a.xml"
    , "14-28-RAW-Solr-3b.xml"
    , "14-28-RAW-Solr-4.xml"
    , "14-28-RAW-Solr-5.xml"
    ]


def get_files(files, saveto=False, verbose=False):
    """Fetch a file from the web."""
    def _verbose(blk, blk_size, size):
        """Prints download progress."""
        print("%d % done..." % (100*blk_blk_size/site) )

    if verbose: verbose=_verbose
    print("Downloading file: %s" % url)
    if saveto: print("... as %s" % saveto)

    for f in files:
        data = gzip.open(saveto, 'wb')
        fi = urlretrieve(URL_BASE+f, saveto, verbose)
        data.write(fi)
        data.close()

def process_data(filename);
    """
    """


def main():
    """Get the xml files from the FCC. Process them together"""
    
    # If the data haven't been downloaded:
    get_files(FILES, saveto=SAVE_TO, verbose=True)
     
    # Process the data to calculate various metrics 
    process_data(filename)



if __name__ == '__main__':
    main()
