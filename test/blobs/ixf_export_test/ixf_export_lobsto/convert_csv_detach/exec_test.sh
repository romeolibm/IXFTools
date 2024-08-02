#!/bin/bash
ACTION="../../../../../src/IXFTools.py"
$ACTION cmd=convert in=../inst/blobs_ixf_lobs_to_blob_dir.ixf out=. trace=n ouputLobStrategy=detached > cmd.out 2>&1
