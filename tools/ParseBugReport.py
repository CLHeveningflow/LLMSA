import xml.etree.ElementTree as ET
from .DetectInfo import Bug_Info, Trace_Node

def parse_bug_info(bug) -> Bug_Info:
    # 获取Bug的唯一标识符
    bug_id = bug.get('id')
    # 查找Info节点
    info = bug.find('Info')
    # 获取Bug所在的文件路径
    file_path = info.get('file')
    # 获取Bug所在的行号
    line = info.get('line')
    # 获取Bug所在的列号
    column = info.get('column')
    
    # 获取规则信息
    rule = bug.find('Rule')
    weak = rule.get('weak')
    level = bug.find('Level').text
    info = []
    
    sinkfun = bug.find('SinkFun')
    if sinkfun is None:
        sink_start_line, sink_end_line = -1, -1
    else:
        sink_start_line = sinkfun.get('line')
        sink_end_line = sinkfun.get('endline')
        sink_start_line = -1 if sink_start_line is None else int(sink_start_line)
        sink_end_line = -1 if sink_end_line is None else int(sink_end_line)
    
    # 获取跟踪信息
    traceNode = bug.find('TraceInfos').find('TraceNode')
    for info_node in traceNode.findall('.//Info'):
        info_file = info_node.get('file')
        info_line = info_node.get('line')
        info_fun = info_node.get('type')
        info_text = info_node.find('Key').text.strip()
        info_inter = True if info_node.get('edge') == 'call' else False
        info.append(Trace_Node(file=info_file, line=int(info_line), fun=info_fun, info=info_text, inter=info_inter))
    bug_info = Bug_Info(id=bug_id, file_path=file_path, sink_start_line=sink_start_line, sink_end_line=sink_end_line, weak=weak, info=info)
    return bug_info

def parse_bug_info_onetrace(xml_file) -> list[Bug_Info]:
    # 解析XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()
    bug_infos = []
    # 查找所有Bug节点
    for bug in root.findall('.//Bug'):
        bug_info = parse_bug_info(bug)
        bug_infos.append(bug_info)
    return bug_infos

def parse_bug_info_by_id(xml_file, bug_id) -> Bug_Info:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    bugs = root.findall('.//Bug')
    for bug in bugs:
        if bug.get('id') == bug_id:
            return parse_bug_info(bug)
    return None