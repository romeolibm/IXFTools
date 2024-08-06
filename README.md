# IXFTools
A python script to parse IBM DB2 IFX format to inspect and convert to csv or other formats

#ATENTION! The current logic uses the default encoding for all data. 
This means that if your .ixf source fiels were created by a database with a different encoding the data conversion may
output wrong data fer certain column types that requires decoding/encoding.
The current version of the software is not fully tested on all encodings.
Please check if your data is correct before using the tool in production.
If you have trouble with the encoding then please fel free to modify the logic as you find fit.

# Command syntax
```
 IXFTols <name-value-parameter-list>
```

Parameters:
* cmd - command, optional, values (info,convert) default info
* in  - input entity, can be '-' for stdin (default) or a path to an .ixf file or folder containing .ixf files (when batch processing is done)
* out - output entity, can be '-' for stdout (default) or a path to a file or folder where the converted files will be stored
* outfmt - output format, can be csv or json default csv
* outputLobStrategy - what to do with the lob data, by default is 'detached' where each lob is written to a single file (this is default and only one supprted in this version)
* fromRow - if provided allows for skipping a number of rows before start processing
* maxRows - if provided can help limit the number of rows processed 
* trace - y|n if y then additional information about ixf records will be output on stderr

# LOB Handling
 By default lobs are written in files who's names and extenssions are determined from the table(file) name, column name and row number, and the extension from the lob type, .xml for xml objects .txt for CLOBs and .bin for all other lobs. 
  If you need to name the files in your own way please override the method getExternalLobIdentifier(self,cidx) or more comprehensive handleLobObject(self,cidx) on any of the parser classes IXFParser, IXFParserWriteCsv or IXFParserWriteJSON.

# Learning from test defintions and outcomes
I've commited in the repository a number of tests (minimal) that can be used to learn how the tool works.
To check each test, search for the test executor shell file called exec_test.sh under subfolders of the 'src/test' folder.
The folder hosting the exec_test.sh contains also cmd.out, the output of the command on stdout&stderr.
The converted files are in testOutput or in the same folder as exec_test.sh.
The input files (.ixf and lobs) are in ../inst folders from the exec_test.sh folder

# Known issues
1. Please see the encoding warning at the top of this doc

# Usage examples
## get help on accepted parameters
```
IXFTools.py

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
          supported in this version)
    fromRow - if provided allows for skipping a number of rows before start processing
    maxRows - if provided can help limit the number of rows processed 
    columns - a comma separated list of numbers (column index 1 based) or column names
              default None meaning all columns are output, if a list exists then only the
              provided column/col-index will be output when converting
    filter  - a list of constants to be used to filter rows or a path to a python module
              that has to provide a function called 'acceptrow' accepting a single parameter
              the row to be filtered and returns True if the row is to be 
              accepted for processing or False if not
    trace - y|n if y then additional information about ixf records will be output on stderr
```
## Basic IXF to CSV conversion using colum selection, row filtering by python logic fromRow and maxRows
```
echo Revealing the test code and filter code > /dev/null
cat test/syscat_exports/cmd_rowcol_filter/exec_test.sh
#!/bin/bash
../../../src/IXFTools.py \
 cmd=convert \
 in=../inst/syscat.tables.ixf \
 out=. \
 fromRow=1 \
 maxRows=10 \
 trace=n \
 columns=1,2,6,5 \
 filter=./myrowfilter.py \
 > cmd.out 2> cmd.err

cat test/syscat_exports/cmd_rowcol_filter/myrowfilter.py
def rowfilter(row):
  return row[1] == 'SYSVIEWS'

echo Executing the test > /dev/null
bash ./test/syscat_exports/cmd_rowcol_filter/exec_test.sh

echo Revealign produced output > /dev/null
cat ./test/syscat_exports/cmd_rowcol_filter/cmd.err
Start processing with arguments:
cmd = 'convert'
outfmt = 'csv'
lobFolder = '../inst'
outputEncoding = None
ouputLobStrategy = 'detached'
trace = False
fromRow = '1'
maxRows = '10'
columns = '1,2,6,5'
filter = './myrowfilter.py'
in = '../inst/syscat.tables.ixf'
out = '.'
Writing to file: /Users/romeolupascu/github/romeolibm/IXFTools/test/syscat_exports/cmd_rowcol_filter/syscat.tables.csv
Using row filter from file: <function rowfilter at 0x10461ee50>
Output= <_io.TextIOWrapper name='/Users/romeolupascu/github/romeolibm/IXFTools/test/syscat_exports/cmd_rowcol_filter/syscat.tables.csv' mode='wt' encoding='UTF-8'>
Start processing input from: ../inst/syscat.tables.ixf 
 using parser: <__main__.IXFParserWriteCsv object at 0x10461f460>
Writing data to: /Users/romeolupascu/github/romeolibm/IXFTools/test/syscat_exports/cmd_rowcol_filter/syscat.tables.csv
Reading from: ../inst/syscat.tables.ixf
Using column filter: [1, 2, 6, 5]
Table   Name: syscattables
Column count: 85
Lobs    size: 0
Lob    count: 0
Row    count: 10
Row filtered: 9
Processing time(sec): 0.0024340152740478516

cat ./test/syscat_exports/cmd_rowcol_filter/
TABSCHEMA,TABNAME,STATUS,TYPE
VARCHAR,VARCHAR,CHAR,CHAR
SYSIBM  ,SYSVIEWS,N,T

```

## Basic use case: extract information from a .ixf (table structure, row count, etc) no conversion executed in the PWD
```
IXFTools.py info 
Start processing with arguments: {'cmd': 'info', 'outfmt': 'csv', 'lobFolder': '.', 'outputEncoding': None, 'ouputLobStrategy': 'detached', 'trace': False, 'fromRow': None, 'maxRows': None, 'in': '.', 'out': None}
Start processing folder: .
Start processing input from: ./blobs_ixf_default.ixf 
 using parser: <__main__.IXFParserGetFileInfo object at 0x1031053d0>
Reading from: ./blobs_ixf_default.ixf

IXFHeader:
{'dbcodepage': '01200',
 'headingRowcount': (6,),
 'ixfid': 'IXF',
 'product': 'DB2    02.00',
 'sbcodepage': '01208',
 'version': '0002',
 'writtenDate': '20240208',
 'writtenTime': '112316'}
A-Records:
[{'IXFACTYP': 'A',
  'IXFADATE': '20240208',
  'IXFASLCA': b'\x00\x00SQLCA   \x88\x00\x00\x00Pm\x00\x00\x01\x002\x00\x00\x00'
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              b'\x00\x00\x00\x00\x00\x00SQLUEIWBm\x00\x15\x80\x00\x00'
              b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              b'\x00\x00\x00\x00\x00\x00W             ',
  'IXFATIME': '112316'},
 {'IXFACACH': '0000000020',
  'IXFACOLN': '000000',
  'IXFACTYP': 'S',
  'IXFACYCL': 'N',
  'IXFADATE': '20240208',
  'IXFAINCR': '001                              ',
  'IXFAITYP': 'Y',
  'IXFAMAXV': '002147483647                     ',
  'IXFAMINV': '001                              ',
  'IXFAORDR': 'N',
  'IXFARMRK': '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
  'IXFARMRL': '000',
  'IXFASTRT': '001                              ',
  'IXFATIME': '112316'},
 {'IXFACTYP': 'E', 'IXFADATE': '20240208', 'IXFATIME': '112316'}]
TableDescriptor:
{'colRecordCount': 4,
 'columns': [{'cid': 1,
              'colDataClass': 'R',
              'colno': 0,
              'data_len': 0,
              'dbcodepage': None,
              'defaultValue': '',
              'description': None,
              'dimensionSizes': None,
              'hasdefault': 'N',
              'lob_len': 0,
              'name': 'LOBNO',
              'nullable': 'N',
              'numDimensions': 0,
              'pkpos': '01',
              'pos': 1,
              'refType': '0',
              'sbcodepage': None,
              'selected': 'Y',
              'type': '496',
              'typeName': 'INTEGER',
              'udt': ''},
             {'cid': 1,
              'colDataClass': 'R',
              'colno': 1,
              'data_len': 32700,
              'dbcodepage': None,
              'defaultValue': '',
              'description': None,
              'dimensionSizes': None,
              'hasdefault': 'N',
              'lob_len': 1073741824,
              'name': 'TEXT',
              'nullable': 'Y',
              'numDimensions': 0,
              'pkpos': None,
              'pos': 5,
              'refType': '0',
              'sbcodepage': '01208',
              'selected': 'Y',
              'type': '408',
              'typeName': 'CLOB',
              'udt': ''},
             {'cid': 2,
              'colDataClass': 'R',
              'colno': 2,
              'data_len': 32700,
              'dbcodepage': None,
              'defaultValue': '',
              'description': None,
              'dimensionSizes': None,
              'hasdefault': 'N',
              'lob_len': 1073741824,
              'name': 'DATA',
              'nullable': 'Y',
              'numDimensions': 0,
              'pkpos': None,
              'pos': 1,
              'refType': '0',
              'sbcodepage': None,
              'selected': 'Y',
              'type': '404',
              'typeName': 'BLOB',
              'udt': ''},
             {'cid': 3,
              'colDataClass': 'R',
              'colno': 3,
              'data_len': 6226,
              'dbcodepage': None,
              'defaultValue': '',
              'description': None,
              'dimensionSizes': None,
              'hasdefault': 'N',
              'lob_len': 0,
              'name': 'XML_DATA',
              'nullable': 'Y',
              'numDimensions': 0,
              'pkpos': None,
              'pos': 1,
              'refType': '0',
              'sbcodepage': None,
              'selected': 'Y',
              'type': '988',
              'typeName': 'XML',
              'udt': ''}],
 'dataConvention': 'C',
 'dataFormat': 'M',
 'dataLocation': 'I',
 'dataSource': '',
 'description': None,
 'machineFormat': 'PC',
 'name': 'blobs_ixf_default',
 'pkName': None,
 'qualifier': ''}
Table   Name: blobs_ixf_default
Column count: 4
Lobs    size: 2254
Lob    count: 0
Row    count: 2
Processing time(sec): 0.0011022090911865234
End processing, file count: 1
```
# Convert an .ixf file to csv
```
IXFTools.py convert blobs_ixf_default.ixf
Start processing with arguments: {'cmd': 'convert', 'outfmt': 'csv', 'lobFolder': '', 'outputEncoding': None, 'ouputLobStrategy': 'detached', 'trace': False, 'fromRow': None, 'maxRows': None, 'in': 'blobs_ixf_default.ixf', 'out': 'blobs_ixf_default.csv'}
Writing to file: /Users/romeolupascu/github/romeolibm/IXFTools/test/blobs/ixf_export_test/ixf_export_default/inst/blobs_ixf_default.csv
Start processing input from: blobs_ixf_default.ixf 
 using parser: <__main__.IXFParserWriteCsv object at 0x1025f53d0>
Writing data to: /Users/romeolupascu/github/romeolibm/IXFTools/test/blobs/ixf_export_test/ixf_export_default/inst/blobs_ixf_default.csv
Reading from: blobs_ixf_default.ixf
Table   Name: blobs_ixf_default
Column count: 4
Lobs    size: 2254
Lob    count: 2
Row    count: 2
Processing time(sec): 0.00162506103515625

ll
...
total 192
-rw-r--r--  1 test  staff   2.2K  8 Feb 14:23 blobs_ixf_default.ixf.001.xml
-rw-r--r--  1 tesxt  staff    44K  8 Feb 14:23 blobs_ixf_default.ixf
-rw-r--r--  1 test  staff    58B  2 Aug 11:36 blobs_ixf_default_XML_DATA_0.xml
-rw-r--r--  1 test  staff   1.0K  2 Aug 11:36 blobs_ixf_default_XML_DATA_1.xml
-rw-r--r--  1 test  staff    35K  2 Aug 11:36 blobs_ixf_default.csv

```

# Software License
Apache 2 (see the LICENSE file in the root of the projedct)
