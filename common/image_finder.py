#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图像查找工具 - 简化版本
用于在游戏截图中查找特定的图标或按钮
"""

import os
from typing import Tuple, Optional, List
from .image_recognition import ImageRecognition
from .gui_util import capture_window, get_game_windows


class ImageFinder:
    """
    图像查找工具类
    提供简化的接口来查找游戏界面中的图标或按钮
    """
    
    def __init__(self, confidence_threshold: float = 0.8):
        """
        初始化图像查找器
        
        Args:
            confidence_threshold: 置信度阈值，默认0.8
        """
        self.recognizer = ImageRecognition(confidence_threshold)
        self.game_hwnd = None
        self._setup_game_window()
    
    def _setup_game_window(self):
        """设置游戏窗口"""
        try:
            game_windows = get_game_windows()
            if game_windows:
                self.game_hwnd = game_windows[0][0]  # 使用第一个找到的游戏窗口
                print(f"已连接到游戏窗口: {game_windows[0][1]}")
            else:
                print("未找到游戏窗口")
        except Exception as e:
            print(f"设置游戏窗口时出错: {e}")
    
    def find_icon_in_game(self, icon_path: str, use_multi_scale: bool = True) -> Optional[Tuple[int, int]]:
        """
        在游戏界面中查找指定图标
        
        Args:
            icon_path: 图标文件路径
            use_multi_scale: 已弃用，保留参数向后兼容
            
        Returns:
            图标的中心位置坐标 (x, y)，如果未找到则返回None
        """
        if not self.game_hwnd:
            print("游戏窗口未连接")
            return None
        
        if not os.path.exists(icon_path):
            print(f"图标文件不存在: {icon_path}")
            return None
        
        try:
            # 截取游戏窗口
            scene_image = capture_window(self.game_hwnd)
            if scene_image is None:
                print("截图失败")
                return None
            
            # 使用SIFT特征匹配
            methods = ['feature_match_SIFT']
            
            # 执行图像识别
            results = self.recognizer.find_target_in_scene(scene_image, icon_path, methods)
            
            if results:
                best_match = results[0]  # 取置信度最高的结果
                center = best_match['center']
                confidence = best_match['confidence']
                
                print(f"找到图标 {os.path.basename(icon_path)}")
                print(f"  位置: {center}")
                print(f"  置信度: {confidence:.3f}")
                print(f"  方法: {best_match['method']}")
                
                return center
            else:
                print(f"未找到图标: {os.path.basename(icon_path)}")
                return None
                
        except Exception as e:
            print(f"查找图标时出错: {e}")
            return None
    
    def find_icon_in_image(self, scene_image_path: str, icon_path: str, 
                          use_multi_scale: bool = True) -> Optional[Tuple[int, int]]:
        """
        在指定图像中查找图标
        
        Args:
            scene_image_path: 场景图像路径
            icon_path: 图标文件路径
            use_multi_scale: 已弃用，保留参数向后兼容
            
        Returns:
            图标的中心位置坐标 (x, y)，如果未找到则返回None
        """
        if not os.path.exists(scene_image_path):
            print(f"场景图像文件不存在: {scene_image_path}")
            return None
        
        if not os.path.exists(icon_path):
            print(f"图标文件不存在: {icon_path}")
            return None
        
        try:
            # 使用SIFT特征匹配
            methods = ['feature_match_SIFT']
            
            # 执行图像识别
            results = self.recognizer.find_target_in_scene(scene_image_path, icon_path, methods)
            
            if results:
                best_match = results[0]  # 取置信度最高的结果
                center = best_match['center']
                confidence = best_match['confidence']
                
                print(f"找到图标 {os.path.basename(icon_path)}")
                print(f"  位置: {center}")
                print(f"  置信度: {confidence:.3f}")
                
                return center
            else:
                print(f"未找到图标: {os.path.basename(icon_path)}")
                return None
                
        except Exception as e:
            print(f"查找图标时出错: {e}")
            return None
    
    def find_multiple_icons(self, icon_paths: List[str], 
                           use_multi_scale: bool = True) -> dict:
        """
        在游戏界面中查找多个图标
        
        Args:
            icon_paths: 图标文件路径列表
            use_multi_scale: 已弃用，保留参数向后兼容
            
        Returns:
            字典，键为图标文件名，值为位置坐标或None
        """
        results = {}
        
        if not self.game_hwnd:
            print("游戏窗口未连接")
            return results
        
        try:
            # 截取游戏窗口
            scene_image = capture_window(self.game_hwnd)
            if scene_image is None:
                print("截图失败")
                return results
            
            # 为每个图标查找位置
            for icon_path in icon_paths:
                icon_name = os.path.basename(icon_path)
                
                if not os.path.exists(icon_path):
                    print(f"图标文件不存在: {icon_path}")
                    results[icon_name] = None
                    continue
                
                # 使用SIFT特征匹配
                methods = ['feature_match_SIFT']
                
                # 执行图像识别
                matches = self.recognizer.find_target_in_scene(scene_image, icon_path, methods)
                
                if matches:
                    best_match = matches[0]
                    results[icon_name] = best_match['center']
                    print(f"找到图标 {icon_name}: {best_match['center']}")
                else:
                    results[icon_name] = None
                    print(f"未找到图标: {icon_name}")
            
            return results
            
        except Exception as e:
            print(f"查找多个图标时出错: {e}")
            return results
    
    def is_icon_visible(self, icon_path: str, use_multi_scale: bool = True) -> bool:
        """
        检查图标是否在游戏界面中可见
        
        Args:
            icon_path: 图标文件路径
            use_multi_scale: 已弃用，保留参数向后兼容
            
        Returns:
            如果图标可见返回True，否则返回False
        """
        position = self.find_icon_in_game(icon_path)
        return position is not None
    
    def wait_for_icon(self, icon_path: str, timeout: int = 10, 
                     interval: float = 1.0, use_multi_scale: bool = True) -> Optional[Tuple[int, int]]:
        """
        等待图标出现在游戏界面中
        
        Args:
            icon_path: 图标文件路径
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
            use_multi_scale: 已弃用，保留参数向后兼容
            
        Returns:
            图标的中心位置坐标 (x, y)，如果超时则返回None
        """
        import time
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            position = self.find_icon_in_game(icon_path)
            if position:
                return position
            
            time.sleep(interval)
        
        print(f"等待图标超时: {os.path.basename(icon_path)}")
        return None


def demo_usage():
    """演示如何使用ImageFinder"""
    print("=== ImageFinder 使用演示 ===")
    
    # 创建图像查找器实例
    finder = ImageFinder(confidence_threshold=0.7)
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 单个图标查找
    icon_path = os.path.join(script_dir, "img", "icon", "军事.png")
    print(f"查找图标: {icon_path}")
    
    position = finder.find_icon_in_game(icon_path)
    
    if position:
        print(f"军事图标位置: {position}")
    else:
        print("未找到军事图标")
    
    # 多个图标查找
    icon_paths = [
        os.path.join(script_dir, "img", "icon", "军事.png"),
        # 可以添加更多图标路径
    ]
    
    results = finder.find_multiple_icons(icon_paths)
    print(f"多图标查找结果: {results}")
    
    # 检查图标是否可见
    visible = finder.is_icon_visible(icon_path)
    print(f"军事图标是否可见: {visible}")
    
    # 等待图标出现
    # position = finder.wait_for_icon(icon_path, timeout=5)
    # print(f"等待结果: {position}")


if __name__ == "__main__":
    demo_usage() 