from agent.tasks.task_base import TaskBase
from common.gui_util import get_game_windows, capture_window


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
                image = capture_window(hwnd)
                image.save(f"./screen/{title}.png")
        except Exception as e:
            print(e)
