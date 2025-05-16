import json
import sys
import argparse
import os
import subprocess
def parse_text(text):
    lines = text.split('\n')
    return parse_lines(lines, 0)

def parse_lines(lines, depth):
    result = {}
    current_key = None
    current_value = {}

    while lines:
        line = lines.pop(0)
        if not line:
            continue
        if line.startswith('---'):
            continue
        if line.startswith(' ' * depth):
            line = line.strip()
            parts = line.rsplit(':', 1)
            if len(parts) == 2 and parts[1] != "":
                key = parts[0].strip().strip('\"')
                value = parts[1].strip().strip('\"')
                current_key = key
                current_value = value
                if current_key is not None:
                    result[current_key] = current_value
                current_value = {}
            else:
                new_depth = depth
                current_key_list = parts[0].strip()
                if current_key_list.startswith('-'):
                    current_key_list = parts[0].strip().split('-', 1)[1]
                    new_depth += 2
                current_key_list = current_key_list.strip().strip('\"')
                current_key = current_key_list.strip().strip('\"')
                current_key = current_key_list
                parse_line = parse_lines(lines, new_depth + 2)
                if parse_line:
                    result[current_key] = parse_line
        else:
            lines.insert(0, line)
            break
    return result
def run_doxyparse(dir , output, exec):
    try:
        # 调用 doxyparse . 命令
        output_file = "parse.txt"
        if output:
            output_file = output
        file_f = open(output_file, 'w')
        result = subprocess.run([exec, dir], cwd=os.getcwd(),stdout=file_f, text=True, check=True)
        
        # 打印命令的错误输出（如果有）
        if result.stderr:
            print("Command error output:")
            print(result.stderr)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error output: {e.stderr}")


def parse_convert(parse_file, output):
    text = open(parse_file, 'r').read()
    data = parse_text(text)
    file_f = open(output, 'w')
    json.dump(data, file_f, indent=4)


def merge_convert(parse_file, merge_file, output):
    text = open(parse_file, 'r').read()
    parse_data = parse_text(text)
    merge_text = open(merge_file, 'r').read()
    merge_data = parse_text(merge_text)
    
    # result = {**merge_data, **parse_data}

    
    for key, file in parse_data.items():
        for file_name, file_info in file.items():
            file_defines = file_info['defines']
            merge_defines = None
            if 'defines' in merge_data.get(key, {}).get(file_name, {}):
                merge_defines = merge_data[key][file_name]['defines']
            if file_defines is not None and merge_defines is not None:
                for var_name, var_info in merge_defines.items():
                    if var_name not in file_defines:
                        file_defines[var_name] = var_info
        
    with open(output, 'w') as f_merged:
        json.dump(parse_data, f_merged, indent=4)

if __name__ == "__main__":
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="prase covert")

    # 添加参数
    parser.add_argument('--data', type=str, help='input data file')
    parser.add_argument('--dir', type=str, help='parse dir')                #/Users/eveningflow/LLMSA/testcase/saga-result-ampm/ampm/__src__code__
    parser.add_argument('-o','--output', type=str, help='parse output')
    parser.add_argument('--pt', type=str, help='doxygen parser tool dir')       #/Users/eveningflow/doxygen/build/bin/doxyparse
    parser.add_argument('--npt', type=str, help='doxygen no pre parser tool dir')  #/Users/eveningflow/doxygen/build/bin/doxyparse-no-pre
    # 解析命令行参数
    args = parser.parse_args()
    output = 'parse.json'
    if args.output:
        output = args.output
    if args.data:
        parse_convert(args.data, output)
    elif args.dir:
        parse_data = "parse.txt"
        run_doxyparse(args.dir, parse_data, args.pt)
        parse_data1 = "parsefun.txt"
        run_doxyparse(args.dir, parse_data1, args.npt)
        merge_convert(parse_data, parse_data1, 'merged_parse.json')