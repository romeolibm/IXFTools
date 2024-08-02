# IXFTools
A python script to parse IBM DB2 IFX format to inspect and convert to csv or other formats

#ATENTION! The current logic uses the default encoding for all data. 
This means that if your .ixf source fiels were created by a database with a different encoding the data conversion may
output wrong data fer certain column types that requires decoding/encoding.
The current version of the software is not fully tested on all encodings.
Please check if your data is correct before using the tool in production.
If you have trouble with the encoding then please fel free to modify the logic as you find fit.

# Command syntax

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

