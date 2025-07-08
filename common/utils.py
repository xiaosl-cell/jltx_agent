import os
import sys
import shutil
import re

def exit_program():
    """退出程序"""
    print("感谢使用游戏Agent系统，再见！")
    sys.exit(0)

def clear_screen():
    """清除屏幕"""
    os.system('cls' if os.name == 'nt' else 'clear')

# 控制台颜色常量
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ANSI颜色代码正则表达式
ANSI_PATTERN = re.compile(r'\033\[[0-9;]*m')

def get_display_width(text):
    """获取字符串在终端中的显示宽度，考虑中文字符和ANSI颜色代码"""
    # 移除ANSI颜色代码
    text_without_ansi = ANSI_PATTERN.sub('', text)
    
    # 计算宽度：ASCII字符占1个单位，中文字符占2个单位
    width = 0
    for char in text_without_ansi:
        if ord(char) > 127:  # 简单判断非ASCII字符（包括中文）
            width += 2
        else:
            width += 1
    return width

def center_with_display_width(text, width):
    """根据显示宽度居中文本"""
    display_width = get_display_width(text)
    if display_width >= width:
        return text
    
    # 计算需要添加的空格数
    padding = width - display_width
    left_padding = padding // 2
    right_padding = padding - left_padding
    
    return ' ' * left_padding + text + ' ' * right_padding

def print_centered(text, width=None):
    """打印居中文本，考虑中文字符"""
    if width is None:
        terminal_size = shutil.get_terminal_size()
        width = terminal_size.columns
    
    centered_text = center_with_display_width(text, width)
    print(centered_text)

def print_box(text_list, title=None, width=None):
    """打印带边框的文本框，只有上下边框"""
    if width is None:
        terminal_size = shutil.get_terminal_size()
        width = min(terminal_size.columns, 80)  # 限制最大宽度为80
    
    # 打印顶部边框
    print(f"{Colors.CYAN}{'═' * width}{Colors.ENDC}")
    
    # 打印标题
    if title:
        title_with_color = f"{Colors.YELLOW}{Colors.BOLD}{title}{Colors.ENDC}"
        title_display_width = get_display_width(title)  # 计算标题实际显示宽度
        padding = width - title_display_width
        left_padding = padding // 2
        right_padding = padding - left_padding
        title_line = ' ' * left_padding + title_with_color + ' ' * right_padding
        print(title_line)
        print(f"{Colors.CYAN}{'-' * width}{Colors.ENDC}")
    
    # 打印内容
    for line in text_list:
        line_display_width = get_display_width(line)  # 计算行实际显示宽度
        padding = width - line_display_width
        left_padding = padding // 2
        right_padding = padding - left_padding
        centered_line = ' ' * left_padding + line + ' ' * right_padding
        print(centered_line)
    
    # 打印底部边框
    print(f"{Colors.CYAN}{'═' * width}{Colors.ENDC}")

def print_menu_item(index, name, selected=False):
    """打印菜单项"""
    if selected:
        return f"{Colors.GREEN}{Colors.BOLD}【{index}】{name}{Colors.ENDC}"
    else:
        return f"{Colors.BLUE}【{index}】{name}{Colors.ENDC}"