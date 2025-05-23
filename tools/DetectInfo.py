class Trace_Node:
    def __init__(self, file: str, line: int, fun: str, info: str, inter: bool):
        self.file = file
        self.line = line
        self.info = info
        self.fun = fun
        self.inter = inter

    def __str__(self):
        return f"File: {self.file}, Fun: {self.fun}, Line: {self.line}, Info: {self.info}, Inter-Call-Ret: {self.inter}"

    def print(self):
        print(self.__str__())

class Slice:
    def __init__(self, file_path: str, start_line: int, end_line: int):
        self.file_path = file_path
        self.start_line = start_line
        self.end_line = end_line

    def __str__(self):
        return f"FilePath: {self.file_path}, Start Line: {self.start_line}, End Line: {self.end_line}"
    
    def print(self):
        print(self.__str__())

class Bug_Info:
    def __init__(self, id: str, file_path: str, sink_start_line: int, sink_end_line: int, weak: str, info: list):
        self.id = id
        self.file_path = file_path
        self.sink_start_line = sink_start_line
        self.sink_end_line = sink_end_line
        self.weak = weak
        self.info = info
        
    def __str__(self):
        info_str = "\n".join([item.__str__() for item in self.info])
        return (f"Bug ID: {self.id}\n"
                f"File Path: {self.file_path}\n"
                f"Start Line: {self.sink_start_line}\n"
                f"End Line: {self.sink_end_line}\n"
                f"Weakness: {self.weak}\n"
                f"Info:\n{info_str}")

    def print(self):
        print(self.__str__())