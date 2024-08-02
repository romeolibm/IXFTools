#!/bin/bash
../../../src/IXFTools.py \
 cmd=convert \
 in=../inst/syscat.tables.ixf \
 out=. \
 trace=y \
 > cmd.out 2>&1
