import os
from typing import List


def parse_args(args) -> list:
    """拆分指令参数为一个列表，并去除入口指令

    :param args: str 字符串
    """
    args: List[str] = args.strip().split()
    for i in range(len(args)):
        args[i].strip()
    args.pop(0)
    return args


def isstartswith(prefix: str, args) -> bool:
    """判断prefix是否以args中某元素开头"""
    if type(args) == str:
        args = [args]
    for arg in args:
        if prefix.startswith(arg):
            return True
    return False


def line_break(line, char_counts, tab_stop=4):
    ret = ''
    width = 0
    for index, c in enumerate(line):
        if len(c.encode('utf8')) == 3:
            if (char_counts == width + 1) and ('\u4e00' <= c <= '\u9fa5'):
                width = 2
                ret += '\n' + c
            elif c in '，。？！’“》】）；' and ret.endswith('\n'):
                ret = ret[:-1] + c + '\n'
            else:
                width += 2
                ret += c
        else:
            if c == '\t':
                space_c = tab_stop - width % tab_stop
                ret += ' ' * space_c
                width += space_c
            elif c == '\n':
                width = 0
                ret += c
            elif c in ',.?!\'")>]};' and ret.endswith('\n'):
                ret = ret[:-1] + c + '\n'
            else:
                width += 1
                ret += c
        if width >= char_counts:
            ret += '\n'
            width = 0
    ret.replace('\n\n', '\n')
    if ret.endswith('\n'):
        return ret
    return ret + '\n'


def app_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    print(app_path())
