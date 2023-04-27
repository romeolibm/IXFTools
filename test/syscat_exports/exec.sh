#!/bin/bash
../../src/IXFTools.py > noparams.out 2>&1
../../src/IXFTools.py info syscat.tables.ixf trace=y > syscat.tables.ixf.dump.out 2>&1
../../src/IXFTools.py csv syscat.tables.ixf syscat.tables.csv > csv.out 2>&1
