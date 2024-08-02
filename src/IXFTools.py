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
  @change: fixed lob access, and test on DB2 V11.5
  @version: V0.2
  @summary: A python3 library and tool for processing IBM DB2 IXF format files
  @see: https://www.ibm.com/docs/en/db2/11.5?topic=formats-pc-version-ixf-file-format
  
  Program parameters:
  
  @param cmd: Optional: values csv,info,trace,json default info
  @param input: Optional: A path to an IXF file or a folder default STDIN 
  @param output: Optional: A path to the output file default STDOUT
  
  Not implemented yet:
  1. LOBs are not handled, you get in the csv what is in the IXF field 
  2. DECFLOAT (packed decimal)
  
  The file structure info as present in the IBM DB2 public documentation 
  
   HEADER RECORD (RT=H)
 
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

TABLE RECORD (RT=T)
 
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

COLUMN DESCRIPTOR RECORD (RT=C)
 
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

DATA RECORD (RT=D)
 
   FIELD NAME     LENGTH    TYPE        COMMENTS
   ----------     -------   ---------   -------------
   IXFDRECL       06-BYTE   CHARACTER   record length
   IXFDRECT       01-BYTE   CHARACTER   record type = 'D'
   IXFDRID        03-BYTE   CHARACTER   'D' record identifier
   IXFDFIL1       04-BYTE   CHARACTER   reserved
   IXFDCOLS       varying   variable    columnar data
 
 --- ALL application records are ignored by this version of the script! ---
 
APPLICATION RECORD (RT=A)
 
   FIELD NAME     LENGTH    TYPE        COMMENTS
   ----------     -------   ---------   -------------
   IXFARECL       06-BYTE   CHARACTER   record length
   IXFARECT       01-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       12-BYTE   CHARACTER   application identifier
   IXFADATA       varying   variable    application-specific data

DB2 INDEX RECORD (RT=A+I)

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
    
DB2 HIERARCHY RECORD (RT=A+X)

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
   
   
DB2 SUBTABLE RECORD (RT=A+Y)

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

DB2 CONTINUATION RECORD (RT=A+C)

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

DB2 TERMINATE RECORD (RT=A+E)

   FIELD NAME     LENGTH     TYPE        COMMENTS
   ----------     --------   ---------   -------------
   IXFARECL       006-BYTE   CHARACTER   record length
   IXFARECT       001-BYTE   CHARACTER   record type = 'A'
   IXFAPPID       012-BYTE   CHARACTER   application identifier = 'DB2 02.00'
   IXFAETYP       001-BYTE   CHARACTER   application specific data type = 'E' 
   IXFADATE       008-BYTE   CHARACTER   date written from the 'H' record
   IXFATIME       006-BYTE   CHARACTER   time written from the 'H' record

DB2 IDENTITY RECORD (RT=A+S)
  
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

DB2 SQLCA RECORD (RT=A+A)

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
import os,sys,json,csv,struct,time,traceback,logging, pprint

def readFilePart(fn,offset,read_len,lobFolder=None,trace=False):
    """
    Used by lob locators to retrieve the lob information of a lob.
    If the export was done with "lobs to" then unless you specify
    the lob folder this routine will attempt to search in the CWD
    for the lob file.
    """
    if trace:
        print("ReadFilePart:fn=",fn," offset=",offset,
              " len=",read_len," lobFolder=",lobFolder,
              file=sys.stderr
        )
    
    if not os.path.exists(fn):
        if lobFolder:
            #print(">>Using lobFolder:",lobFolder,file=sys.stderr)
            nfn=os.path.join(lobFolder,fn)
        else:
            nfn=fn
        if not os.path.exists(nfn):
            #print(">>Searching lobFolder:",lobFolder,file=sys.stderr)
            nfn=None
            for dirname,dirs,files in os.walk(lobFolder):
                if nfn:
                    break
                for sfn in files:
                    if sfn==fn:
                        nfn=os.path.join(dirname,sfn)
                        break
        if os.path.exists(nfn):
            fn=nfn
    
    with open(fn,"rb") as fin:
        fin.seek(offset, 0)
        return fin.read(read_len)    

class LobLocator:
    """
    Represent a lob locator, allowing for both db2 simple lob locator
    syntax (to be put in a .csv file) or access to the data by reading
    it from the lob storage (file).
    """
    def __init__(self,fp,offset,objlen,lobFolder=None,encoding=None):
        self.fp=fp
        self.offset=offset
        self.objlen=objlen
        self.lobFolder=lobFolder
        self.encoding=encoding
    
    def __str__(self):
        return self.fp+'.'+str(self.offset)+'.'+str(self.objlen)

    def __repr__(self):
        s="LobLocator('"+self.fp+"',"+str(self.offset)+","+str(self.objlen)
        if self.lobFolder:
            s=s+",lobFolder='"+self.lobFolder+"'"
        if self.encoding:
            s=s+",encoding='"+self.encoding+"'"            
        s=s+")"
        return s
    
    def getLobData(self,trace=False):
        if self.encoding:
            return readFilePart(self.fp, self.offset, self.objlen,self.lobFolder,trace).decode(self.encoding)
        return readFilePart(self.fp, self.offset, self.objlen,self.lobFolder,trace)
    
class IXFParser:
    """
    A reusable component used by the main method to implement the tool's logic. 
    You can reuse this in your own programs.
    """
    recordTypes={
        'H':{
            "fields":[
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
            "parser":"parseHeaderIXFRecord"
            },
        'T':{
            "fields":[
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
            "parser":"parseTableDefIXFRecord"
            },
        'C': {
            "fields":[
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
            "parser":"parseColumnDefIXFRecord"
        },
        'D':{
            "fields":[
               ['IXFDRID' ,3,"'D' record identifier"],
               ['IXFDFIL1',4,'reserved'],
               ['IXFDCOLS',0,'columnar data'],
           ],
            "parser":"parseRowDataIXFRecord"
        },
        'A':{
            "fields":[
               ['IXFAPPID',12,'application identifier'],
               ['IXFADATA', 0,'application-specific data'],
           ],
             "parser":"parseAppIXFRecord"
        }
    }
    
    # encoding the type storage length
    # >0 fixed size known by the type
    # 0 variable length the length is the first 2 bytes in ther data
    # -1 fixed length the column data_len is the storage length
    # -2 computed value from the column and type info 
    # -4 lob/clob
    # blob locators '960','916'
    # clob locators '964','968','920','924'
    typeInfo={
        '492':{'name':'BIGINT','length':8,'parser':'parseDataBigInteger'},
        '912':{'name':'BINARY','length':-1,'parser':'parseDataRaw'},
        '404':{'name':'BLOB','length':-4,'parser':'parseDataLob'},
        '408':{'name':'CLOB','length':-4,'parser':'parseDataLob'},
        '960':{'name':'BLOB_LOCATION_SPECIFIER ','length':-1,'parser':'parseDataLob'},
        '964':{'name':'CLOB_LOCATION_SPECIFIER ','length':-1,'parser':'parseDataLob'},
        '968':{'name':'DBCLOB_ LOCATION_ SPECIFIER','length':-1,'parser':'parseDataLob'},
        '916':{'name':'BLOB_FILE','length':-1,'parser':'parseDataLob'},
        '920':{'name':'CLOB_FILE','length':-1,'parser':'parseDataLob'},
        '924':{'name':'DBCLOB_FILE','length':-1,'parser':'parseDataLob'},
        '452':{'name':'CHAR','length':-1,'parser':'parseDataChars'},
        '384':{'name':'DATE','length':10,'parser':'parseDataChars'},
        '412':{'name':'DBCLOB','length':0,'parser':'parseDataLob'},
        '484':{'name':'DECIMAL','length':-2,'parser':'parseDataNum'},
        '996':{'name':'DECFLOAT','length':-2,'parser':'parseDataNum'},
        '480':{'name':'FLOATING POINT','length':-2,'parser':'parseFloat'},
        '468':{'name':'GRAPHIC','length':-1,'parser':'parseDataVarLen'},
        '496':{'name':'INTEGER','length':4,'parser':'parseDataInteger'},
        '456':{'name':'LONGVARCHAR','length':0,'parser':'parseDataVarLen'},
        '472':{'name':'LONG VARGRAPHIC','length':0,'parser':'parseDataVarLen'},
        '500':{'name':'SMALLINT','length':2,'parser':'parseSmallInt'},
        '388':{'name':'TIME','length':8,'parser':'parseDataChars'},
        '392':{'name':'TIMESTAMP','length':-2,'parser':'parseDataChars'},
        '908':{'name':'VARBINARY','length':0,'parser':'parseDataVarLen'},
        '448':{'name':'VARCHAR','length':0,'parser':'parseDataVarLen'},
        '464':{'name':'VARGRAPHIC','length':0,'parser':'parseDataVarLen'},
        '988':{'name':'XML','length':-4,'parser':'parseDataXML'},
    }
    
    dbCodePageToPythonCodePageMap={
        '01200':'UTF-8',
        '01208':'UTF-8'
    }
    
    def __init__(self,**args):
        self.endianism='<'
        self.tableDefProcessed=False
        self.tableDef={
            'name':None,
            'schema':None,
            'columns':[],
        }
        self.aRecords=[]
        self.inputEncoding=args.get('inputEncoding',None)
        self.outputEncoding=args.get('outputEncoding',"UTF-8")
        self.ixfHeader={}
        self.columns=[]
        self.currentRow=None
        self.ixfRecordCount=0
        self.columnCount=0
        self.rowCount=0
        self.totalDataSize=0
        self.totalLobSize=0
        self.totalLobCount=0
        self.minLobSize=-1
        self.maxLobSize=-1
        self.traceRecords=args.get('trace',False)
        self.lobFolder=args.get('lobFolder','.')
        self.outObj=args.get('out',None)
        self.output=None
        self.csvwriter=None
        self.fromRow=args.get('fromRow','-1')
        self.maxRows=args.get('maxRows','-1')
        self.fromRow=-1 if self.fromRow is None else int(self.fromRow)
        self.maxRows=-1 if self.maxRows is None else int(self.maxRows)
        
        # bind all record parsers to methods of this class
        for k in self.recordTypes:
            rt=self.recordTypes[k]
            pdn=rt['parser']
            if type(pdn) == str:
                rt['parser']=getattr(self, pdn)
            # if self.traceRecords:
            #     print("IXF record type:",k," using parser:",rt['parser'],file=sys.stderr)
        
        # bind all type parsers to methods of this class
        for k in self.typeInfo:
            td=self.typeInfo[k]
            pn=td['parser']
            if type(pn) == str:
                td['parser']=getattr(self, pn,self.parseDataRaw)
            # if self.traceRecords:
            #     print("Data type:",k," Using parser=",td['parser'],file=sys.stderr)
            
    def onTableDef(self):
        """
        Override in the derived class  
        Optional processing when the table definition is fully built.
        At this point a SQL statement can be created or the column list 
        written to a csv file 
        """
                
    def onRowReceived(self):
        """
        Override in the derived class  
        Process a data row if an output was defined
        """
        
    def onLastRecord(self):
        """
        Override in the derived class  
        """
    
    def beforeFirstRow(self):
        """
        Called when the 'T' record and all 'C' record were processed.
        This routine will fully define the table structure.
        """
        self.tableDef['columns']=self.columns
        self.colcidmap={}
        for cd in self.columns:
            cid=cd['cid']
            cim=self.colcidmap.get(cid)
            if cim is None:
                cim=[cd]
                self.colcidmap[cid]=cim
            else:
                cim.append(cd)
        if self.traceRecords:
            print("New table definition received:",
                  json.dumps(self.tableDef,indent=' ',sort_keys=True),
                  file=sys.stderr
            )
              
    def getColset(self,cid):
        return self.colcidmap.get(cid)
    
    def parseDataNum(self,coldef,data):
        # TODO: implement
        return self.parseDataRaw(coldef,data)

    def parseFloat(self,coldef,data):
        if len(data) == 4:
            return struct.unpack(self.endianism+'f',data)[0]
        return struct.unpack(self.endianism+'d',data)[0]

    def parseSmallInt(self,coldef,data):
        return struct.unpack(self.endianism+'h',data)[0]
    
    def parseDataInteger(self,coldef,data):
        return struct.unpack(self.endianism+'i',data)[0]

    def parseDataBigInteger(self,coldef,data):
        return struct.unpack(self.endianism+'q',data)[0]

    def parseDataVarLen(self,coldef,data):
        """
        """
        #if self.traceRecords:print(">>>parse_varlen:",data,file=sys.stderr)
        encoding=self.getColumnEncoding(coldef)      
        try:
            #return data[2:].decode(encoding)
            return data.decode(encoding)
        except Exception as x:
            print("parseDataVarLen:error:",x,file=sys.stderr)
            return data
    
    def getExternalLobIdentifier(self,lobColIdx):
        """
        TODO: REPLACE THIS WITH YOUR OWN IMPL IF NEEDED
        
        If the table contains lobs that should be saved in independent files
        then we need a way to name the lob file.
        There are many ways to name/id the lob object and usually it is related to
        other column values. For example if the row describes a person and the
        row contains that person's name then we can use it to to generate an id for
        its picture stored as a jpeg file in a lob. The file extension (.jpg) may also
        depend on the lob type column (or maybe default for this table).
        This means this method can be overloaded in order to allow you to name
        the lobs.
        By default we can generate a complete unique id by using the table name,
        column name and row number.
        we add the extension '.bin' if we have no idea of what the content is,
        '.txt' if this is a clob and '.xml' if an XML doc.
        """
        ts=self.tableDef.get('schema','noschema')
        tn=self.tableDef['name']
        cd=self.columns[lobColIdx]
        cn=cd['name']
        lt=cd['type']
        ext='.bin'
        if lt in ('964','968','920','924','408'):# clobs
            ext='.txt'
        elif lt == '988':
            ext='.xml'
        return tn+"_"+cn+"_"+str(self.rowCount)+ext 
    
    def isLobType(self,lobColIdx):
        """
        Return True if the column with index lobColIdx (zero based) is a lob (blob,clob,xml,etc)
        """
        return self.columns[lobColIdx]['type'] in ('960', '964', '968','916', '920', '924','988')
        
    def isTextLobType(self,lobColIdx):
        """
        Return True if the column with index lobColIdx (zero based) is a lob (blob,clob,xml,etc)
        """
        return self.columns[lobColIdx]['type'] in ('964','968','920','924','408','988')
    
    def parseDataLob(self,coldef,data):
        """
        Parse any lob (CLOB,BLOB,DBCLOB) and their locators 
        """
        encoding=self.getColumnEncoding(coldef)      
        # is this a lob locator?
        if coldef['type'] in ('960', '964', '968','916', '920', '924'):
            #print('>>LOBLOC:',coldef['type']," lcdata:",data,file=sys.stderr)
            lobloc=data[2:-1].decode(encoding)
            llc=lobloc.split('.')
            fn=".".join(llc[0:-2])
            offset=int(llc[-2])
            objlen=int(llc[-1])
            self.totalLobSize+=objlen
            if coldef['type'] in ('964','968','920','924'):
                lobLocator=LobLocator(fn,offset,objlen,self.lobFolder,encoding)
                if self.traceRecords:
                    print('>>LOBLOC_repr:',repr(lobLocator),file=sys.stderr)
                    print('>>LOBLOC     :',lobLocator,file=sys.stderr)
                    #print('>>CLOB:',lobLocator.getLobData(),file=sys.stderr)
            else:
                lobLocator=LobLocator(fn,offset,objlen,self.lobFolder)
                if self.traceRecords:
                    print('>>LOBLOC_repr:',repr(lobLocator),file=sys.stderr)
                    print('>>LOBLOC     :',lobLocator,file=sys.stderr)
                    #print('>>BLOB:',lobLocator.getLobData(),file=sys.stderr)
            return lobLocator
        
        if coldef['type'] == '408':
            # is a CLOB file 
            return data[2:].decode(encoding)
        
        return self.parseDataRaw(coldef,data[2:])

    def parseDataXML(self,coldef,data):
        """
        XML seems to be always created in a lob locator of its own format
        like: <XDS FIL='blobs_ixf_default.ixf.001.xml' OFF='58' LEN='1048' />
        """
        encoding=self.getColumnEncoding(coldef)      
        #print(">>XML locator raw:",data,file=sys.stderr)
        xml_loc=data[3:].decode(encoding).split(' ')
        #print(">>XML locator:",repr(xml_loc),file=sys.stderr)
        
        fn=xml_loc[1][5:-1]
        offset=int(xml_loc[2][5:-1])
        objlen=int(xml_loc[3][5:-1])
        lobLocator=LobLocator(fn,offset,objlen,self.lobFolder,encoding)
        self.totalLobSize+=objlen
        
        if self.traceRecords:
            print(">>XMLLOC_repr:",repr(lobLocator),file=sys.stderr)
            #print(">>XMLLOC_str :",lobLocator,file=sys.stderr)
            #print(">>XMLDOC:",lobLocator.getLobData(),file=sys.stderr)
        
        return lobLocator
        
    def parseDataChars(self,coldef,data):
        """
        """
        #print(">>>parse_chars:",data,file=sys.stderr)
        try:
            encoding=self.getColumnEncoding(coldef)      
            return data.decode(encoding)
        except Exception as x:
            print("parseDataChars:error:",x,file=sys.stderr)
            return data
    
    def parseInt(self,bstr,dv=0):
        """
        Parse an integer value from a binary string containing a list of character digits. 
        """
        try:
            #return struct.unpack(self.endianism+'i',bstr)[0]
            return int(bstr.decode(self.getIXFFileEncoding())) #TODO: default encoding 
        except:
            return dv
    
    def parseDataRaw(self,coldef,data):
        """
        A generic placeholder for a unspecified parser.
        Returns data as is provided in the parameter.
        """
        return data
    
    def getIXFFileEncoding(self):
        if self.inputEncoding:
            return self.inputEncoding
        
        ixfCp=self.tableDef.get('dbcodepage',None)
        if ixfCp is None:
            ixfCp=self.tableDef.get('sbcodepage',None)
        if ixfCp is None:
            ixfCp=self.ixfHeader.get('dbcodepage',None)
        if ixfCp is None:
            ixfCp=self.ixfHeader.get('sbcodepage',None)
        
        if ixfCp is None:
            ixfCp='01200'
            if self.traceRecords:
                print("WARNING! No code page found the IXF records, using the default:",ixfCp,file=sys.stderr)
            
        cpn=self.dbCodePageToPythonCodePageMap.get(ixfCp,None)
        if cpn is None:
            raise Exception("Unable to map db-codepage:"+ixfCp+" to a python codepage")
        return cpn
        
    def getColumnEncoding(self,coldef):
        """
        The encoding for a column is checked first in the column definition
        then in the Table header then in the IXF header.
        The found value is then mapped to a python code-page.
        if you provide your own inputEncoding then it will override
        the IXF code page. This allows you to override the IXF code page
        in case you need to do so. 
        """
        if self.inputEncoding:
            return self.inputEncoding
        
        ixfCp=coldef.get('dbcodepage',None)
        if ixfCp is None:
            ixfCp=coldef.get('sbcodepage',None)
        if ixfCp is None:
            return self.getIXFFileEncoding()
          
        cpn=self.dbCodePageToPythonCodePageMap.get(ixfCp,None)
        if cpn is None:
            raise Exception("Unable to map db-codepage:"+ixfCp+" to a python codepage")
        return cpn
       
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
            if len(blen)==4:
                ln=struct.unpack(self.endianism+'I',blen)[0]
            else:
                ln=struct.unpack(self.endianism+'H',blen)[0]
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
        """
        
        """
        colset=self.getColset(cid)
        if colset is None:return None
        
        for cd in colset:
            td=self.typeInfo[cd['type']]
            pos=cd['pos']-1
            len,cbdt = self.getFieldActualLengthAndData(cd,td,pos,data)
            if len<0:return None
            cv=td['parser'](cd,cbdt)
            if self.traceRecords:
                print("Parsing column:",cd['colno'],
                      " name:",cd['name'],
                      " data:",cbdt,
                      " parser:",td['parser'],
                      " parsedValue:",cv,
                      "\n prow:",self.currentRow,
                      file=sys.stderr
                )
            self.currentRow[cd['colno']]=cv

    def parseHeaderIXFRecord(self,rdtitms):
        """
       HEADER RECORD (RT=H)
     
       FIELD NAME         LENGTH    TYPE        COMMENTS
       ----------         -------   ---------   -------------
       IXFHRECL          06-BYTE   CHARACTER   record length
       IXFHRECT          01-BYTE   CHARACTER   record type = 'H'
       IXFHID  [0]       03-BYTE   CHARACTER   IXF identifier
       IXFHVERS[1]       04-BYTE   CHARACTER   IXF version
       IXFHPROD[2]       12-BYTE   CHARACTER   product
       IXFHDATE[3]       08-BYTE   CHARACTER   date written
       IXFHTIME[4]       06-BYTE   CHARACTER   time written
       IXFHHCNT[5]       05-BYTE   CHARACTER   heading record count
       IXFHSBCP[6]       05-BYTE   CHARACTER   single byte code page
       IXFHDBCP[7]       05-BYTE   CHARACTER   double byte code page
       IXFHFIL1[8]       02-BYTE   CHARACTER   reserved
       
       IXF Header record sample:
       H: [
           b'IXF', 
           b'0002', 
           b'DB2    02.00', 
           b'20240208', 
           b'112316', 
           b'00006', 
           b'01208', 
           b'01200', 
           b'  '
        ]

        """
        self.ixfHeader['ixfid']=rdtitms[0].decode(self.getIXFFileEncoding())
        self.ixfHeader['version']=rdtitms[1].decode(self.getIXFFileEncoding())
        self.ixfHeader['product']=rdtitms[2].decode(self.getIXFFileEncoding())
        self.ixfHeader['writtenDate']=rdtitms[3].decode(self.getIXFFileEncoding())
        self.ixfHeader['writtenTime']=rdtitms[4].decode(self.getIXFFileEncoding())
        self.ixfHeader['headingRowcount']=self.parseInt(rdtitms[5],0),
        self.ixfHeader['sbcodepage']=rdtitms[6].decode(self.getIXFFileEncoding())
        self.ixfHeader['dbcodepage']=rdtitms[7].decode(self.getIXFFileEncoding())
        
    def parseTableDefIXFRecord(self,rdtitms):
        """
        TABLE RECORD (RT=T)
     
       FIELD NAME         LENGTH     TYPE        COMMENTS
       ----------         -------    ---------   -------------
    
       IXFTRECL           006-BYTE   CHARACTER   record length
       IXFTRECT           001-BYTE   CHARACTER   record type = 'T'
       IXFTNAML[00]       003-BYTE   CHARACTER   name length
       IXFTNAME[01]       256-BYTE   CHARACTER   name of data
       IXFTQULL[02]       003-BYTE   CHARACTER   qualifier length
       IXFTQUAL[03]       256-BYTE   CHARACTER   qualifier
       IXFTSRC [04]       012-BYTE   CHARACTER   data source
       IXFTDATA[05]       001-BYTE   CHARACTER   data convention = 'C'
       IXFTFORM[06]       001-BYTE   CHARACTER   data format = 'M'
       IXFTMFRM[07]       005-BYTE   CHARACTER   machine format = 'PC'
       IXFTLOC [08]       001-BYTE   CHARACTER   data location = 'I'
       IXFTCCNT[09]       005-BYTE   CHARACTER   'C' record count
       IXFTFIL1[10]       002-BYTE   CHARACTER   reserved
       IXFTDESC[11]       030-BYTE   CHARACTER   data description
       IXFTPKNM[12]       257-BYTE   CHARACTER   primary key name
       IXFTDSPC[13]       257-BYTE   CHARACTER   reserved
       IXFTISPC[14]       257-BYTE   CHARACTER   reserved
       IXFTLSPC[15]       257-BYTE   CHARACTER   reserved
       
       IXF Table record sample:
       T: [
           b'021', 
           b'blobs_ixf_default.ixf                                                                                                                                                                                                                                           ', 
           b'000', 
           b'                                                                                                                                                                                                                                                                ', 
           b'            ', 
           b'C', 
           b'M', 
           b'PC   ', 
           b'I', 
           b'00004', 
           b'  ', 
           b'\x00                             ', 
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ]

        """
        nameLen=self.parseInt(rdtitms[0])
        name=rdtitms[1][:nameLen].decode(self.getIXFFileEncoding())
        if name.endswith('.ixf'):
            name=name[:-4]
        
        self.tableDef['name']=name
        nameLen=self.parseInt(rdtitms[2])
        self.tableDef['qualifier']=rdtitms[3][:nameLen].decode(self.getIXFFileEncoding())
        
        if rdtitms[4][0]==0:
            self.tableDef['dataSource']=None
        else:
            self.tableDef['dataSource']=rdtitms[4].decode(self.getIXFFileEncoding()).strip()
            
        self.tableDef['dataConvention']=rdtitms[5].decode(self.getIXFFileEncoding()).strip()
        self.tableDef['dataFormat']=rdtitms[6].decode(self.getIXFFileEncoding()).strip()
        self.tableDef['machineFormat']=rdtitms[7].decode(self.getIXFFileEncoding()).strip()
        self.tableDef['dataLocation']=rdtitms[8].decode(self.getIXFFileEncoding()).strip()
        self.tableDef['colRecordCount']=self.parseInt(rdtitms[9])
        
        if rdtitms[11][0]==0:
            self.tableDef['description']=None
        else:
            self.tableDef['description']=rdtitms[11].decode(self.getIXFFileEncoding()).strip()
            
        if rdtitms[12][0]==0:
            self.tableDef['pkName']=None
        else:
            self.tableDef['pkName']=rdtitms[12].decode(self.getIXFFileEncoding()).strip()
        
    def parseColumnDefIXFRecord(self,rdtitms):
        """
        COLUMN DESCRIPTOR RECORD (RT=C)
     
       FIELD NAME         LENGTH     TYPE        COMMENTS
       ----------         -------    ---------   -------------
       IXFCRECL[-2]       006-BYTE   CHARACTER   record length
       IXFCRECT[-1]       001-BYTE   CHARACTER   record type = 'C'
       
       IXFCNAML[00]       003-BYTE   CHARACTER   column name length
       IXFCNAME[01]       256-BYTE   CHARACTER   column name
       IXFCNULL[02]       001-BYTE   CHARACTER   column allows nulls
       IXFCDEF [03]       001-BYTE   CHARACTER   column has defaults
       IXFCSLCT[04]       001-BYTE   CHARACTER   column selected flag
       IXFCKPOS[05]       002-BYTE   CHARACTER   position in primary key
       IXFCCLAS[06]       001-BYTE   CHARACTER   data class
       IXFCTYPE[07]       003-BYTE   CHARACTER   data type
       IXFCSBCP[08]       005-BYTE   CHARACTER   single byte code page
       IXFCDBCP[09]       005-BYTE   CHARACTER   double byte code page
       IXFCLENG[10]       005-BYTE   CHARACTER   column data length
       IXFCDRID[11]       003-BYTE   CHARACTER   'D' record identifier
       IXFCPOSN[12]       006-BYTE   CHARACTER   column position
       IXFCDESC[13]       030-BYTE   CHARACTER   column description
       IXFCLOBL[14]       020-BYTE   CHARACTER   lob column length
       IXFCUDTL[15]       003-BYTE   CHARACTER   UDT name length
       IXFCUDTN[16]       256-BYTE   CHARACTER   UDT name
       IXFCDEFL[17]       003-BYTE   CHARACTER   default value length
       IXFCDEFV[18]       254-BYTE   CHARACTER   default value
       IXFCREF [19]       001-BYTE   CHARACTER   reference type
       IXFCNDIM[20]       002-BYTE   CHARACTER   number of dimensions
       IXFCDSIZ[21]       varying    CHARACTER   size of each dimension
       
       Sample: IXF Column record
       C: [
       b'005', 
       b'LOBNO                                                                                                                                                                                                                                                           ', 
       b'N', 
       b'N', 
       b'Y', 
       b'01', 
       b'R', 
       b'496', 
       b'00000', 
       b'00000', 
       b'     ', 
       b'001', 
       b'000001', 
       b'                              ', 
       b'00000000000000000000', 
       b'000', 
       b'0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 
       b'000', 
       b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 
       b'0', 
       b'00', 
       b'0000000000'
       ]

        """
        colNameLen=self.parseInt(rdtitms[0])
        col={}
        
        col['colno']=self.columnCount
        col['name']=(rdtitms[1][:colNameLen]).decode(self.getIXFFileEncoding())
        
        col['nullable']=rdtitms[2].decode(self.getIXFFileEncoding())
        col['hasdefault']=rdtitms[3].decode(self.getIXFFileEncoding())
        if rdtitms[5][0] == b'\x00':
            col['pkpos']=None
        else:
            col['pkpos']=rdtitms[5].decode(self.getIXFFileEncoding())
            if col['pkpos'] == 'N\x00':
                col['pkpos']=None
        col['selected']=rdtitms[4].decode(self.getIXFFileEncoding())
        col['colDataClass']=rdtitms[6].decode(self.getIXFFileEncoding())
        col['type']=rdtitms[7].decode(self.getIXFFileEncoding())
        col['sbcodepage']=rdtitms[8].decode(self.getIXFFileEncoding())
        if col['sbcodepage']=='00000':
            col['sbcodepage']=None
        col['dbcodepage']=rdtitms[9].decode(self.getIXFFileEncoding())
        if col['dbcodepage'] == '00000':
            col['dbcodepage']=None
        col['data_len']=self.parseInt(rdtitms[10])
        col['cid']=self.parseInt(rdtitms[11])
        col['pos']=self.parseInt(rdtitms[12])
        col['description']=rdtitms[9].decode(self.getIXFFileEncoding())
        if col['description'] == '00000':
            col['description']=None
        col['lob_len']=self.parseInt(rdtitms[14])
        col['udt']=(rdtitms[16][:self.parseInt(rdtitms[15])]).decode(self.getIXFFileEncoding())
        col['defaultValue']=(rdtitms[18][:self.parseInt(rdtitms[17])]).decode(self.getIXFFileEncoding())
        col['refType']=rdtitms[19].decode(self.getIXFFileEncoding())
        col['numDimensions']=self.parseInt(rdtitms[20])
        if col['numDimensions']>0:
            col['dimensionSizes']=rdtitms[21].decode(self.getIXFFileEncoding())
        else:
            col['dimensionSizes']=None
        col['typeName']=self.typeInfo[col['type']]['name']
        self.columns.append(col)
        self.columnCount+=1
        
    def parseRowDataIXFRecord(self,rdtitms):
        """
        DATA RECORD (RT=D)
     
       FIELD NAME     LENGTH    TYPE        COMMENTS
       ----------     -------   ---------   -------------
       IXFDRECL       06-BYTE   CHARACTER   record length
       IXFDRECT       01-BYTE   CHARACTER   record type = 'D'
       IXFDRID        03-BYTE   CHARACTER   'D' record identifier
       IXFDFIL1       04-BYTE   CHARACTER   reserved
       IXFDCOLS       varying   variable    columnar data 
        """
        if not self.tableDefProcessed:
            self.beforeFirstRow()
            self.tableDefProcessed=True
            
        colno=self.parseInt(rdtitms[0])
        
        if colno==1:
            if not self.currentRow is None:
                self.onRowReceived()
                self.rowCount+=1
            self.currentRow=[None]*self.columnCount
        
        self.parseColumnsForField(colno,rdtitms[2])
 
    IXFAppDB2RecDescriptors={
        "I":{
            "fields":[
               ["IXFADATE"  ,8  ,"CHARACTER","date written from the 'H' record",True],
               ["IXFATIME"  ,6  ,"CHARACTER","time written from the 'H' record",True],
               ["IXFANDXL"  ,2  ,"SHORT INT","length of name of the index",False],
               ["IXFANDXN"  ,256,"CHARACTER","name of the index",True],
               ["IXFANCL"   ,2  ,"SHORT INT","length of name of the index creator",False],
               ["IXFANCN"   ,256,"CHARACTER","name of the index creator",True],
               ["IXFATABL"  ,2  ,"SHORT INT","length of name of the table",False],
               ["IXFATABN"  ,256,"CHARACTER","name of the table",True],
               ["IXFATCL"   ,2  ,"SHORT INT","length of name of the table creator",False],
               ["IXFATCN"   ,256,"CHARACTER","name of the table creator",True],
               ["IXFAUNIQ"  ,1  ,"CHARACTER","unique rule",True],
               ["IXFACCNT"  ,2  ,"SHORT INT","column count",True],
               ["IXFAREVS"  ,1  ,"CHARACTER","allow reverse scan flag",True],
               ["IXFAIDXT"  ,1  ,"CHARACTER","type of index",True],
               ["IXFAPCTF"  ,2  ,"CHARACTER","amount of pct free",True],
               ["IXFAPCTU"  ,2  ,"CHARACTER","amount of minpctused",True],
               ["IXFAEXTI"  ,1  ,"CHARACTER","reserved",True],
               ["IXFACNML"  ,6  ,"SHORT INT","length of name of the columns",False],
               ["IXFACOLN"  ,-1 ,"CHARACTER","name of the columns in the index",True]
           ],
            "parser":""
        },
        "X":{
            "fields":[
               ["IXFADATE"  ,8  ,"CHARACTER","date written from the 'H' record",True],
               ["IXFATIME"  ,6  ,"CHARACTER","time written from the 'H' record",True],
               ["IXFAYCNT"  ,10 ,"CHARACTER","'Y' record count for this hierarchy",True],
               ["IXFAYSTR"  ,10 ,"CHARACTER","starting column of this hierarchy",True]                
            ],
            "parser":""
        },
        "Y":{
            "fields":[
               ["IXFADATE"  ,8  ,"CHARACTER","date written from the 'H' record",True],
               ["IXFATIME"  ,6  ,"CHARACTER","time written from the 'H' record",True],
               ["IXFASCHL"  ,3  ,"CHARACTER","type schema name length",False],
               ["IXFASCHN"  ,256,"CHARACTER","type schema name",True],
               ["IXFATYPL"  ,3  ,"CHARACTER","type name length",False],
               ["IXFATYPN"  ,256,"CHARACTER","type name",True],
               ["IXFATABL"  ,3  ,"CHARACTER","table name length",False],
               ["IXFATABN"  ,256,"CHARACTER","table name",True],
               ["IXFAPNDX"  ,10 ,"CHARACTER","subtable index of parent table",True],
               ["IXFASNDX"  ,5  ,"CHARACTER","starting column index of current table",True],                                               
               ["IXFAENDX"  ,5  ,"CHARACTER","ending column index of current table",True]
            ],
            "parser":""
        },
        "C":{
            "fields":[
               ["IXFADATE"  ,8  ,"CHARACTER","date written from the 'H' record",True],
               ["IXFATIME"  ,6  ,"CHARACTER","time written from the 'H' record",True],
               ["IXFALAST"  ,2  ,"SHORT INT","last diskette volume number",True],
               ["IXFATHIS"  ,2  ,"SHORT INT","this diskette volume number",True],
               ["IXFANEXT"  ,2  ,"SHORT INT","next diskette volume number",True]
            ],
            "parser":""
        },
        "E":{
            "fields":[
               ["IXFADATE"  ,8  ,"CHARACTER","date written from the 'H' record",True],
               ["IXFATIME"  ,6  ,"CHARACTER","time written from the 'H' record",True]
            ],
            "parser":""
        },
        "S":{
            "fields":[
               ["IXFADATE"  ,8  ,"CHARACTER","application record creation date",True],
               ["IXFATIME"  ,6  ,"CHARACTER","application record creation time",True],
               ["IXFACOLN"  ,6  ,"CHARACTER","column number of the identity column",True],
               ["IXFAITYP"  ,1  ,"CHARACTER","generated always ('Y' or 'N')",True],
               ["IXFASTRT"  ,33 ,"CHARACTER","identity START AT value",True],
               ["IXFAINCR"  ,33 ,"CHARACTER","identity INCREMENT BY value",True],
               ["IXFACACH"  ,10 ,"CHARACTER","identity CACHE value",True],
               ["IXFAMINV"  ,33 ,"CHARACTER","identity MINVALUE",True],
               ["IXFAMAXV"  ,33 ,"CHARACTER","identity MAXVALUE",True],
               ["IXFACYCL"  ,1  ,"CHARACTER","identity CYCLE ('Y' or 'N')",True],
               ["IXFAORDR"  ,1  ,"CHARACTER","identity ORDER ('Y' or 'N')",True],
               ["IXFARMRL"  ,3  ,"CHARACTER","identity Remark length",True],
               ["IXFARMRK"  ,254,"CHARACTER","identity Remark value",True]
            ],
            "parser":""
        },
        "A":{
            "fields":[
               ["IXFADATE"  ,8  ,"CHARACTER","date written from the 'H' record",True],
               ["IXFATIME"  ,6  ,"CHARACTER","time written from the 'H' record",True],
               ["IXFASLCA"  ,136,"BYTES"    ,"sqlca - SQL communications area",True]
            ],
            "parser":""
        },        
    }
    
    def parseAppIXFRecord(self,rdtitms):
        """
        APPLICATION RECORD (RT=A)
     
       FIELD NAME     LENGTH    TYPE        COMMENTS
       ----------     -------   ---------   -------------
       IXFARECL       06-BYTE   CHARACTER   record length
       IXFARECT       01-BYTE   CHARACTER   record type = 'A'
       IXFAPPID       12-BYTE   CHARACTER   application identifier
       IXFADATA       varying   variable    application-specific data
        """
        applId=rdtitms[0].decode(self.getIXFFileEncoding())
        if applId == 'DB2    02.00':
            record={}
            recType=rdtitms[1][:1].decode(self.getIXFFileEncoding())[0]
            record['IXFACTYP']=recType
            
            recDef=self.IXFAppDB2RecDescriptors.get(recType,None)
            if recDef:
                recFields=recDef['fields']
                nextRecLen=None
                binbuff=rdtitms[1][1:]
                for rd in recFields:
                    recLen=rd[1]
                    itm=binbuff[:recLen]
                    binbuff=binbuff[recLen:]
                    
                    if rd[4]:
                        if nextRecLen:
                            val=itm[:nextRecLen].decode(self.getIXFFileEncoding())
                            nextRecLen=None
                        else:
                            try:
                                val=itm.decode(self.getIXFFileEncoding())
                            except Exception as x:
                                val=itm
                        record[rd[0]]=val
                    else:
                        nextRecLen=self.parseInt(itm)
                self.aRecords.append(record)
                
    def handleLobObject(self,cidx):
        """
        TODO: replace if you need a different approach!
        
        Default implementation will save each lob in a file in the given path.
        Override this method to implement your own lob processing! 
        Return a piece of identity to be placed in the csv record (for example).
        """
        if self.output is None:
            print(">>> Skip lob output for self.output is None",file=sys.stderr)
            return
        if type(self.outObj) != str:
            print(">>> Skip lob output for self.outObj type is:",type(self.outObj),file=sys.stderr)
            return
        
        fn=self.getExternalLobIdentifier(cidx)
        if os.path.isdir(self.outObj):
            fd=self.outObj
        else:
            fd=os.path.dirname(self.outObj)    
        fp=os.path.join(fd,fn)
        
        if self.isTextLobType(cidx):
            ft='wt'
        else:
            ft='wb'
        
        ld=self.currentRow[cidx]
        if type(ld) == LobLocator:
            ld=ld.getLobData(self.traceRecords)
        if ld and len(ld)>0:
            with open(fp,ft) as out:
                if self.traceRecords:print(">>> Writing lob:",fp,file=sys.stderr)
                self.totalLobCount+=1
                self.totalDataSize+=len(ld)
                out.write(ld)
        return fn
    
    def parseIXFRecordFromStream(self,feed):
        """
        Given an input stream (feed parameter) read and parse the next IXF record.
        
       FIELD NAME     LENGTH    TYPE        COMMENTS
       ----------     -------   ---------   -------------
       IXFHRECL       06-BYTE   CHARACTER   record length
       IXFHRECT       01-BYTE   CHARACTER   record type = 'H'
       
    Read the header and get the length and type of the record then
    parse the data based on the record type.
        """
        ln=feed.read(6)
        if not ln or len(ln)<6:
            self.onLastRecord()
            return False
        rt=feed.read(1)
        if not rt:
            self.onLastRecord()
            return False
        ln=self.parseInt(ln)
        rt=rt.decode() # TODO: encoding?
        rdt=feed.read(ln-1)
        
        rdtitms=[]
        self.ixfRecordCount+=1
        
        recd=self.recordTypes.get(rt) # retrieve the definition of the current record
        if not recd:
            self.unknownRecTypes+=1
            print("Unknown IXF record type:",rt,file=sys.stderr)
            return True
        
        # parse the record based on its field lengths
        rst=recd['fields']
        off=0
        for r in rst[:-1]:
            rl=int(r[1])
            rdtitms.append(rdt[off:off+rl])
            off+=rl
        rdtitms.append(rdt[off:])
        
        if self.traceRecords:
            print(rt+":",repr(rdtitms),file=sys.stderr)
        
        # catch parsing record exceptions in order to continue with the next record
        # this make the logic more robust on files that have some errors at record level
        # for few records but the rest of the file is OK.
        try:
            recParser=recd['parser']
            if self.traceRecords:
                print("Parsing record with parser:",recParser,file=sys.stderr)
            recParser(rdtitms)
        except Exception as x:
            #self.currentRow=None
            traceback.print_exc(file=sys.stdout)
        
        return True
    
    def processIFXRecords(self,feed,feedFolder=None):
        """
    An IXF File is a collection of records that start with this header:
    
       FIELD NAME     LENGTH    TYPE        COMMENTS
       ----------     -------   ---------   -------------
       IXFHRECL       06-BYTE   CHARACTER   record length
       IXFHRECT       01-BYTE   CHARACTER   record type = 'H'
       
    Read the header and get the length and type of the record then
    parse the data based on the record type.
        """
        if feedFolder:
            if not self.lobFolder:
                self.lobFolder=feedFolder
        self.tableDef={}
        self.columns=[]
        self.columnCount=0
        self.rowCount=0
        self.totalDataSize=0
        self.totalLobSize=0
        self.minLobSize=-1
        self.maxLobSize=-1
        self.currentRow=None
        self.unknownRecTypes=0
        self.aRecords=[]
        self.ixfHeader={}
        
        while self.parseIXFRecordFromStream(feed):
            if self.maxRows>0:
                if self.rowCount>=self.maxRows:
                    break
        
class IXFParserWriteCsv(IXFParser):
    """
    An IXF parser that writes the row data in a .csv file
    """
    
    def __init__(self,**args):
        IXFParser.__init__(self,**args)
        # todo, add csv, output parameters
        self.csvwriter=None
    
    def onTableDef(self):
        """
        Optional processing when the table definition is fully built.
        At this point a SQL statement can be created or the column list 
        written to a csv file 
        """
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
        if self.fromRow>0:
            if self.rowCount<self.fromRow:
                print("Skipping beginning row!",file=sys.stderr)
                return # skip rows output if required
        #print("self.tableDef",self.tableDef,file=sys.stderr)
        if self.traceRecords:
            print(">>> Final-Row[",self.rowCount,"]=",repr(self.currentRow),file=sys.stderr)
        for cidx in range(len(self.columns)):
            if self.isLobType(cidx):
                nlv=self.handleLobObject(cidx)
                self.currentRow[cidx]=nlv
        
        if self.csvwriter:          
            self.csvwriter.writerow(    
                [repr(x) if type(x) == bytes else x for x in self.currentRow]
            )
    
    def onLastRecord(self):
        """
        Do the cleanup for a file conversion.
        """
        if self.output:
            self.output.flush()
            if self.output!=sys.stdout:
                self.output.close()

    def setOutput(self,output):
        if self.output:
            self.output.close()
        self.output=output
        self.csvwriter=csv.writer(self.output)
        
class IXFParserWriteJSON(IXFParser):
    """
    An IXF parser that writes the row data in a .JSON file
    """
    
    def __init__(self,**args):
        IXFParser.__init__(self,**args)
    
    def onTableDef(self):
        """
        A json table is a list of records so we write a list start line
        """
        print("[",file=self.output)
        
    def onRowReceived(self):
        """
        Process a data row if an output was defined
        """
        if self.fromRow>0:
            if self.rowCount<self.fromRow:
                return # skip rows output if required
        
        for cidx in range(len(self.columns)):
            if self.isLobType(cidx):
                nlv=self.handleLobObject(cidx)
                self.currentRow[cidx]=nlv
                
        rowMap={}
        for i in range(len(self.currentRow)):
            rowMap[self.columns[i],self.currentRow[i]]
        
        json.dump(rowMap, self.output,indent="  ",sort_keys=True)
        
    def onLastRecord(self):
        """
        Do the cleanup for a file conversion.
        """
        if self.output:
            print("]",file=self.output)
            self.output.flush()
            if self.output!=sys.stdout:
                self.output.close()

    def setOutput(self,output):
        if self.output:
            self.output.close()
        self.output=output

    def handleLobObject(self,cidx):
        """
        TODO: replace if you need a different approach!
        
        Default implementation will save each lob in a file in the given path.
        Override this method to implement your own lob processing! 
        Return a piece of identity to be placed in the csv record (for example).
        """
        if self.output is None:return
        
        fn=self.getExternalLobIdentifier(cidx)
        if type(self.outObj) == str:
            if os.path.isdir(self.outObj):
                fd=self.outObj
            else:
                fd=os.path.dirname(self.outObj)    
            fp=os.path.join(fd,fn)
            
            if self.isTextLobType(cidx):
                ft='wt'
            else:
                ft='wb'
            
            if self.traceRecords:
                print("Writing lob:",fp,file=sys.stderr)
            
            with open(fp,ft) as out:
                ld=self.currentRow[cidx]
                if type(ld) == LobLocator:
                    ld=ld.getLobData(self.traceRecords)
                out.write(ld)
            return fn
        
        raise Exception("JSON in document inlining is not yet supported!")
        
class IXFParserGetFileInfo(IXFParser):
    """
    An IXF parser that extracts statistics from an .ixf file
    and write's them down to a file or stdout using a format
    like text, csv, json, xml (only text and json is supported now)
    """
    
    def __init__(self,**args):
        IXFParser.__init__(self,**args)
    
    def onTableDef(self):
        """
        """
        if self.output:
            json.dump(self.tableDef, self.output)
     
    def onRowReceived(self):
        """
        """
        if self.output:
            json.dump(self.tableDef, self.output)
        
    def onLastRecord(self):
        """
        Output the stats info to the output file and format 
        """
        if self.output:
            self.output.close()        
        
    def setOutput(self,output):
        if self.output:
            self.output.close()
        self.output=output
        
def processSingleFile(cmd,inp,outp,**args):
    """
    Process a single ixf file given an IXF instance processor
    a command and input output file paths.
    """
    out=None
    if cmd == 'convert':
        if type(outp) == str:
            outp=os.path.abspath(outp)
            if not os.path.exists(outp):
                if outp.endswith(".csv") or outp.endswith(".json"):
                    os.makedirs(os.path.dirname(outp), exist_ok=True)
                else:
                    os.makedirs(outp, exist_ok=True)
            if os.path.isdir(outp):
                ofn=os.path.splitext(os.path.basename(inp))[0]+('.csv' if args['outfmt']=='csv' else '.json')
                outp=os.path.join(outp,ofn)
            
            print("Writing to file:",outp,file=sys.stderr)
            out=open(outp,"wt")
        else:
            print("Writing to stdout",file=sys.stderr)
            
        fmt=args.get('outfmt','csv')
        if fmt == 'csv':
            ixfp=IXFParserWriteCsv(**args)
        elif fmt == 'json':
            ixfp=IXFParserWriteJSON(**args)
        else:
            raise Exception("Invalid output format:"+args['outfmt'])
    else:
        ixfp=IXFParserGetFileInfo(**args)
        
    ixfp.setOutput(out)
    
    print("Start processing input from:",inp,"\n using parser:",ixfp,file=sys.stderr)
    if out:
        print("Writing data to:",outp,file=sys.stderr)
    
    start=time.time()
    if type(inp) == str: 
        with open(inp,"rb") as fin:
            print("Reading from:",inp,file=sys.stderr)
            ixfp.processIFXRecords(fin,os.path.dirname(inp))
    else:
        print("Reading from:stdin",file=sys.stderr)
        ixfp.processIFXRecords(inp,args.get('lobFolder','.'))        
    stop=time.time()
        
    if cmd == 'info':
        print(file=sys.stderr)
        print("IXFHeader:",file=sys.stderr)
        pprint.pprint(ixfp.ixfHeader, sys.stderr)
        print("A-Records:",file=sys.stderr)
        pprint.pprint(ixfp.aRecords, sys.stderr)
        print("TableDescriptor:",file=sys.stderr)
        pprint.pprint(ixfp.tableDef, sys.stderr)
    
    print("Table   Name:",ixfp.tableDef.get('name',"unknown"),file=sys.stderr)
    print("Column count:",ixfp.columnCount,file=sys.stderr)
    print("Lobs    size:",ixfp.totalLobSize,file=sys.stderr)           
    print("Lob    count:",ixfp.totalLobCount,file=sys.stderr)
    print("Row    count:",ixfp.rowCount,file=sys.stderr)
    print("Processing time(sec):",stop-start,file=sys.stderr)
   

def batchProcess(cmd,inp,outp=None,**args):
    """
    Process a set of files as a batch.
    List file information/stats or convert to .csv.
    """
    if (cmd == 'convert') and (outp is None):
        raise Exception("Output path is not a folder!")
    
    print("Start processing folder:",inp,file=sys.stderr)
    pfc=0
    for fn in os.listdir(inp):
        if fn.endswith('.ixf'):
            infp=os.path.join(inp,fn)
            outfp=os.path.join(outp,fn[:-3]+'csv') if cmd=='convert' else None
            processSingleFile(cmd,infp,outfp,**args)
            pfc+=1
    if pfc>0:
        print("End processing, file count:",pfc,file=sys.stderr)
    else:
        print("End processing, no files found!",pfc,file=sys.stderr)        
    
def main():
    """
    """
    if len(sys.argv)==1:
        print("""
Analyze or convert IXF format files/bundles to csv or json
Syntax:
 IXFTols <name-value-parameter-list>
 
 Parameters:
    cmd - command, optional, values (info,convert) default info
    in  - input entity, can be '-' for stdin (default) or a path to an .ixf file
          or folder containing .ixf files (when batch processing is done)
    out - output entity, can be '-' for stdout (default) or a path to a file or
          folder where the converted files will be stored
    outfmt - output format, can be csv or json default csv
    otputLobStrategy - what to do with the lob data, by default is 'detached'
          where each lob is written to a single file (this is default and only one
          supprted in this version)
    fromRow - if provided allows for skipping a number of rows before start processing
    maxRows - if provided can help limit the number of rows processed 
    trace - y|n if y then additional information about ixf records will be output on stderr
        """,file=sys.stderr)
        return True
    
    args = {}
    args['cmd'] = 'info'
    args['outfmt'] = 'csv'
    args['lobFolder'] = None
    args['outputEncoding'] = None
    args['ouputLobStrategy'] = "detached" # also detached (name can be pk, or hash
    args['trace'] = 'n'
    args['fromRow'] = None
    args['maxRows'] = None
    
    inp = None
    out = None
    
    pav=[]
    for arg in sys.argv[1:]:
        aa=arg.split('=')
        if len(aa)==1:
            pav.append(arg)
        else:
            n=aa[0]
            v=aa[1]
            args[n]=v            
            if n == 'in':
                inp=v
            elif n == 'out':
                out=v
    
    # interpret positional values
    for pv in pav:
        if pv in ('info','convert'):
            args['cmd']=pv
        elif pv in ('trace','-t'):
            args['trace']=True
        elif pv=='-':
            if inp is None:
                inp=pv
            elif out is None:
                out=pv
        elif os.path.exists(pv):
            if inp is None:
                inp=pv
            elif out is None:
                out=pv
    
    args['trace']=args['trace']=='y'
    if inp is None:inp='.'
    if inp in ('-','stdin'):inp=sys.stdin
    if out in ('-','stdout'):out=sys.stdout
    
    if type(inp) == str:
        if not os.path.exists(inp):
            print("Input file does not exists! ",inp,file=sys.stderr)
            return False
    
    if out is None:
        if type(inp) == str:
            if os.path.isdir(inp):
                out=inp
            else:
                out=os.path.splitext(inp)[0]+('.csv' if args['outfmt']=='csv' else '.json')  
        else:
            out='.'
    
    if not args['lobFolder'] :
        if type(inp) == str:
            if os.path.isdir(inp):
                args['lobFolder']=inp
            else:
                args['lobFolder']=os.path.dirname(inp)
        else:
            args['lobFolder']='.'
    
    if args['cmd'] == 'info':out=None
    
    args['in']=inp
    args['out']=out
    print("Start processing with arguments:",args,file=sys.stderr)
    
    if (type(inp) != str) or not os.path.isdir(inp):
        processSingleFile(inp=inp,outp=out,**args)
    else:
        batchProcess(inp=inp,outp=out,**args)
    
    return True

if __name__ == '__main__':
    try:
        if not main():sys.exit(1)
    except Exception as x:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    