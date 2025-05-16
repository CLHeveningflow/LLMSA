from assistant import Assistant
from tools import TraceSlice, ParseBugReport
from llm import LLMModel
import os,sys
import json
import argparse

base_prompt = """你是一个代码分析专家, 你的任务是根据用户提供的代码缺陷报告完成2个任务:
1. 分析给定的代码片段和缺陷报告, 判断该缺陷报告是正报（即存在缺陷）还是误报（报告与实际代码逻辑不符）。用户给出的缺陷代码片段会以'// trace'来标明预期的执行路径。示例如下：
int fun(int *ptr) {    // trace 0: 变量ptr传入函数
    free(ptr);  // trace 1: freepath: 变量ptr被用作参数
    int res = *ptr;  // trace 2: usepath: 读取变量ptr的值
}
2. 请**只**使用 JS0N 格式返回结果, **不要**包含任何其他解释性文字或 Markdowm 代码块标记, 输出结果包含Result和Reason两部分。
Result代表分析结果, 如果根据trace执行的代码为正报, 回答 True, 误报则回答 False。
Reason代表结论原因, 如果满足提到的缺陷, 描述代码的逻辑, 包括缺陷产生的原因以及该缺陷可能如何影响程序的执行；如果不满足提到的缺陷, 说明理由, 解释为什么该缺陷报告不成立（例如数据流不可行、缺陷满足的条件实际情况下不会发生等）。
{
    "Result": True,
    "Reason": "变量ptr 在'trace 1'被传入函数, 在'trace 2'进行了释放, 并在'trace 3'进行了解引用, 缺陷路径成立"
}
"""

def parse_arguments():
    parser = argparse.ArgumentParser(description="parameters:")
    parser.add_argument('-t', type=str, choices=['assistant', 'prompt'], help='mode: assistant or prompt')
    parser.add_argument('-c', type=str, help='directory of source code.')
    parser.add_argument('-s', type=str, help='dircetory of source code summary')
    parser.add_argument('-b', type=str, help='directory of defect type and info')
    parser.add_argument('-x', type=str, help='directory of result xml')
    parser.add_argument('-id', type=str, help='defect id')
    return parser.parse_args()
    
if __name__ == '__main__':
    args = parse_arguments()
    if args.t == 'assistant':
        current_file_path = os.path.dirname(__file__)
        weakness = {}
        with open('rules.json', 'r', encoding='utf-8') as file:
            weakness = json.load(file)
        model = LLMModel.get_openai_model_info("Aliyun_QwQ32B")
        assistant = Assistant.BasicAssistant(llm_openai_model=model, prompts_path=[current_file_path + '/prompts/analysis.txt'], 
                                        bug_report=current_file_path + '/testcase/saga-result-ampm/bt1.axf_db19b7e9.bc.xml', weakness_des=weakness)
        assistant.analysis_all(current_file_path + "/testcase/saga-result-ampm/ampm/", '/Users/eveningflow/LLMSA/merged_parse.json')
    elif args.t == 'prompt':
        prompt = base_prompt
        defect_type = args.b
        defect_description = ""
        bug_report_file = args.x        #xml file
        bug_id = args.id                #id
        function_summary = args.s       #'/Users/eveningflow/LLMSA/merged_parse.json'
        source_code_dirc = args.c       #current_file_path + "/testcase/saga-result-ampm/ampm/"
        data = TraceSlice.read_json_to_dict(function_summary)
        bug_info = ParseBugReport.parse_bug_info_by_id(bug_report_file, bug_id)
        trace_nodes = TraceSlice.getTraceFunFromBugInfo(bug_info=bug_info, source_dirc=source_code_dirc)
        code = TraceSlice.get_slice_code(data, trace_nodes)
        prompt_analysis = str(f'待分析的缺陷类型为: {defect_type}, 代码片段中, 假定跟着注释 "// trace" 的代码行是程序的实际执行流。代码片段如下:\n{code}')
        prompt += prompt_analysis
        print(prompt)
    else:
        print("Error: parameter -t must be 'assistant' or 'prompt'.")


