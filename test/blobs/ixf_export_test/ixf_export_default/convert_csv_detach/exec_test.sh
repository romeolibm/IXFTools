#!/bin/bash
ACTION="../../../../../src/IXFTools.py"
$ACTION cmd=convert in=../inst/blobs_ixf_default.ixf out=testOutput trace=y ouputLobStrategy=detached > cmd.out 2>&1
