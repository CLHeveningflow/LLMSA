import xml.etree.ElementTree as ET
from .DetectInfo import Bug_Info, Slice
import json

def getSourceCodeFromLine(info_slice: Slice, line: int, max_line_pre_func: int) -> str:
    source = ""
    if info_slice == None:
        print("Error: info_slice is None.")
        return ""
    
    try:
        with open(info_slice.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            start_index = max(info_slice.start_line - 1, line - max_line_pre_func / 2)
            end_index = min(len(lines), line + max_line_pre_func / 2)
            source_code = ''.join(lines[start_index:end_index])
            source += source_code
    except FileNotFoundError:
        print(f"Error: File not found - {info_slice.file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
        
    return source

def getSourceCodeFromSlice(info_slice: Slice) -> list[str]:
    source = []
    if info_slice == None:
        print("Error: info_slice is None.")
        return []
    
    try:
        with open(info_slice.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            source_code = lines[info_slice.start_line-1 : info_slice.end_line]
            return source_code
    except FileNotFoundError:
        print(f"Error: File not found - {info_slice.file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return source

def getSourceCodeFromSink(bug_info: Bug_Info, source_dirc: str) -> str:
    source = ''
    start_line, end_line = bug_info.sink_start_line, bug_info.sink_end_line # int(bug_info[0]), int(bug_info[1])
    file_path = getRealFilePath(bug_info.file_path, source_dirc)
    print(file_path, start_line, end_line)
    return getSourceCodeFromSlice(Slice(file_path=file_path, start_line=start_line, end_line=end_line))

def getRealFilePath(file_path: str, source_dirc: str) -> str:
    tree = ET.parse(source_dirc + '__cnf__/compiler_info.xml')
    root = tree.getroot()
    path = root.find(".//path").text
    path = '/'.join(path.replace('\\', '/').split('/')[:-1]) + '/'
    real_file_path = file_path.replace(path, source_dirc + "__src__code__/")
    return real_file_path

def getTraceFunFromBugInfo(bug_info: Bug_Info, source_dirc: str) -> list:
    trace_fun = []
    for traceNode in bug_info.info:
        file_path = traceNode.file
        real_file_path = getRealFilePath(file_path=file_path, source_dirc=source_dirc)
        trace_fun.append((real_file_path, traceNode.fun, traceNode.line, traceNode.info))
    return trace_fun

def read_json_to_dict(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def find_funcitions_in_file(data: dict, file_path: str, funcname: str)-> list:
    file_data = data[file_path][file_path.split('/')[-1]]["defines"].keys()
    functions = [key for key in file_data if key.startswith(funcname+'(')]
    return functions

def find_function_by_line(data: dict, file_path: str, line: int) -> Slice:
    file_data = data.get(file_path, {})
    if not file_data:
        return None
    
    for file, file_infos in file_data.items():
        for func_name, func_info in file_infos["defines"].items():
            if func_info.get('type') == 'function':
                start_line = int(func_info.get('line', 0))
                lines_of_code = int(func_info.get('lines_of_code', 1))
                end_line = start_line + lines_of_code - 1
                if start_line > 0:
                    start_line -= 1
                if start_line <= line <= end_line:
                    return Slice(file_path, start_line,end_line)
    return None


def get_slice_code(data, trace_nodes: list):
    code = ''
    slices = {}
    trace_cnt = 0
    for file_path, fun, line, info in trace_nodes:
        if fun == '@global':
            slice = Slice(file_path, line, line)
            source_list = getSourceCodeFromSlice(slice)
            code += ''.join(source_list).rstrip('\n') + f' // trace {trace_cnt}: {info}\n'
            trace_cnt += 1
        else:
            if (file_path, fun) in slices:
                slice_dict = slices[(file_path, fun)]
                index = line - slice_dict["slice"].start_line
                slice_dict["code"][index] = slice_dict["code"][index].rstrip('\n') + str(f' // trace {trace_cnt}: {info}\n')
                trace_cnt += 1
            else:
                slice = find_function_by_line(data, file_path, line)
                if slice is None:
                    print(f"Error: Could not find function in file {file_path} at line {line}", file=sys.stderr)
                    continue
                source_list = getSourceCodeFromSlice(slice)
                index = line - slice.start_line
                source_list[index] = source_list[index].rstrip('\n') +  str(f' // trace {trace_cnt}: {info}\n')
                
                slices[(file_path, fun)] = {"slice": slice, "code": source_list}
                trace_cnt += 1
    
    for file_path, fun in sorted(slices.keys()):
        slice_dict = slices[(file_path, fun)]
        source_code_with_trace = ''.join(slice_dict["code"])
        code += source_code_with_trace + '\n'

    return code