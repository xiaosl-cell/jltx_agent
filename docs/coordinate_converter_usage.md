# 坐标转换工具使用说明

## 概述

坐标转换工具 (`CoordinateConverter`) 用于将相对于窗口截图的坐标转换为屏幕绝对坐标，使得程序能够准确地在指定位置执行鼠标点击操作。

## 主要功能

### 1. 坐标转换
- **图像坐标 → 屏幕坐标**：将相对于窗口截图的坐标转换为屏幕绝对坐标
- **屏幕坐标 → 图像坐标**：将屏幕绝对坐标转换为相对于窗口截图的坐标

### 2. 窗口信息获取
- 自动获取窗口位置和尺寸
- 计算客户区域偏移量
- 处理DPI缩放

### 3. 鼠标点击操作
- 支持左键、右键、中键点击
- 自动验证坐标是否在窗口范围内
- 提供安全的点击机制

## 使用方法

### 基本用法

```python
from common.gui_util import get_game_windows
from common.coordinate_converter import CoordinateConverter

# 获取游戏窗口
game_windows = get_game_windows()
hwnd, title = game_windows[0]

# 创建坐标转换器
converter = CoordinateConverter(hwnd)

# 转换坐标
image_x, image_y = 100, 200
screen_x, screen_y = converter.image_to_screen_coords(image_x, image_y)
print(f"图像坐标({image_x}, {image_y}) -> 屏幕坐标({screen_x}, {screen_y})")
```

### 图像查找和点击

```python
from common.image_finder import ImageFinder
from common.coordinate_converter import CoordinateConverter

# 创建图像查找器和坐标转换器
image_finder = ImageFinder(confidence_threshold=0.8)
coord_converter = CoordinateConverter(hwnd)

# 查找图标
target_center = image_finder.find_icon_in_game("./img/template/icon.png")
if target_center:
    # 点击图标
    success = coord_converter.click_at_image_coords(target_center[0], target_center[1])
    if success:
        print("点击成功")
```

### 使用辅助方法

```python
# 在任务类中使用辅助方法
class MyTask(TaskBase):
    def execute(self):
        game_windows = get_game_windows()
        for hwnd, title in game_windows:
            # 使用辅助方法查找并点击图标
            success = self.click_icon_if_found(hwnd, "./img/template/button.png", "按钮")
            if success:
                print("成功点击按钮")
```

## API 参考

### CoordinateConverter 类

#### 构造函数
```python
CoordinateConverter(hwnd: int)
```
- `hwnd`: 窗口句柄

#### 主要方法

##### image_to_screen_coords(image_x, image_y)
将图像坐标转换为屏幕坐标
- **参数**：
  - `image_x`: 图像中的x坐标
  - `image_y`: 图像中的y坐标
- **返回值**：屏幕坐标元组 `(screen_x, screen_y)`

##### screen_to_image_coords(screen_x, screen_y)
将屏幕坐标转换为图像坐标
- **参数**：
  - `screen_x`: 屏幕x坐标
  - `screen_y`: 屏幕y坐标
- **返回值**：图像坐标元组 `(image_x, image_y)`

##### click_at_image_coords(image_x, image_y, button='left')
在图像坐标位置执行点击
- **参数**：
  - `image_x`: 图像中的x坐标
  - `image_y`: 图像中的y坐标
  - `button`: 鼠标按钮 ('left', 'right', 'middle')
- **返回值**：点击是否成功 (bool)

##### click_at_screen_coords(screen_x, screen_y, button='left')
在屏幕坐标位置执行点击
- **参数**：
  - `screen_x`: 屏幕x坐标
  - `screen_y`: 屏幕y坐标
  - `button`: 鼠标按钮 ('left', 'right', 'middle')
- **返回值**：点击是否成功 (bool)

##### is_point_in_window(screen_x, screen_y)
检查屏幕坐标是否在窗口范围内
- **参数**：
  - `screen_x`: 屏幕x坐标
  - `screen_y`: 屏幕y坐标
- **返回值**：是否在窗口范围内 (bool)

##### get_window_center()
获取窗口中心点的屏幕坐标
- **返回值**：中心点坐标元组 `(center_x, center_y)`

## 注意事项

### 1. DPI缩放处理
工具会自动处理Windows的DPI缩放，确保在不同缩放比例下都能正确转换坐标。

### 2. 窗口状态
- 确保目标窗口处于可见状态
- 工具会自动将窗口置于前台
- 建议在使用前检查窗口是否正常

### 3. 坐标系统
- 图像坐标：相对于窗口截图的坐标 (0,0) 为左上角
- 屏幕坐标：绝对屏幕坐标 (0,0) 为屏幕左上角

### 4. 错误处理
- 所有方法都包含异常处理
- 建议在实际使用中检查返回值
- 使用前验证窗口句柄的有效性

## 示例程序

运行示例程序查看详细用法：

```bash
python examples/coordinate_converter_demo.py
```

该程序演示了：
- 基本坐标转换
- 图像查找和点击
- 多坐标转换
- 坐标范围检查

## 常见问题

### Q: 点击位置不准确怎么办？
A: 检查以下几点：
1. 确认DPI缩放设置
2. 验证窗口是否完全可见
3. 检查图像识别的准确性

### Q: 如何处理窗口移动？
A: 坐标转换器会在每次转换时自动更新窗口信息，自动适应窗口位置变化。

### Q: 支持哪些鼠标按钮？
A: 支持左键 ('left')、右键 ('right')、中键 ('middle')。 