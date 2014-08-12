"""
Process the xml file and store it in an HDF5 database.
"""




#MODULES
import pandas as pd
import xmltodict
import datetime
import sys
import sqlite3 as lite
from collections import OrderedDict

#GLOBALS
FILE_BASE = "/run/media/potterzot/My Passport/potterzot/data/fcc/"
DBOUT = FILE_BASE+"nn_comments.db"
FILES = [
    "14-28-RAW-Solr-1.xml"
    , "14-28-RAW-Solr-2.xml"
    , "14-28-RAW-Solr-3a.xml"
    , "14-28-RAW-Solr-3b.xml"
    ,  "14-28-RAW-Solr-4.xml"
    , "14-28-RAW-Solr-5.xml"
    ]
EPOCH = datetime.datetime.strptime('1/1/70', "%m/%d/%y") 

TABLE = "comments"
COLUMN_DICT = OrderedDict([
    ('id', 'long'),
    ('applicant', 'str'),
    ('applicant_sort', 'str'),
    ('author', 'str'),
    ('author_sort', 'str'),
    ('brief', 'bool'),
    ('city', 'str'),
    ('stateCd', 'str'),
    ('zip', 'str'),
    ('daNumber', 'str'),
    ('dateCommentPeriod', 'date'),
    ('dateReplyComment', 'date'),
    ('dateRcpt', 'date'),
    ('disseminated', 'date'),
    ('exParte', 'bool'),
    ('fileNumber', 'str'),
    ('lawfirm', 'str'),
    ('lawfirm_sort', 'str'),
    ('modified', 'date'),
    ('pages', 'int'),
    ('proceeding', 'str'),
    ('reportNumber', 'str'),
    ('regFlexAnalysis', 'bool'),
    ('smallBusinessImpact', 'bool'),
    ('submissionType', 'str'),
    ('text', 'str'),
    ('viewingStatus', 'str'),
    ('score', '#text'),
])

def date_to_int(date):
    """Takes a date string and returns an int."""
    try:
        d = date[0:date.find('.')].replace("T"," ")
        #d = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S")
    except:
        print(date)
        pass
    
    return d #(d-EPOCH).total_seconds()

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
                value = 1
            else:
                value = 0
        elif vtype in ['str', 'long']:
            value = str(d2[vtype]) #.encode('UTF-8')
        elif vtype in ['int']:
            value = int(d2[vtype])
        elif vtype=='#text':
            value = float(d2[vtype])
        else:
            value = d2[vtype]
        keyvalue = {'key': name, 'value': value}
    except:
        keyvalue = False
        
    return keyvalue
    

def get_type(k):
    """Takes a dict. Returns undefined if not keyed, otherwise returns the key type."""
    
    try:
        v = COLUMN_DICT[k]
        
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

def process(filein, cursor):
    """
    Take xml file and iterate through it, writing each record to an h5 table.
    table should be an h5 table
    """
    with open(filein, 'r') as fi:
        for line in fi:
            if len(line.strip()) > 0:
                if line.strip() == '<doc>': # start record
                    new_comment = OrderedDict()
                    for column in COLUMN_DICT.keys():
                        new_comment[column] = None
                elif line.strip() == '</doc>': # end record
                    for key in new_comment.keys():
                        if new_comment[key]==None:
                            new_comment[key] = {'#text': "",
                                'str': "", 
                                'date': "", 
                                'bool': None, 
                                'long': None, 
                                'int': 0}[COLUMN_DICT[key]]
                    
                    cursor.execute("INSERT INTO "+ TABLE + " VALUES ( \
                        ?,?,?,?,?,?,?,?,?,?, \
                        ?,?,?,?,?,?,?,?,?,?, \
                        ?,?,?,?,?,?,?,?)", list(new_comment.values())) 
                elif (line.strip()[0:4] in ['<flo', '<arr']):
                    xml = line.strip()
                    if line.strip().find('text') == -1: # not a text field
                        set_row_value(new_comment, xml)
                elif (line.strip()[0] != '<'):
                    xml += " "+line.strip()
                elif line.strip() == "</str></arr>":
                    xml += line.strip()
                    set_row_value(new_comment, xml)

def main():
    """open the gzipped xml, process data, save as records in a pytables hdf5 table, then gzip it."""
    
    # Open SQL database and create the table
    sqldb = None
    sqldb = lite.connect(DBOUT)
    
    with sqldb:
        cursor = sqldb.cursor()
    
        # Drop the old table
        cursor.execute("DROP TABLE IF EXISTS "+TABLE)
        
        # Create the new table
        cursor.execute("CREATE TABLE " + TABLE + "(\
            id                    TEXT \
            , applicant           TEXT\
            , applicant_sort      TEXT\
            , author              TEXT\
            , author_sort         TEXT\
            , brief               INT \
            , city                TEXT\
            , stateCd             TEXT\
            , zip                 TEXT \
            , daNumber            TEXT\
            , dateCommentPeriod   TEXT\
            , dateReplyComment    TEXT\
            , dateRcpt            TEXT\
            , disseminated        TEXT\
            , exParte             INT \
            , fileNumber          TEXT\
            , lawfirm             TEXT\
            , lawfirm_sort        TEXT\
            , modified            TEXT\
            , pages               INT \
            , proceeding          TEXT\
            , reportNumber        TEXT\
            , regFlexAnalysis     INT\
            , smallBusinessImpact INT \
            , submissionType      TEXT\
            , text                TEXT\
            , viewingStatus       TEXT\
            , score               REAL  \
        )")

        # Convert to database
        for f in FILES:
            process(FILE_BASE+f, cursor)
            sqldb.commit()

if __name__ == '__main__':
    main()




