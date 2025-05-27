./dist/parser_convert/parser_convert --dir /home/llvm/LLMSA/testcase/testc --pt /home/llvm/doxygen/build/bin/doxyparse --npt /home/llvm/doxygen/build/bin/doxyparse-no-pre -o merged_parse.json
./dist/Analysis/Analysis -c /home/llvm/LLMSA/testcase/testc -s /home/llvm/LLMSA/merged_parse.json -b 空指针解引用 -x /home/llvm/LLMSA/testcase/testc/result.xml -id a6ea2d8985103227341aa9e6f9f4e343 -prompt /home/llvm/LLMSA/prompts


# parser_convert.exe --dir [path_to_source_code] --pt [path_to_doxyparse] --npt [path_to_doxyparse_no_pre] -o [output_file]
# Analysis.exe -c [path_to_source_code] -s [parser_convert_output] -b [checker_name] -x [codesense_output_xml] -id [bug_id] -prompt [path_to_prompt]

#./dist/parser_convert/parser_convert --dir /home/llvm/LLMSA/testcase/saga-result-ampm/ampm/__src__code__ --pt /home/llvm/doxygen/build/bin/doxyparse --npt /home/llvm/doxygen/build/bin/doxyparse-no-pre -o ampm.json
#./dist/Analysis/Analysis -c /home/llvm/LLMSA/testcase/saga-result-ampm/ampm/__src__code__ -s /home/llvm/LLMSA/ampm.json -b 在对指针NULL检查前或后进行指针解引用 -x /home/llvm/LLMSA/testcase/saga-result-ampm/bt1.axf_db19b7e9.bc.xml -id 4692fcbebb7a7a09f684eb28f30d1ec5 -prompt /home/llvm/LLMSA/prompts
