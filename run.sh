./dist/parser_convert/parser_convert.exe --dir E:/LLMSA/LLMSA/testcase/saga-result-ampm/ampm/__src__code__ --pt E:/LLMSA/doxyparse-win/bin/doxyparse.exe --npt E:/LLMSA/doxyparse-win/bin/doxyparse-no-pre.exe -o merged_parse.json
./dist/Analysis/Analysis.exe -c E:/LLMSA/LLMSA/testcase/saga-result-ampm/ampm/ -s E:/LLMSA/LLMSA/merged_parse.json -b 空指针解引用 -x E:/LLMSA/LLMSA/testcase/saga-result-ampm/bt1.axf_db19b7e9.bc.xml -id 4769f974799ba00c8c73591c6c6e1c72



parser_convert.exe --dir [path_to_source_code] --pt [path_to_doxyparse] --npt [path_to_doxyparse_no_pre] -o [output_file]
Analysis.exe -c [path_to_source_code] -s [parser_convert_output] -b [checker_name] -x [codesense_output_xml] -id [bug_id]