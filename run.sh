python /Users/eveningflow/LLMSA/LLMSA/parser_convert.py --dir /Users/eveningflow/LLMSA/LLMSA/testcase/saga-result-ampm --pt /Users/eveningflow/LLMSA/doxygen/build/bin/doxyparse --npt /Users/eveningflow/LLMSA/doxygen/build/bin/doxyparse-no-pre -o merged_parse.json
python /Users/eveningflow/LLMSA/LLMSA/Analysis.py -c /Users/eveningflow/LLMSA/LLMSA/testcase/saga-result-ampm/ampm/__src__code__ -s /Users/eveningflow/LLMSA/LLMSA/merged_parse.json -b 函数参数未使用 -x /Users/eveningflow/LLMSA/LLMSA/testcase/saga-result-ampm/result.xml -id 8550e24e35e9fdb80711fd9095703766 -prompt /Users/eveningflow/LLMSA/LLMSA/prompts

# parser_convert.exe --dir [path_to_source_code] --pt [path_to_doxyparse] --npt [path_to_doxyparse_no_pre] -o [output_file]
# Analysis.exe -c [path_to_source_code] -s [parser_convert_output] -b [checker_name] -x [codesense_output_xml] -id [bug_id] -prompt [path_to_prompt]

#./dist/parser_convert/parser_convert --dir /home/llvm/LLMSA/testcase/saga-result-ampm/ampm/__src__code__ --pt /home/llvm/doxygen/build/bin/doxyparse --npt /home/llvm/doxygen/build/bin/doxyparse-no-pre -o ampm.json
#./dist/Analysis/Analysis -c /home/llvm/LLMSA/testcase/saga-result-ampm/ampm/__src__code__ -s /home/llvm/LLMSA/ampm.json -b 在对指针NULL检查前或后进行指针解引用 -x /home/llvm/LLMSA/testcase/saga-result-ampm/bt1.axf_db19b7e9.bc.xml -id 4692fcbebb7a7a09f684eb28f30d1ec5 -prompt /home/llvm/LLMSA/prompts


