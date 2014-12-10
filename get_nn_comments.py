"""
Download and process the 400,000+ comments the FCC received on Net Neutrality.
The files are available here: http://www.fcc.gov/files/ecfs/14-28/
Also at that location are the XSD and description of fields documents
"""
#MODULES
import datetime
from urllib.request import urlopen, Request, urlretrieve

#GLOBALS
TODAY = str(datetime.date.today()).replace('-','')
URL_BASE = "http://www.fcc.gov/files/ecfs/14-28/"
FILE_BASE = "/run/media/potterzot/zfire1/data/fcc/"
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
        print("%d done..." % (100*blk_size/size) )

    if verbose: verbose=_verbose

    for f in files:
	print("Saving as %s" % f)
        urlretrieve(URL_BASE+f, FILE_BASE+f, verbose)

def main():
    """Get the xml files from the FCC."""
    
    # If the data haven't been downloaded:
    get_files(FILES, saveto=SAVE_TO, verbose=False)

if __name__ == '__main__':
    main()
