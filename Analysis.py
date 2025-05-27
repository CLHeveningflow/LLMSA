from tools import TraceSlice, ParseBugReport
import os
import sys
import json
import argparse
import logging

current_file_path = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename='llmsa.log', 
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S', 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="parameters:")
#    parser.add_argument('-t', type=str, choices=['assistant', 'prompt'], help='mode: assistant or prompt')
    parser.add_argument('-c', type=str, help='directory of source code.')
    parser.add_argument('-s', type=str, help='dircetory of source code summary')
    parser.add_argument('-b', type=str, help='directory of defect type and info')
    parser.add_argument('-x', type=str, help='directory of result xml')
    parser.add_argument('-id', type=str, help='defect id')
    parser.add_argument('-prompt', type=str, help='directory of prompts')
    return parser.parse_args()


def read_prompt_config_value(file_path, key):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        logging.info(f"文件 {file_path} 不存在, 将采用默认提示词")
        return None
    try:
        # 打开并读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        
        # 读取指定键的值
        if key in config:
            return config[key]
        else:
            # print(f"键 {key} 不存在于配置文件中")
            return 'analysis_all.txt'
    except json.JSONDecodeError as e:
        logging.info(f"读取 JSON 文件时出错: {e}, 将采用默认提示词")
        return None
    except Exception as e:
        logging.info(f"读取文件时出错: {e}, 将采用默认提示词")
        return None

if __name__ == '__main__':
    args = parse_arguments()
    if args.prompt:
        prompt_directory = args.prompt
    else:
        prompt_directory = current_file_path + '/prompt'

    if not os.path.exists(prompt_directory):
        logging.error(f"目录 {prompt_directory} 不存在")
        sys.exit(-1)

    defect_description = ""
    defect_type = args.b
    bug_report_file = args.x        #xml file
    bug_id = args.id                #id
    function_summary = args.s       #'/Users/eveningflow/LLMSA/merged_parse.json'
    source_code_dirc = args.c       #current_file_path + "/testcase/saga-result-ampm/ampm/"

    if defect_type is None or bug_report_file is None or bug_id is None or function_summary is None or source_code_dirc is None:
        logging.error("One or more required arguments are missing.")
        sys.exit(-1)

    prompt_file = read_prompt_config_value(prompt_directory + '/config.json', defect_type)
    if prompt_file is None:
        prompt_file = prompt_directory + '/analysis_all.txt'
    else:
        prompt_file = prompt_directory + '/' + prompt_file

    try:
        with open(prompt_file, 'r', encoding='utf-8') as prompt_stream:
            prompt = prompt_stream.read()
    except FileNotFoundError:
        logging.error(f"文件 {file_path} 不存在")
        sys.exit(-1)
    except Exception as e:
        logging.error(f"读取文件时出错: {e}")
        sys.exit(-1)

    data = TraceSlice.read_json_to_dict(function_summary)
    bug_info = ParseBugReport.parse_bug_info_by_id(bug_report_file, bug_id)
    trace_nodes = TraceSlice.getTraceFunFromBugInfo(bug_info=bug_info, source_dirc=source_code_dirc)
    code = TraceSlice.get_slice_code(data, trace_nodes)
    prompt_analysis = str(f'待分析的信息如下:缺陷类型为: {defect_type}, 代码片段中, 假定跟着注释 "// trace" 的代码行是程序的实际执行流。代码片段如下:\n{code}')
    prompt += '\n' + prompt_analysis
    print(prompt)
    sys.exit(0)

#python ./Analysis.py 
#-c E:/LLMSA/LLMSA/testcase/saga-result-ampm/ampm/ -s E:/LLMSA/LLMSA/merged_parse.json -b 空指针解引用 -x E:/LLMSA/LLMSA/testcase/saga-result-ampm/bt1.axf_db19b7e9.bc.xml -id 4769f974799ba00c8c73591c6c6e1c72
