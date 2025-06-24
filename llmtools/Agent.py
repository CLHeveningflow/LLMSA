from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os, sys, uuid
from tools import TraceSlice, ParseBugReport, DetectInfo


class BasicAssistant:
    SKIP_WEAKNESS = ['DANGERFUNC_POTENTIAL_S', 'PTR_FIXXEDADDR_PTR_S', 'REDUNDANT_GLOBAL_S', 'UNUSED_VAR_S',
                     'UNUSED_ARG_S', 'WEAK_RAND_S', 'SPECULATIVE_EXECUTION_DATA_LEAK_S', 'UNUSED_VALUE_S']
    
    def __init__(self, llm_openai_model, prompts_path, bug_report, weakness_des, **kwargs):
        self.prompts = None
        llm = ChatOpenAI(**llm_openai_model)
        
        self.WEAKNESS_DES = weakness_des
        
        self.get_prompts(prompts_path)
        
        def call_model_with_prompts(state: MessagesState):
            model = self.prompts | llm
            response = model.invoke(state["messages"])
            return {"messages": response}
        
        def call_model(state: MessagesState):
            response = llm.invoke(state["messages"])
            return {"messages": response}

        self.bug_infos = ParseBugReport.parse_bug_info_onetrace(bug_report)
        
        workflow = StateGraph(state_schema=MessagesState)
        
        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model_with_prompts)
        workflow.add_edge("model", END)
        
        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)
        
        thread_id = uuid.uuid4()
        self.config = {"configurable": {"thread_id": thread_id}}
        self.memory = [{"role": "system", "content": self.prompts}]

    def clean_messages(self):
        thread_id = uuid.uuid4()
        self.config = {"configurable": {"thread_id": thread_id}}

    def get_prompts(self, prompt_paths):
        prompts = ""
        for prompt_path in prompt_paths:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompts += f.read() + '\n\n'
        self.prompts = ChatPromptTemplate.from_messages(
            [
            ("system", prompts),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
    
    def send_message(self, message=None):
        res = None
        if message is not None:
            message = {"messages": message}
        
        for event in self.app.stream(message, config=self.config, stream_mode="values"):
            if "messages" in event:
                res = event["messages"][-1].content
        return res
    
    def analysis(self, defect_type, code):
        self.clean_messages()
        return self.send_message(
            f'代码片段分析的缺陷类型为: {defect_type}, 代码片段中，假定跟着注释 "// trace" 的代码行是程序的实际执行流。代码片段如下:\n{code}'
        )
        
    def analysis_all(self, source_dirc, function_summary, output_to_file=True):
        data = TraceSlice.read_json_to_dict(function_summary)
        max_line_pre_func = 100
        output_file = 'analysis_output.txt' if output_to_file else None
        
        bug_cnt = 0
        
        with open(output_file, 'w', encoding='utf-8') if output_to_file else open(os.devnull, 'w') as f:
            for bug_info in self.bug_infos:
                if bug_info.weak in self.SKIP_WEAKNESS:
                    continue
                bug_cnt += 1
                trace_nodes = TraceSlice.getTraceFunFromBugInfo(bug_info=bug_info, source_dirc=source_dirc)
                code = TraceSlice.get_slice_code(data, trace_nodes)
                    
                #print(bug_info, file=f)
                lines_of_code = len(code.split('\n'))
                if lines_of_code > 100:
                    print(f"Warning: TOO LONG!!!, lines of code is {lines_of_code}", file=f)
                
                print(bug_info.id, ': '.join(self.WEAKNESS_DES[bug_info.weak]))
                print(code)
                result = self.analysis(': '.join(self.WEAKNESS_DES[bug_info.weak]), code)
                
                print(result)
                print(result, file=f)
                
                while True:
                    n = input("请输入n以继续循环: ")
                    if n.lower() == 'n':
                        break
                    elif n.lower() == 'q':
                        return
                
        print(f"Bug Count: {bug_cnt}")