#!/bin/bash
../../../src/IXFTools.py \
 cmd=convert \
 in=../inst/syscat.tables.ixf \
 out=. \
 trace=n \
 > cmd.out 2>&1
