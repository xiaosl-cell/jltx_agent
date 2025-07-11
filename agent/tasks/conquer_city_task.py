from agent.tasks.task_base import TaskBase
from common.gui_util import get_game_windows, capture_window
from common.image_finder import ImageFinder
from common.coordinate_converter import CoordinateConverter
from common.image_recognition import ImageRecognition
import time
import numpy as np
import cv2


class ConquerCityTask(TaskBase):
    def __init__(self):
        super().__init__("攻城掠地", "攻城掠地")

    def execute(self):
        try:
            game_windows = get_game_windows()
            titles = [title for hwnd, title in game_windows]
            print(f"检测到{len(game_windows)}个游戏窗口：{titles}")
            
            for game_window in game_windows:
                hwnd, title = game_window
                print(f"正在处理窗口：{title}")
                
                # 创建坐标转换器
                coord_converter = CoordinateConverter(hwnd)
                
                # 使用封装方法查找并点击军事事务图标
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/military_affairs.png",
                    description="军事事务图标",
                    confidence_threshold=0.8,
                    delay=1.0
                )

                # 使用封装方法查找并点击攻城图标
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/conquer_city.png",
                    description="攻城图标",
                    confidence_threshold=0.8,
                    delay=1.0
                )

                
                # 八珍汤
                imageRecognition = ImageRecognition(0.6)
                scene_image = capture_window(hwnd)
                results = imageRecognition.find_target_in_scene(scene_image, "./img/template/bazhentang.png")
                
                # 将PIL Image转换为OpenCV格式用于绘制
                if scene_image is not None:
                    # 转换PIL Image为OpenCV格式
                    scene_cv = cv2.cvtColor(np.array(scene_image), cv2.COLOR_RGB2BGR)
                    # 在图上绘制所有结果
                    print(f"检测到 {len(results)} 个八珍汤")
                    result_image = imageRecognition.draw_matches(scene_cv, results)
                    cv2.imwrite(f"./img/screen/test_result.png", result_image)
                    
                    # 如果检测到八珍汤，点击中心点下方height/4的位置
                    if results:
                        best_match = results[0]  # 取置信度最高的结果
                        center_x, center_y = best_match['center']
                        height = best_match['height']
                        
                        # 计算目标点击位置：中心点下移height/4
                        target_x = center_x
                        target_y = center_y + height // 4 + 5
                        
                        print(f"八珍汤中心点: ({center_x}, {center_y})")
                        print(f"目标点击位置: ({target_x}, {target_y})")
                        
                        # 使用坐标转换器进行点击（图像坐标）
                        coord_converter.click_at_image_coords(target_x, target_y)

                # 搜索对手
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/search_opponent.png",
                    description="搜索对手",
                    confidence_threshold=0.8,
                    delay=1.0
                )
                
                # 确定
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/confirm.png",
                    description="确定",
                    confidence_threshold=0.8,
                    delay=1.0
                )

                # 进攻
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/attack.png",
                    description="进攻",
                    confidence_threshold=0.8,
                    delay=1.0
                )
                
                while True:
                    time.sleep(10)
                    # 游戏窗口左边最中间鼠标左键不放手
                    window_center_x, window_center_y = coord_converter.get_window_center()
                    
                    # 计算左边位置：窗口中心x坐标减去窗口宽度的一半，再加一点偏移避免在边界
                    coord_converter._update_window_info()
                    left_margin = 50  # 距离左边界50像素的位置
                    left_x = coord_converter.client_screen_pos[0] + left_margin
                    center_y = window_center_y
                    
                    print(f"准备在窗口左边中间位置按住鼠标: ({left_x}, {center_y})")
                    
                    # 移动鼠标到目标位置
                    import win32api
                    import win32con
                    win32api.SetCursorPos((left_x, center_y))
                                     # 按下鼠标左键20秒
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    print("鼠标左键已按下，将保持20秒...")
                    
                    # 保持按下20秒
                    time.sleep(10)
                    
                    # 松开鼠标左键
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    print("鼠标左键已松开")
                    
                    # 检查是否出现“下一场”按钮
                    while True:
                        image_finder = ImageFinder(0.8)
                        results = image_finder.find_icon_in_game("./img/template/next_opponent.png")
                        if results:
                            print("下一场按钮已出现，等待5秒后点击")
                            time.sleep(10)
                            break
                    # 点击下一场
                    coord_converter.find_and_click_icon(
                        icon_path="./img/template/next_opponent.png",
                        description="下一场",
                        confidence_threshold=0.8,
                        delay=1.0
                    )
                
                
        except Exception as e:
            print(f"执行任务时出错: {e}")
            import traceback
            traceback.print_exc()
