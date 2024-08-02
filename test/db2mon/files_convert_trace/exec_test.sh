#!/bin/bash

../../../src/IXFTools.py \
 cmd=convert \
 in=../db2mon_snap_hostname_db2inst1_DBNAME_TS/db_get_cfg.ixf \
 out=testOutput \
 ouputLobStrategy=detached \
> cmd1.out 2>&1

../../../src/IXFTools.py \
 cmd=convert \
 in=../db2mon_snap_hostname_db2inst1_DBNAME_TS/mon_get_pkg_cache_stmt.ixf \
 out=testOutput \
 ouputLobStrategy=detached \
> cmd2.out 2>&1

../../../src/IXFTools.py \
 cmd=convert \
 in=../db2mon_snap_hostname_db2inst1_DBNAME_TS/mon_get_table.ixf \
 out=testOutput \
 ouputLobStrategy=detached \
> cmd3.out 2>&1

../../../src/IXFTools.py \
 cmd=convert \
 in=../db2mon_snap_hostname_db2inst1_DBNAME_TS/syscat_tables.ixf \
 out=testOutput \
 ouputLobStrategy=detached \
> cmd4.out 2>&1
