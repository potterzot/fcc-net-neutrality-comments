"""
Process the xml file and store it in an HDF5 database.
"""




#MODULES
import pandas as pd
from pandas.io import pytables as pt
import tables as t
import xmltodict
import datetime
import sys

#GLOBALS
FILE_BASE = "/run/media/potterzot/My Passport/potterzot/data/fcc/"
FILEOUT = FILE_BASE+"nn_comments.h5"
FILES = [
    "14-28-RAW-Solr-1.xml"
    , "14-28-RAW-Solr-2.xml"
    , "14-28-RAW-Solr-3a.xml"
    , "14-28-RAW-Solr-3b.xml"
    ,  "14-28-RAW-Solr-4.xml"
    , "14-28-RAW-Solr-5.xml"
    ]
EPOCH = datetime.datetime.strptime('1/1/70', "%m/%d/%y") 



class Comment(t.IsDescription):
    """A comment object / row in the hdf5 data table."""
    score               = t.Float32Col() # comment score
    applicant           = t.StringCol(100) # applicant name
    applicant_sort      = t.StringCol(100) # applicant sort number
    author              = t.StringCol(100) # author name
    author_sort         = t.StringCol(100) # author sort number
    brief               = t.BoolCol()  # is the comment brief?
    city                = t.StringCol(50) # city name
    daNumber            = t.StringCol(20) # fcc number
    dateCommentPeriod   = t.Time64Col() # comment period date
    dateRcpt            = t.Time64Col() # date recieved
    disseminated        = t.Time64Col() # date disseminated to public
    exParte             = t.BoolCol() # whether an ex parte filing or not
    fileNumber          = t.StringCol(100) # file number
    id                  = t.Int32Col() # id number of filing
    lawfirm             = t.StringCol(200) # law firm name
    lawfirm_sort        = t.StringCol(200) # law firm sort order
    modified            = t.Time64Col() # date modified
    pages               = t.Int32Col() # number of pages
    proceeding          = t.StringCol(1000) # proceeding name 
    reportNumber        = t.StringCol(50) # proceeding name 
    regFlexAnalysis     = t.StringCol(1) # not used
    smallBusinessImpact = t.BoolCol() # small business impact indicator
    stateCd             = t.BoolCol() # State code
    submissionType      = t.StringCol(20) # Type of filing
    text                = t.StringCol(20000) # Comment text
    viewingStatus       = t.StringCol(15) # Confidential, Sunshine, Correspondence, Unrestricted
    zip                 = t.Int32Col() # zip code

def date_to_int(date):
    """Takes a date string and returns an int."""
    try:
        d = date[0:date.find('.')]
        d = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S")
    except:
        print(date)
        pass
    
    return (d-EPOCH).total_seconds()

def get_keyvalue(xml):
    """Takes an xml string and returns a key and value pair."""
    d = xmltodict.parse(xml)
    if d.keys().__contains__('arr'):
        d2 = d['arr']
    elif d.keys().__contains__('float'):
        d2 = d['float']

    try:
        name = d2['@name']
        vtype = get_type(name)
        if(vtype == 'date'):
            value = date_to_int(d2[vtype])
        elif(vtype=='bool'):
            if d2[vtype]=='true':
                value = True
            else:
                value = False
        elif vtype=='str':
            value = d2[vtype].encode('UTF-8')
        else:
            value = d2[vtype]
        keyvalue = {'key': name, 'value': value}
    except:
        keyvalue = False
        
    return keyvalue
    

def get_type(k):
    """Takes a dict. Returns undefined if not keyed, otherwise returns the key type."""
    
    try:
        v = {
            'score': '#text',
            'applicant': 'str',
            'applicant_sort': 'str',
            'author': 'str',
            'author_sort': 'str',
            'brief': 'bool',
            'city': 'str',
            'daNumber': 'str',
            'dateCommentPeriod': 'date',
            'dateReplyComment': 'date',
            'dateRcpt': 'date',
            'disseminated': 'date',
            'exParte': 'bool',
            'fileNumber': 'str',
            'id': 'long',
            'lawfirm': 'str',
            'lawfirm_sort': 'str',
            'modified': 'date',
            'pages': 'int',
            'proceeding': 'str',
            'reportNumber': 'str',
            'regFlexAnalysis': 'bool',
            'smallBusinessImpact': 'bool',
            'stateCd': 'str',
            'submissionType': 'str',
            'text': 'str',
            'viewingStatus': 'str',
            'zip': 'str'
        }[k]
        
    except:
        v = False
    
    return v

def set_row_value(row, xml):
    """xml string parsed and set to comment values."""
    try:
        keyvalue = get_keyvalue(xml)
        row[keyvalue['key']] = keyvalue['value']
    except:
        print("FAIL: " + str(xml))
        pass

def process(filein, store):
    """
    Take xml file and iterate through it, writing each record to an h5 table.
    table should be an h5 table
    """
    with open(filein, 'r') as fi:
        for line in fi:
            if len(line.strip()) > 0:
                if line.strip() == '<doc>': # start record
                    row = store.row
                elif line.strip() == '</doc>': # end record
                    row.append()
                elif (line.strip()[0:4] in ['<flo', '<arr']):
                    xml = line.strip()
                    if line.strip().find('text') == -1: # not a text field
                        set_row_value(row, xml)
                elif (line.strip()[0] != '<'):
                    xml += " "+line.strip()
                elif line.strip() == "</str></arr>":
                    xml += line.strip()
                    set_row_value(row, xml)
        store.flush()

def main():
    """open the gzipped xml, process data, save as records in a pytables hdf5 table, then gzip it."""

    
    # Open the HDF5 table and set it up
    h5file = t.open_file(FILEOUT, mode = "w", title = "FCC Net Neutrality Comments")
    group = h5file.create_group("/", 'nn_comments', 'Comment Data')

    table = h5file.create_table(group, 'comments', Comment, 'Comment Data')
    #store = pt.HDFStore(FILEOUT)

    # Convert to database
    for f in FILES:
        process(FILE_BASE+f, table)
    
    # Close the HDF5 file
    h5file.close()

if __name__ == '__main__':
    main()




