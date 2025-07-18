from agent.tasks.task_base import TaskBase
from common.gui_util import get_game_windows
from common.coordinate_converter import CoordinateConverter


class DailyTask(TaskBase):
    def __init__(self):
        super().__init__('日常任务', '日常琐事')

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

                # 点击侧边栏
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/cebian.png",
                    description="侧边栏",
                    confidence_threshold=0.8,
                    delay=1.0
                )

                # 进入军团
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/legion.png",
                    description="进入军团",
                    confidence_threshold=0.8,
                    delay=1.0
                )

                # 军团签到
                coord_converter.find_and_click_icon(
                    icon_path="./img/template/legion_sign_in.png",
                    description="军团签到",
                    confidence_threshold=0.8,
                    delay=1.0
                )

        except Exception as e:
            print(e)
