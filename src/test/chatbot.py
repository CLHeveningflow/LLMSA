from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from llm.LLMModel import get_openai_model_info

# 定义消息类型
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 创建状态图
graph_builder = StateGraph(State)

llm = ChatOpenAI(**get_openai_model_info("Aliyun_Qwen"))

def chatbot(state: State):
    return {"messages" : [llm.invoke(state["messages"])]}

# 添加开始节点
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


#stream_graph_updates("hello")
while True:
    try:
        user_input = input("User: ")
        if(user_input.lower() in ["quit", "exit", "q"]):
            print("Goodbye")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break