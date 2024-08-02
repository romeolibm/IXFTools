DROP TABLE
RLT.BLOBS
;
CREATE TABLE 
RLT.BLOBS
(
  lobno integer generated always as identity primary key,
  text clob(1G),
  data blob(1G),
  xml_data xml
);
truncate table RLT.BLOBS immediate
;
insert into RLT.BLOBS 
(text,data,xml_data) 
values 
 ('text sample',BX'000102030405','<re><x>123</x></re>')
,(repeat('text sample,',1000),
  repeat(BX'000102030405',1000),
  '<re>'||repeat('<x>123</x>',100)||'</re>'
 )
,(repeat('text sample2,',1000),
  repeat(BX'0001020304050607',1000),
  '<re>'||repeat('<x>1234</x>',100)||'</re>'
)
;

select * from RLT.BLOBS with ur
;

-- db2 "export to blobs_ixf_default.ixf of ixf select * from rlt.blobs"
-- mkdir blob_dir
-- db2 "export to blobs_ixf_lobs_to_blob_dir.ixf of ixf lobs to blob_dir xml to blob_dir select * from rlt.blobs"
-- db2 "export to blobs_ixf_lobfile.ixf of ixf lobfile blob_file xmlfile xml_file select * from rlt.blobs"
