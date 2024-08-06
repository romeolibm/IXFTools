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
