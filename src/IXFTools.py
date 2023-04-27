#!/usr/bin/python3
"""

    Copyright 2023 IBM

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
   
  @license: APACHE-2 https://opensource.org/licenses/Apache-2.0 
  @author: Romeo Lupascu <romeol@ca.ibm.com>
  @copyright: 2023 IBM
  @since: Apr 25, 2023
  @summary: A python3 library and tool for processing IBM DB2 IXF format files
  @see: https://www.ibm.com/docs/en/db2/11.1?topic=format-pcixf-record-types
  
  Program parameters:
  
  @param cmd: Optional: values csv,info,trace,json default info
  @param input: Optional: A path to an IXF file or a folder default STDIN 
  @param output: Optional: A path to the output file default STDOUT
  
  Not implemented yet:
  1. LOBs are not handled, you get in the csv what is in the IXF field 
  2. DECFLOAT (packed decimal)
  
  The file structure info as present in the IBM DB2 public documentation 
  
   HEADER RECORD
 
   FIELD NAME     LENGTH    TYPE        COMMENTS
   ----------     -------   ---------   -------------
   IXFHRECL       06-BYTE   CHARACTER   record length
   IXFHRECT       01-BYTE   CHARACTER   record type = 'H'
   IXFHID         03-BYTE   CHARACTER   IXF identifier
   IXFHVERS       04-BYTE   CHARACTER   IXF version
   IXFHPROD       12-BYTE   CHARACTER   product
   IXFHDATE       08-BYTE   CHARACTER   date written
   IXFHTIME       06-BYTE   CHARACTER   time written
   IXFHHCNT       05-BYTE   CHARACTER   heading record count
   IXFHSBCP       05-BYTE   CHARACTER   single byte code page
   IXFHDBCP       05-BYTE   CHARACTER   double byte code page
   IXFHFIL1       02-BYTE   CHARACTER   reserved

TABLE RECORD
 
   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     -------    ---------   -------------

   IXFTRECL       006-BYTE   CHARACTER   record length
   IXFTRECT       001-BYTE   CHARACTER   record type = 'T'
   IXFTNAML       003-BYTE   CHARACTER   name length
   IXFTNAME       256-BYTE   CHARACTER   name of data
   IXFTQULL       003-BYTE   CHARACTER   qualifier length
   IXFTQUAL       256-BYTE   CHARACTER   qualifier
   IXFTSRC        012-BYTE   CHARACTER   data source
   IXFTDATA       001-BYTE   CHARACTER   data convention = 'C'
   IXFTFORM       001-BYTE   CHARACTER   data format = 'M'
   IXFTMFRM       005-BYTE   CHARACTER   machine format = 'PC'
   IXFTLOC        001-BYTE   CHARACTER   data location = 'I'
   IXFTCCNT       005-BYTE   CHARACTER   'C' record count
   IXFTFIL1       002-BYTE   CHARACTER   reserved
   IXFTDESC       030-BYTE   CHARACTER   data description
   IXFTPKNM       257-BYTE   CHARACTER   primary key name
   IXFTDSPC       257-BYTE   CHARACTER   reserved
   IXFTISPC       257-BYTE   CHARACTER   reserved
   IXFTLSPC       257-BYTE   CHARACTER   reserved

COLUMN DESCRIPTOR RECORD
 
   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     -------    ---------   -------------
   IXFCRECL       006-BYTE   CHARACTER   record length
   IXFCRECT       001-BYTE   CHARACTER   record type = 'C'
   IXFCNAML       003-BYTE   CHARACTER   column name length
   IXFCNAME       256-BYTE   CHARACTER   column name
   IXFCNULL       001-BYTE   CHARACTER   column allows nulls
   IXFCDEF        001-BYTE   CHARACTER   column has defaults
   IXFCSLCT       001-BYTE   CHARACTER   column selected flag
   IXFCKPOS       002-BYTE   CHARACTER   position in primary key
   IXFCCLAS       001-BYTE   CHARACTER   data class
   IXFCTYPE       003-BYTE   CHARACTER   data type
   IXFCSBCP       005-BYTE   CHARACTER   single byte code page
   IXFCDBCP       005-BYTE   CHARACTER   double byte code page
   IXFCLENG       005-BYTE   CHARACTER   column data length
   IXFCDRID       003-BYTE   CHARACTER   'D' record identifier
   IXFCPOSN       006-BYTE   CHARACTER   column position
   IXFCDESC       030-BYTE   CHARACTER   column description
   IXFCLOBL       020-BYTE   CHARACTER   lob column length
   IXFCUDTL       003-BYTE   CHARACTER   UDT name length
   IXFCUDTN       256-BYTE   CHARACTER   UDT name
   IXFCDEFL       003-BYTE   CHARACTER   default value length
   IXFCDEFV       254-BYTE   CHARACTER   default value
   IXFCREF        001-BYTE   CHARACTER   reference type
   IXFCNDIM       002-BYTE   CHARACTER   number of dimensions
   IXFCDSIZ       varying    CHARACTER   size of each dimension

DATA RECORD
 
   FIELD NAME     LENGTH    TYPE        COMMENTS
   ----------     -------   ---------   -------------
   IXFDRECL       06-BYTE   CHARACTER   record length
   IXFDRECT       01-BYTE   CHARACTER   record type = 'D'
   IXFDRID        03-BYTE   CHARACTER   'D' record identifier
   IXFDFIL1       04-BYTE   CHARACTER   reserved
   IXFDCOLS       varying   variable    columnar data
 
 --- ALL application records are ignored by this version of the script! ---
 
APPLICATION RECORD
 
   FIELD NAME     LENGTH    TYPE        COMMENTS
   ----------     -------   ---------   -------------
   IXFARECL       06-BYTE   CHARACTER   record length
   IXFARECT       01-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       12-BYTE   CHARACTER   application identifier
   IXFADATA       varying   variable    application-specific data

DB2 INDEX RECORD

   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     --------   ---------   -------------
   IXFARECL       006-BYTE   CHARACTER   record length
   IXFARECT       001-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       012-BYTE   CHARACTER   application identifier = 'DB2 02.00'
   IXFAITYP       001-BYTE   CHARACTER   application specific data type = 'I'
   IXFADATE       008-BYTE   CHARACTER   date written from the 'H' record
   IXFATIME       006-BYTE   CHARACTER   time written from the 'H' record
   IXFANDXL       002-BYTE   SHORT INT   length of name of the index
   IXFANDXN       256-BYTE   CHARACTER   name of the index
   IXFANCL        002-BYTE   SHORT INT   length of name of the index creator
   IXFANCN        256-BYTE   CHARACTER   name of the index creator
   IXFATABL       002-BYTE   SHORT INT   length of name of the table
   IXFATABN       256-BYTE   CHARACTER   name of the table
   IXFATCL        002-BYTE   SHORT INT   length of name of the table creator
   IXFATCN        256-BYTE   CHARACTER   name of the table creator
   IXFAUNIQ       001-BYTE   CHARACTER   unique rule
   IXFACCNT       002-BYTE   SHORT INT   column count
   IXFAREVS       001-BYTE   CHARACTER   allow reverse scan flag
   IXFAIDXT       001-BYTE   CHARACTER   type of index
   IXFAPCTF       002-BYTE   CHARACTER   amount of pct free
   IXFAPCTU       002-BYTE   CHARACTER   amount of minpctused
   IXFAEXTI       001-BYTE   CHARACTER   reserved
   IXFACNML       006-BYTE   SHORT INT   length of name of the columns
   IXFACOLN       varying    CHARACTER   name of the columns in the index
    
DB2 HIERARCHY RECORD

   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     --------   ---------   -------------
   IXFARECL       006-BYTE   CHARACTER   record length
   IXFARECT       001-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       012-BYTE   CHARACTER   application identifier = 'DB2 02.00'
   IXFAXTYP       001-BYTE   CHARACTER   application specific data type = 'X'
   IXFADATE       008-BYTE   CHARACTER   date written from the 'H' record
   IXFATIME       006-BYTE   CHARACTER   time written from the 'H' record
   IXFAYCNT       010-BYTE   CHARACTER   'Y' record count for this hierarchy
   IXFAYSTR       010-BYTE   CHARACTER   starting column of this hierarchy
   
   
DB2 SUBTABLE RECORD

   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     --------   ---------   -------------
   IXFARECL       006-BYTE   CHARACTER   record length
   IXFARECT       001-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       012-BYTE   CHARACTER   application identifier = 'DB2 02.00'
   IXFAYTYP       001-BYTE   CHARACTER   application specific data type = 'Y' 
   IXFADATE       008-BYTE   CHARACTER   date written from the 'H' record
   IXFATIME       006-BYTE   CHARACTER   time written from the 'H' record
   IXFASCHL       003-BYTE   CHARACTER   type schema name length
   IXFASCHN       256-BYTE   CHARACTER   type schema name
   IXFATYPL       003-BYTE   CHARACTER   type name length
   IXFATYPN       256-BYTE   CHARACTER   type name
   IXFATABL       003-BYTE   CHARACTER   table name length
   IXFATABN       256-BYTE   CHARACTER   table name
   IXFAPNDX       010-BYTE   CHARACTER   subtable index of parent table
   IXFASNDX       005-BYTE   CHARACTER   starting column index of current table
                                           
   IXFAENDX       005-BYTE   CHARACTER   ending column index of current table

DB2 CONTINUATION RECORD

   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     --------   ---------   -------------
   IXFARECL       006-BYTE   CHARACTER   record length
   IXFARECT       001-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       012-BYTE   CHARACTER   application identifier = 'DB2 02.00'
   IXFACTYP       001-BYTE   CHARACTER   application specific data type = 'C'
   IXFADATE       008-BYTE   CHARACTER   date written from the 'H' record
   IXFATIME       006-BYTE   CHARACTER   time written from the 'H' record
   IXFALAST       002-BYTE   SHORT INT   last diskette volume number
   IXFATHIS       002-BYTE   SHORT INT   this diskette volume number
   IXFANEXT       002-BYTE   SHORT INT   next diskette volume number

DB2 TERMINATE RECORD

   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     --------   ---------   -------------
   IXFARECL       006-BYTE   CHARACTER   record length
   IXFARECT       001-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       012-BYTE   CHARACTER   application identifier = 'DB2 02.00'
   IXFAETYP       001-BYTE   CHARACTER   application specific data type = 'E' 
   IXFADATE       008-BYTE   CHARACTER   date written from the 'H' record
   IXFATIME       006-BYTE   CHARACTER   time written from the 'H' record

DB2 IDENTITY RECORD
  
   FIELD NAME     LENGTH    TYPE        COMMENTS
   ----------     -------   ---------   -------------
   IXFARECL       06-BYTE   CHARACTER   record length
   IXFARECT       01-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       12-BYTE   CHARACTER   application identifier
   IXFATYPE       01-BYTE   CHARACTER   application specific record type = 'S'
   IXFADATE       08-BYTE   CHARACTER   application record creation date
   IXFATIME       06-BYTE   CHARACTER   application record creation time
   IXFACOLN       06-BYTE   CHARACTER   column number of the identity column
   IXFAITYP       01-BYTE   CHARACTER   generated always ('Y' or 'N')
   IXFASTRT       33-BYTE   CHARACTER   identity START AT value
   IXFAINCR       33-BYTE   CHARACTER   identity INCREMENT BY value
   IXFACACH       10-BYTE   CHARACTER   identity CACHE value
   IXFAMINV       33-BYTE   CHARACTER   identity MINVALUE
   IXFAMAXV       33-BYTE   CHARACTER   identity MAXVALUE
   IXFACYCL       01-BYTE   CHARACTER   identity CYCLE ('Y' or 'N')
   IXFAORDR       01-BYTE   CHARACTER   identity ORDER ('Y' or 'N')
   IXFARMRL       03-BYTE   CHARACTER   identity Remark length
   IXFARMRK      254-BYTE   CHARACTER   identity Remark value

DB2 SQLCA RECORD

   FIELD NAME     LENGTH    TYPE        COMMENTS
   ----------     -------   ---------   -------------
   IXFARECL       006-BYTE  CHARACTER   record length
   IXFARECT       001-BYTE  CHARACTER   record type = 'A'
   IXFAPPID       012-BYTE  CHARACTER   application identifier = 'DB2 02.00'
   IXFAITYP       001-BYTE  CHARACTER   application specific data type = 'A'
   IXFADATE       008-BYTE  CHARACTER   date written from the 'H' record
   IXFATIME       006-BYTE  CHARACTER   time written from the 'H' record
   IXFASLCA       136-BYTE  variable    sqlca - SQL communications area



"""
import os,sys,json,csv,struct,time

class IXFParser:
    """
    A reusable component used by the main method to implement the tool's logic. 
    You can reuse this in your own programs.
    """
    recordTypes={
        'H':[
           ['IXFHID',3,'IXF identifier'],
           ['IXFHVERS',4,'IXF version'],
           ['IXFHPROD',12,'product'],
           ['IXFHDATE',8,'date written'],
           ['IXFHTIME',6,'time written'],
           ['IXFHHCNT',5,'heading record count'],
           ['IXFHSBCP',5,'single byte code page'],
           ['IXFHDBCP',5,'double byte code page'],
           ['IXFHFIL1',2,'reserved']
        ],
        'T':[
           ['IXFTNAML',  3,'name length'],
           ['IXFTNAME',256,'name'],
           ['IXFTQULL',  3,'qualifier length'],
           ['IXFTQUAL',256,'qualifier'],
           ['IXFTSRC',  12,'data source'],
           ['IXFTDATA',  1,"data convention = 'C'"],
           ['IXFTFORM',  1,"data format = M'"],
           ['IXFTMFRM',  5,"machine format = 'PC'"],
           ['IXFTLOC' ,  1,"data location = 'I'"],
           ['IXFTCCNT',  5,"'C' record count"],
           ['IXFTFIL1',  2,'reserved'],
           ['IXFTDESC', 30,'data description'],
           ['IXFTPKNM',257,'primary key name'],
           ['IXFTDSPC',257,'reserved'],
           ['IXFTISPC',257,'reserved'],
           ['IXFTLSPC',257,'reserved']
        ],
        'C': [
           ['IXFCNAML',  3,'column name length'], # 0
           ['IXFCNAME',256,'column name'], # 1
           ['IXFCNULL',  1,'column allows nulls'], # 2
           ['IXFCDEF',   1,'column has defaults'], # 3
           ['IXFCSLCT',  1,'column selected flag'], # 4
           ['IXFCKPOS',  2,'position in primary key'], # 5
           ['IXFCCLAS',  1,'data class'], # 6
           ['IXFCTYPE',  3,'data type'], # 7
           ['IXFCSBCP',  5,'single byte code page'], # 8
           ['IXFCDBCP',  5,'double byte code page'], # 9
           ['IXFCLENG',  5,'column data length'], # 10
           ['IXFCDRID',  3,"'D' record identifier"], # 11
           ['IXFCPOSN',  6,'column position'], # 12
           ['IXFCDESC', 30,'column description'], # 13
           ['IXFCLOBL', 20,'lob column length'], # 14
           ['IXFCUDTL',  3,'UDT name length'], # 15
           ['IXFCUDTN',256,'UDT name'], # 16
           ['IXFCDEFL',  3,'default value length'], # 17
           ['IXFCDEFV',254,'default value'], # 18
           ['IXFCREF',   1,'reference type'], # 19
           ['IXFCNDIM',  2,'number of dimensions'], # 20
           ['IXFCDSIZ',  0,'size of each dimension'] # 21
        ],
        'D':[
           ['IXFDRID' ,3,"'D' record identifier"],
           ['IXFDFIL1',4,'reserved'],
           ['IXFDCOLS',0,'columnar data'],
        ],
        'A':[
           ['IXFAPPID',12,'application identifier'],
           ['IXFADATA', 0,'application-specific data'],
        ],
    }
    
    # encoding the type storage length
    # >0 fixed size known by the type
    # 0 variable length the length is the first 2 bytes in ther data
    # -1 fixed length the column data_len is the storage length
    # -2 computed value from the column and type info 
    # -4 lob/clob
    typeInfo={
        '492':{'name':'BIGINT','length':8,'parser':'parseBigInteger'},
        '912':{'name':'BINARY','length':-1,'parser':'parseRaw'},
        '404':{'name':'BLOB','length':-4,'parser':'parseLob'},
        '408':{'name':'CLOB','length':-4,'parser':'parseLob'},
        '960':{'name':'BLOB_LOCATION_ SPECIFIER ','length':-1,'parser':'parseLob'},
        '964':{'name':'BLOB_LOCATION_ SPECIFIER ','length':-1,'parser':'parseLob'},
        '968':{'name':'DBCLOB_ LOCATION_ SPECIFIER','length':-1,'parser':'parseLob'},
        '916':{'name':'BLOB_FILE','length':-1,'parser':'parseLob'},
        '920':{'name':'CLOB_FILE','length':-1,'parser':'parseLob'},
        '924':{'name':'DBCLOB_FILE','length':-1,'parser':'parseLob'},
        '452':{'name':'CHAR','length':-1,'parser':'parseChars'},
        '384':{'name':'DATE','length':10,'parser':'parseChars'},
        '412':{'name':'DBCLOB','length':0,'parser':'parseLob'},
        '484':{'name':'DECIMAL','length':-2,'parser':'parseNum'},
        '996':{'name':'DECFLOAT','length':-2,'parser':'parseNum'},
        '480':{'name':'FLOATING POINT','length':-2,'parser':'parseFloat'},
        '468':{'name':'GRAPHIC','length':-1,'parser':'parseVarLen'},
        '496':{'name':'INTEGER','length':4,'parser':'parseInteger'},
        '456':{'name':'LONGVARCHAR','length':0,'parser':'parseNum'},
        '472':{'name':'LONG VARGRAPHIC','length':0,'parser':'parseVarLen'},
        '500':{'name':'SMALLINT','length':2,'parser':'parseSmallInt'},
        '388':{'name':'TIME','length':8,'parser':'parseChars'},
        '392':{'name':'TIMESTAMP','length':-2,'parser':'parseChars'},
        '908':{'name':'VARBINARY','length':0,'parser':'parseVarLen'},
        '448':{'name':'VARCHAR','length':0,'parser':'parseVarLen'},
        '464':{'name':'VARGRAPHIC','length':0,'parser':'parseVarLen'},
    }
    
    def __init__(self,**args):
        self.endianism='<'
        self.tableDefProcessed=False
        self.tableDef={
            'name':None,
            'schema':None,
            'columns':[],
        }
        self.columns=[]
        self.currentRow=None
        self.columnCount=0
        self.rowCount=0
        self.convertTo=args.get('outfmt',None)
        self.traceRecords=args.get('trace',False)
        self.output=None
        self.csvwriter=None
        
        for k in self.typeInfo:
            td=self.typeInfo[k]
            pn=td['parser']
            pm=getattr(self, pn)
            if pm:
                td['parser']=pm
            else:
                pm=self.parseRaw
            
    def getColset(self,cid):
        return self.colcidmap.get(cid)
    
    def onTableDef(self):
        """
        Optional processing when the table definition is fully built.
        At this point a SQL statement can be created or the column list 
        written to a csv file 
        """
        self.tableDef['columns']=self.columns
        self.colcidmap={}
        for cd in self.columns:
            if self.traceRecords:
                print(repr(cd),file=sys.stderr)
                
            cid=cd['cid']
            cim=self.colcidmap.get(cid)
            if cim is None:
                cim=[cd]
                self.colcidmap[cid]=cim
            else:
                cim.append(cd)
            
        if self.convertTo:
            if self.csvwriter:
                colnames=[]
                coltypes=[]
                for cd in self.columns:
                    colnames.append(cd['name'])
                    coltypes.append(self.typeInfo[cd['type']]['name']) # TODO: finish impl
                    
                self.csvwriter.writerow(colnames)
                self.csvwriter.writerow(coltypes)
                
    def onRowReceived(self):
        """
        Process a data row if an output was defined
        """
        if self.traceRecords:
            print(repr(self.currentRow),file=sys.stderr)
        
        if self.output is None:
            return
        
        if self.csvwriter:          
            self.csvwriter.writerow([repr(x) if type(x) == bytes else x for x in self.currentRow])
        
    def onLastRecord(self):
        """
        Do the cleanup for a file conversion.
        """
        if self.currentRow:
            self.onRowReceived()
            self.rowCount+=1
        if self.output:
            self.output.flush()
            if self.output!=sys.stdout:
                self.output.close()
            
    def parseNum(self,coldef,data):
        # TODO: implement
        return self.parseRaw(coldef,data)

    def parseFloat(self,coldef,data):
        if len(data) == 4:
            return struct.unpack(self.endianism+'f',data)[0]
        return struct.unpack(self.endianism+'d',data)[0]

    def parseSmallInt(self,coldef,data):
        return struct.unpack(self.endianism+'h',data)[0]
    
    def parseInteger(self,coldef,data):
        return struct.unpack(self.endianism+'i',data)[0]

    def parseBigInteger(self,coldef,data):
        return struct.unpack(self.endianism+'q',data)[0]

    def parseVarLen(self,coldef,data):
        encoding=self.getColumnEncoding(coldef)      
        try:
            return data.decode(encoding)
        except Exception as x:
            print("parseVarLen:error:",x,file=sys.stderr)
            return data
        
    def parseLob(self,coldef,data):
        # TODO: implement
        if coldef['type'] in ('960', '964', '968'):
            # is a LOB locator
            pass
        if coldef['type'] in ('916', '920', '924'):
            # is a LOB file
            pass
        
        if coldef['type'] == '408':
            encoding=self.getColumnEncoding(coldef)      
            # is a CLOB file or locator
            return data.decode(encoding)
        
        return self.parseRaw(coldef,data)

    def parseChars(self,coldef,data):
        try:
            return data.decode()
        except Exception as x:
            print("parseChars:error:",x,file=sys.stderr)
            return data
        
    def parseRaw(self,coldef,data):
        return data
        
    def getColumnEncoding(self,coldef):
        """
        """
        return 'utf-8'
    
    def getFieldActualLengthAndData(self,coldef,coltdef,pos,data):
        """
        DECIMAL -> 484 -> -2 use the method to get the length
        precision P (as specified by the first three bytes of IXFCLENG in the column descriptor record) and 
        scale S (as specified by the last two bytes of IXFCLENG). 
        The length, in bytes, of a packed decimal number is (P+2)/2
        
        DECFLOAT:The storage length of the 16 digit value is 8 bytes, 
          and the storage length of the 34 digit value is 16 bytes.
        
        TIMESTAMP ->
        """
        tdlen=coltdef['length']
        # fixed length known in type
        if tdlen>0:
            if coltdef['name'] in ('CHAR','DATE','TIME') and data[pos] == 0xff:
                return (-1,None)
            return (tdlen,data[pos:pos+tdlen])
        
        # fixed length defined in the column definition
        if tdlen==-1:
            if data[pos] == 0xff:
                return (-1,None)
            ln=coldef['data_len']
            return (ln,data[pos:pos+ln])
        
        # lob var length defined in the column definition
        if tdlen==-4:
            blen=data[pos:pos+4]
            ln=struct.unpack(self.endianism+'I',blen)[0]
            data=data[pos+4:pos+4+ln]
            return (ln,data)
        
        # variable length length embedded in data (2 bytes)
        if tdlen==0:
            blen=data[pos:pos+2]
            ln=struct.unpack(self.endianism+'H',blen)[0]
            data=data[pos+2:pos+2+ln]
            return (ln,data)
        
        # special cases
        if coltdef['name'] =='FLOATING POINT':
            ln=coldef['data_len']
            return (ln,data[pos:pos+ln])
        
        if coltdef['name'] =='DECIMAL':
            plen=coldef['data_len']>>16
            return ((plen+2)/2,data[pos:pos+plen])
        
        if coltdef['name'] == 'DECFLOAT':
            ln=(8 if coldef['data_len']==16 else 16)
            return (ln,data[pos:pos+ln])
        
        if coltdef['name'] == 'TIMESTAMP':
            if data[pos] == 0xff:
                return (-1,None)
            ln=20+coldef['data_len']
            return (ln,data[pos:pos+ln])
        
    def parseColumnsForField(self,cid,data):
        colset=self.getColset(cid)
        if colset is None:
            return None
        
        for cd in colset:
            td=self.typeInfo[cd['type']]
            pos=cd['pos']-1
            len,cbdt = self.getFieldActualLengthAndData(cd,td,pos,data)
            if len<0:
                return None
            
            cv=td['parser'](cd,cbdt)
            self.currentRow[cd['colno']]=cv

    def parseInt(self,bstr,dv=0):
        try:
            return int(bstr.decode())
        except:
            return dv
    
    def processIFXRecords(self,feed,output=None):
        """
    An IXF File is a collection of records that start with this header:
    
       FIELD NAME     LENGTH    TYPE        COMMENTS
       ----------     -------   ---------   -------------
       IXFHRECL       06-BYTE   CHARACTER   record length
       IXFHRECT       01-BYTE   CHARACTER   record type = 'H'
       
    Read the header and get the length and type of the record then
    parse the data based on the record type.
        """
        self.output=output
        if self.convertTo=='csv' and self.output:
            self.csvwriter=csv.writer(self.output)
        else:
            self.csvwriter=None
        self.tableDef={}
        self.columns=[]
        self.columnCount=0
        self.rowCount=0
        self.currentRow=None
        
        while True:
            ln=feed.read(6)
            if not ln or len(ln)<6:
                self.onLastRecord()
                return
            rt=feed.read(1)
            if not rt:
                self.onLastRecord()
                return
            ln=self.parseInt(ln)
            rt=rt.decode()
            rdt=feed.read(ln-1)
            rdtitms=[]
            
            rst=self.recordTypes.get(rt)
            if not rst:
                continue
            
            # parse the record based on its field lengths
            off=0
            for r in rst[:-1]:
                rl=int(r[1])
                rdtitms.append(rdt[off:off+rl])
                off+=rl
            rdtitms.append(rdt[off:])
            
            if self.traceRecords:
                print(rt+":",repr(rdtitms),file=sys.stderr)
            
            if rt == 'H':
                # ignore in this version
                pass
                
            elif rt == 'T':
                name=rdtitms[1][:self.parseInt(rdtitms[0])].decode()
                if name.endswith('.ixf'):
                    name=name[:-4]
                
                self.tableDef['name']=name
                
                # TODO: add more properties 
            elif rt == 'C':
                col={
                    'colno':self.columnCount,
                    'name':(rdtitms[1][:self.parseInt(rdtitms[0])]).decode(),
                    'pkpos':rdtitms[5].decode(),
                    'type': rdtitms[7].decode(),
                    'sbcodepage':rdtitms[8].decode(),
                    'dbcodepage':rdtitms[9].decode(),
                    'data_len': self.parseInt(rdtitms[10]),
                    'cid':self.parseInt(rdtitms[11]),
                    'pos':self.parseInt(rdtitms[12],0),
                    'lob_len': self.parseInt(rdtitms[14]),
                    'nullable':rdtitms[2].decode(),
                    'hasdefault':rdtitms[3].decode(),
                }
                # TODO: add more column fields
                self.columns.append(col)
                self.columnCount+=1
                
            elif rt == 'D':
                if not self.tableDefProcessed:
                    self.onTableDef()
                    self.tableDefProcessed=True
                colno=self.parseInt(rdtitms[0])
                
                if colno==1:
                    if not self.currentRow is None:
                        self.onRowReceived()
                        self.rowCount+=1
                    self.currentRow=[None]*self.columnCount
                
                self.parseColumnsForField(colno,rdtitms[2])
                
            elif rt == 'A':
                # ignore in this version
                pass

def prcessSingleFile(ixfp,cmd,inp,outp):
    """
    Process a single ixf file given an IXF instance processor
    a command and input output file paths.
    """
    if cmd != 'info':
        if type(outp) == str:
            print("Writing to file:",outp,file=sys.stderr)
            out=open(outp,"wt")
    else:
        out=None
    
    with open(inp,"rb") as fin:
        print("Reading from:",inp,file=sys.stderr)
        start=time.time()
        ixfp.processIFXRecords(fin,out)
        stop=time.time()
        
        print("Table Name:",ixfp.tableDef['name'],file=sys.stderr)
        print("Column Count:",ixfp.columnCount,file=sys.stderr)
        print("Row    Count:",ixfp.rowCount,file=sys.stderr)
        print("Processing time(sec):",stop-start,file=sys.stderr)
   

def batchProcess(ixf,cmd,indir,outdir=None):
    """
    Process a set of files
    """
    if outdir is None:
        outdir=indir
    for fn in os.listdir(indir):
        if fn.endswith('.ixf'):
            infp=os.path.join(indir,fn)
            outfp=os.path.join(outdir,fn[:-3]+'csv')
            prcessSingleFile(ixf,cmd,infp,outfp)

def main():
    cmd='info'
    outfmt='csv'
    trace=False
    inp=None
    out=None
    
    pav=[]
    for arg in sys.argv[1:]:
        aa=arg.split('=')
        if len(aa)==1:
            pav.append(arg)
        else:
            if aa[0]=='cmd':
                cmd=aa[1]
            elif aa[0] == 'in':
                inp=aa[1]
            elif aa[0] == 'out':
                out=aa[1]
            elif aa[0] == 'trace':
                trace=aa[1]=='y'
    
    for pv in pav:
        if pv in ('info','csv','json'):
            cmd=pv
        elif pv=='trace':
            trace=True
        elif pv=='-':
            if inp is None:
                inp=sys.stdin
            elif out is None:
                out=sys.stdout
                break 
        elif os.path.exists(pv):
            if inp is None:
                inp=pv
            elif out is None:
                out=pv
                break                
        elif out is None:
            out=pv
            break
    
    if inp is None:
        inp='.'
        
    ixfp=IXFParser(outfmt=outfmt,trace=trace)
    
    if (type(inp) == str) and os.path.isdir(inp):
        batchProcess(ixfp,cmd,inp,out)
    else:
        prcessSingleFile(ixfp,cmd,inp,out)
            
if __name__ == '__main__':
    main()
