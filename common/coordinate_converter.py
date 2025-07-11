#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
坐标转换工具
用于将相对于窗口截图的坐标转换为屏幕绝对坐标
"""

import win32gui
import win32api
import win32con
from typing import Tuple, Optional
from .gui_util import get_window_dpi_scale

class CoordinateConverter:
    """
    坐标转换工具类
    负责将相对于窗口截图的坐标转换为屏幕绝对坐标
    """
    
    def __init__(self, hwnd: int):
        """
        初始化坐标转换器
        
        Args:
            hwnd: 窗口句柄
        """
        self.hwnd = hwnd
        self.dpi_scale = get_window_dpi_scale(hwnd)
        self._update_window_info()
    
    def _update_window_info(self):
        """更新窗口信息"""
        try:
            # 获取窗口完整矩形区域（包括标题栏）
            self.window_rect = win32gui.GetWindowRect(self.hwnd)
            self.window_left, self.window_top, self.window_right, self.window_bottom = self.window_rect
            
            # 获取客户区矩形区域
            self.client_rect = win32gui.GetClientRect(self.hwnd)
            client_left, client_top, client_right, client_bottom = self.client_rect
            
            # 计算客户区在屏幕上的位置
            self.client_screen_pos = win32gui.ClientToScreen(self.hwnd, (0, 0))
            
            # 计算客户区尺寸
            self.client_width = client_right - client_left
            self.client_height = client_bottom - client_top
            
            # 计算窗口装饰（标题栏、边框）的偏移量
            self.title_bar_height = self.client_screen_pos[1] - self.window_top
            self.left_border_width = self.client_screen_pos[0] - self.window_left
            
            print(f"窗口信息更新:")
            print(f"  窗口位置: ({self.window_left}, {self.window_top}) - ({self.window_right}, {self.window_bottom})")
            print(f"  客户区尺寸: {self.client_width}x{self.client_height}")
            print(f"  客户区屏幕位置: {self.client_screen_pos}")
            print(f"  标题栏高度: {self.title_bar_height}")
            print(f"  左边框宽度: {self.left_border_width}")
            print(f"  DPI缩放: {self.dpi_scale}")
            
        except Exception as e:
            print(f"更新窗口信息失败: {e}")
            # 使用默认值
            self.window_rect = (0, 0, 800, 600)
            self.client_rect = (0, 0, 800, 600)
            self.client_screen_pos = (0, 0)
            self.client_width = 800
            self.client_height = 600
            self.title_bar_height = 0
            self.left_border_width = 0
    
    def image_to_screen_coords(self, image_x: int, image_y: int) -> Tuple[int, int]:
        """
        将相对于窗口截图的坐标转换为屏幕绝对坐标
        
        Args:
            image_x: 图像中的x坐标
            image_y: 图像中的y坐标
            
        Returns:
            屏幕绝对坐标 (screen_x, screen_y)
        """
        try:
            # 更新窗口信息（防止窗口移动）
            self._update_window_info()
            
            # 考虑DPI缩放：图像坐标需要除以DPI缩放比例
            real_x = image_x / self.dpi_scale
            real_y = image_y / self.dpi_scale
            
            # 转换为屏幕坐标
            screen_x = int(self.client_screen_pos[0] + real_x)
            screen_y = int(self.client_screen_pos[1] + real_y)
            
            print(f"坐标转换: 图像({image_x}, {image_y}) -> 屏幕({screen_x}, {screen_y})")
            
            return screen_x, screen_y
            
        except Exception as e:
            print(f"坐标转换失败: {e}")
            return image_x, image_y
    
    def screen_to_image_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """
        将屏幕绝对坐标转换为相对于窗口截图的坐标
        
        Args:
            screen_x: 屏幕绝对x坐标
            screen_y: 屏幕绝对y坐标
            
        Returns:
            图像相对坐标 (image_x, image_y)
        """
        try:
            # 更新窗口信息
            self._update_window_info()
            
            # 转换为相对于客户区的坐标
            relative_x = screen_x - self.client_screen_pos[0]
            relative_y = screen_y - self.client_screen_pos[1]
            
            # 考虑DPI缩放：相对坐标需要乘以DPI缩放比例
            image_x = int(relative_x * self.dpi_scale)
            image_y = int(relative_y * self.dpi_scale)
            
            print(f"逆向坐标转换: 屏幕({screen_x}, {screen_y}) -> 图像({image_x}, {image_y})")
            
            return image_x, image_y
            
        except Exception as e:
            print(f"逆向坐标转换失败: {e}")
            return screen_x, screen_y
    
    def is_point_in_window(self, screen_x: int, screen_y: int) -> bool:
        """
        检查屏幕坐标是否在窗口客户区内
        
        Args:
            screen_x: 屏幕x坐标
            screen_y: 屏幕y坐标
            
        Returns:
            如果坐标在客户区内返回True，否则返回False
        """
        try:
            self._update_window_info()
            
            # 检查是否在客户区范围内
            client_left, client_top = self.client_screen_pos
            client_right = client_left + self.client_width
            client_bottom = client_top + self.client_height
            
            in_bounds = (client_left <= screen_x <= client_right and 
                        client_top <= screen_y <= client_bottom)
            
            return in_bounds
            
        except Exception as e:
            print(f"检查坐标范围失败: {e}")
            return False
    
    def get_window_center(self) -> Tuple[int, int]:
        """
        获取窗口客户区中心点的屏幕坐标
        
        Returns:
            中心点屏幕坐标 (center_x, center_y)
        """
        try:
            self._update_window_info()
            
            center_x = self.client_screen_pos[0] + self.client_width // 2
            center_y = self.client_screen_pos[1] + self.client_height // 2
            
            return center_x, center_y
            
        except Exception as e:
            print(f"获取窗口中心失败: {e}")
            return 0, 0
    
    def click_at_image_coords(self, image_x: int, image_y: int, button: str = 'left') -> bool:
        """
        在图像坐标位置执行鼠标点击
        
        Args:
            image_x: 图像中的x坐标
            image_y: 图像中的y坐标
            button: 鼠标按钮 ('left', 'right', 'middle')
            
        Returns:
            点击是否成功
        """
        try:
            # 转换为屏幕坐标
            screen_x, screen_y = self.image_to_screen_coords(image_x, image_y)
            
            # 检查坐标是否在窗口范围内
            if not self.is_point_in_window(screen_x, screen_y):
                print(f"警告: 点击坐标({screen_x}, {screen_y})超出窗口范围")
            
            # 执行鼠标点击
            return self.click_at_screen_coords(screen_x, screen_y, button)
            
        except Exception as e:
            print(f"在图像坐标点击失败: {e}")
            return False
    
    def click_at_screen_coords(self, screen_x: int, screen_y: int, button: str = 'left') -> bool:
        """
        在屏幕坐标位置执行鼠标点击
        
        Args:
            screen_x: 屏幕x坐标
            screen_y: 屏幕y坐标
            button: 鼠标按钮 ('left', 'right', 'middle')
            
        Returns:
            点击是否成功
        """
        try:
            # 保存当前鼠标位置
            current_pos = win32gui.GetCursorPos()
            
            # 移动鼠标到目标位置
            win32api.SetCursorPos((screen_x, screen_y))
            
            # 根据按钮类型执行点击
            if button == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif button == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            elif button == 'middle':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            else:
                print(f"不支持的鼠标按钮: {button}")
                return False
            
            print(f"在屏幕坐标({screen_x}, {screen_y})执行{button}点击")
            
            # 可选：恢复鼠标原位置
            # win32api.SetCursorPos(current_pos)
            
            return True
            
        except Exception as e:
            print(f"点击失败: {e}")
            return False

    def find_and_click_icon(self, icon_path: str, description: str = "图标", 
                           confidence_threshold: float = 0.8, delay: float = 0.5, 
                           button: str = 'left') -> bool:
        """
        完整的查找图标并点击流程：查找图标 -> 转换坐标 -> 执行点击
        
        Args:
            icon_path: 图标文件路径
            description: 图标描述，用于日志输出
            confidence_threshold: 图像识别置信度阈值
            delay: 点击前的延迟时间（秒）
            button: 鼠标按钮 ('left', 'right', 'middle')
            
        Returns:
            是否成功找到并点击图标
        """
        try:
            from .image_finder import ImageFinder
            
            # 创建图像查找器
            image_finder = ImageFinder(confidence_threshold=confidence_threshold)
            
            # 查找图标
            print(f"正在查找{description}...")
            target_center = image_finder.find_icon_in_game(icon_path)
            
            if target_center:
                print(f"找到{description}，图像坐标：{target_center}")
                
                # 转换为屏幕坐标
                screen_x, screen_y = self.image_to_screen_coords(target_center[0], target_center[1])
                print(f"转换后的屏幕坐标：({screen_x}, {screen_y})")
                
                # 检查坐标是否在窗口范围内
                if self.is_point_in_window(screen_x, screen_y):
                    print(f"坐标在窗口范围内，将在{delay}秒后点击{description}...")
                    
                    # 延迟
                    if delay > 0:
                        import time
                        time.sleep(delay)
                    
                    # 执行点击
                    success = self.click_at_image_coords(target_center[0], target_center[1], button)
                    if success:
                        print(f"成功点击{description}")
                        return True
                    else:
                        print(f"点击{description}失败")
                        return False
                else:
                    print(f"警告：{description}坐标({screen_x}, {screen_y})超出窗口范围")
                    return False
            else:
                print(f"未找到{description}")
                return False
                
        except Exception as e:
            print(f"查找并点击{description}时出错: {e}")
            import traceback
            traceback.print_exc()
            return False