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
  If you need to name the files in your own way please override the method self.getExternalLobIdentifier(self,cidx) or  more comprehensive handleLobObject(self,cidx) on any of the parser classes IXFParser, IXFParserWriteCsv or IXFParserWriteJSON.

# Learning from test defintions and outcomes
I've commited in the repository a number of tests (minimal) that can be used to learn how the tool works.
To check each test, search for the test executor shell file called exec_test.sh under subfolders of the 'src/test' folder.
The folder hosting the exec_test.sh contains also cmd.out, the output of the command on stdout&stderr.
The converted files are in testOutput or in the same folder as exec_test.sh.
The input files (.ixf and lobs) are in ../inst folders from the exec_test.sh folder

# Software License
Apache 2 (see the LICENSE file in the root of the projedct)
