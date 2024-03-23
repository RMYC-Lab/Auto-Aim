from typing import Iterable, Union, Any, List


from .parameter import Parameter


PARSE_REGEX_BASE = r'^(?P<result>.+?)( seq (?P<seq>.+))?;\n?$'


SEQ_DEFAULT = "&@#DEFAULT#@&"


class CommandBuilder:
    """
    Command class
    命令类
    """
    def __init__(self, command: str, params: Union[Iterable[Parameter], None] = None,
                 seq: Union[str, None] = None):
        self.command: str = command
        self.params: Union[List[Parameter], None] = list(params) if params is not None else None
        self.seq: Union[str, None] = seq

    def check(self, params: Union[Iterable[Any], None]) -> bool:
        """
        Check parameters
        检查参数
        """
        if self.params is None:     # 无参数
            return True
        if params is None:
            return False
        params = list(params)
        if len(params) > len(self.params):  # 参数过多
            return False
        for i, param in enumerate(params):
            if not self.params[i].check(param):
                return False
        return True

    def build(self, params: Union[Iterable[Any], None] = None, seq: Union[str, None] = SEQ_DEFAULT) -> 'Command':
        """
        Build command
        构建命令
        """
        if not self.check(params):
            raise ValueError("Invalid parameters")
        return Command(self, params, seq)

    def format(self, params: Union[Iterable[Any], None] = None, seq: Union[str, None] = SEQ_DEFAULT) -> str:
        """
        Format parameters
        格式化参数
        """
        assert self.check(params), "Invalid parameters"
        param_str = f"{self.command}"
        if self.params is not None and params is not None:
            params = list(params)
            for i, param in enumerate(params):
                param_str += self.params[i].format(param)
        if seq is not None and seq != SEQ_DEFAULT:  # format 指定 seq
            param_str += f" seq {seq}"
        elif seq == SEQ_DEFAULT and self.seq is not None:
            param_str += f" seq {self.seq}"         # format 默认 seq
        # else:  # 无 seq
        return f"{param_str};"

    '''
    def parse(self, parse_str: str) -> Union[bool, 'Result']:
        """
        Parse command from string
        从字符串解析命令
        """
        regex = PARSE_REGEX_BASE.format(command=self.command)
        match = re.match(regex, parse_str)
        if match is None:
            return False
        result = match.group('result').strip()
        seq = match.group('seq')
        return Result(result, seq)
    '''


class Command:
    """
    Command class
    一种 params 持久化的命令类
    命令类
    """
    global_seq = 0

    def __init__(self, command_builder: CommandBuilder, params: Union[Iterable[Any], None] = None,
                 seq: Union[str, None] = SEQ_DEFAULT):
        assert command_builder.check(params), "Invalid parameters"
        self.command_builder: CommandBuilder = command_builder
        self.params: Union[List[Any], None] = list(params) if params is not None else None
        self.seq: Union[str, None] = seq

    def format(self, seq: Union[str, None] = SEQ_DEFAULT) -> tuple[str, Union[str, None]]:
        """
        Format command
        格式化命令
        """
        _seq: Union[str, None] = None
        if seq == SEQ_DEFAULT:
            # 使用持久化的 seq
            if self.seq == SEQ_DEFAULT:
                # 生成一个新的 seq
                _seq = str(Command.global_seq)
                Command.global_seq += 1
            elif self.seq is None:
                _seq = None  # 无 seq
            else:
                _seq = self.seq
        else:
            _seq = seq
        return self.command_builder.format(self.params, _seq), _seq
        # return self.command_builder.format(self.params, seq)


class Result:
    """
    Result class
    结果类
    """
    def __init__(self, result: str, seq: Union[str, None] = None):
        self.result = result
        self.seq = seq
