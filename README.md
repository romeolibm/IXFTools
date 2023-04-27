# IXFTools
A python script to parse IBM DB2 IFX format to inspect and convert to csv or other formats

# Command syntax

```
IXFTools.py cmd <ixf-file.ixf> [output-file.csv] [trace=y]
```

Where cmd can be 'info' or 'csv'.

Use trace if you want to check the IXF record structures the information will be dumped to the stderr.

# Just wnat to know what is in this IXF file my.ixf

```
IXFTools.py info my.ixf
```

# Dump the structure of this IXF file my.ixf

```
IXFTools.py info my.ixf trace=y
```

# Semi test

A set of three exec patterns already executed can be found in the test folder.