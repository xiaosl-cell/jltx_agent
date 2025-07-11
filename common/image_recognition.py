from typing import List, Optional, Dict, Any

import cv2
import numpy as np
from PIL import Image


class ImageRecognition:
    """
    图像识别工具类
    支持在场景图中找到目标图的位置，能处理目标大小和长宽比的变化
    """
    
    def __init__(self, confidence_threshold: float = 0.8):
        """
        初始化图像识别器
        
        Args:
            confidence_threshold: 置信度阈值，默认0.8
        """
        self.confidence_threshold = confidence_threshold
        self.sift = cv2.SIFT_create()
        self.orb = cv2.ORB_create()
        
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        加载图像
        
        Args:
            image_path: 图像路径
            
        Returns:
            图像数组或None
        """
        try:
            if isinstance(image_path, str):
                image = cv2.imread(image_path)
            elif isinstance(image_path, Image.Image):
                # 如果是PIL Image对象，转换为OpenCV格式
                image = cv2.cvtColor(np.array(image_path), cv2.COLOR_RGB2BGR)
            else:
                # 如果是numpy数组
                image = image_path
            
            if image is None:
                print(f"无法加载图像: {image_path}")
                return None
            
            return image
        except Exception as e:
            print(f"加载图像时出错: {e}")
            return None
    
    
    def feature_match(self, scene_image: np.ndarray, template_image: np.ndarray, 
                     method: str = 'SIFT') -> List[Dict[str, Any]]:
        """
        特征匹配
        
        Args:
            scene_image: 场景图像
            template_image: 模板图像
            method: 特征提取方法 ('SIFT' 或 'ORB')
            
        Returns:
            匹配结果列表
        """
        try:
            # 转换为灰度图
            scene_gray = cv2.cvtColor(scene_image, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
            
            # 选择特征提取器
            if method == 'SIFT':
                detector = self.sift
            elif method == 'ORB':
                detector = self.orb
            else:
                print(f"不支持的特征提取方法: {method}")
                return []
            
            # 提取特征点和描述子
            kp1, des1 = detector.detectAndCompute(template_gray, None)
            kp2, des2 = detector.detectAndCompute(scene_gray, None)
            
            if des1 is None or des2 is None:
                print("未找到足够的特征点")
                return []
            
            # 特征匹配
            if method == 'SIFT':
                # 使用FLANN匹配器
                FLANN_INDEX_KDTREE = 1
                index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
                search_params = dict(checks=50)
                flann = cv2.FlannBasedMatcher(index_params, search_params)
                matches = flann.knnMatch(des1, des2, k=2)
                
                # 使用Lowe's ratio test筛选好的匹配
                good_matches = []
                for match_pair in matches:
                    if len(match_pair) == 2:
                        m, n = match_pair
                        if m.distance < 0.7 * n.distance:
                            good_matches.append(m)
            else:
                # 使用BF匹配器
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1, des2)
                good_matches = sorted(matches, key=lambda x: x.distance)
            
            # 需要至少4个匹配点来计算单应矩阵
            if len(good_matches) < 4:
                print("匹配点不足，无法计算位置")
                return []
            
            # 提取匹配点的坐标
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            
            # 计算单应矩阵
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            
            if M is None:
                print("无法计算单应矩阵")
                return []
            
            # 计算模板图像的四个角在场景图像中的对应位置
            h, w = template_gray.shape
            pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            
            # 计算中心点
            center_x = np.mean(dst[:, 0, 0])
            center_y = np.mean(dst[:, 0, 1])
            
            # 计算边界框
            x_coords = dst[:, 0, 0]
            y_coords = dst[:, 0, 1]
            min_x, max_x = np.min(x_coords), np.max(x_coords)
            min_y, max_y = np.min(y_coords), np.max(y_coords)
            
            # 计算置信度（基于内点比例）
            confidence = np.sum(mask) / len(mask) if mask is not None else 0
            
            results = []
            if confidence >= 0.3:  # 特征匹配的置信度阈值可以设置得更低
                results.append({
                    'confidence': confidence,
                    'center': (int(center_x), int(center_y)),
                    'top_left': (int(min_x), int(min_y)),
                    'bottom_right': (int(max_x), int(max_y)),
                    'width': int(max_x - min_x),
                    'height': int(max_y - min_y),
                    'corners': dst.reshape(-1, 2).astype(int),
                    'matches_count': len(good_matches),
                    'inliers_count': int(np.sum(mask)) if mask is not None else 0,
                    'method': f'feature_match_{method}'
                })
            
            return results
            
        except Exception as e:
            print(f"特征匹配时出错: {e}")
            return []
    
    def find_target_in_scene(self, scene_image_path: str, template_image_path: str, 
                            methods: List[str] = None) -> List[Dict[str, Any]]:
        """
        在场景图中找到目标图的位置
        
        Args:
            scene_image_path: 场景图像路径或PIL Image对象
            template_image_path: 模板图像路径或PIL Image对象
            methods: 使用的匹配方法列表，默认只使用SIFT特征匹配
            
        Returns:
            所有匹配结果的列表
        """
        if methods is None:
            methods = ['feature_match_SIFT']
        
        # 加载图像
        scene_image = self.load_image(scene_image_path)
        template_image = self.load_image(template_image_path)
        
        if scene_image is None or template_image is None:
            print("无法加载图像")
            return []
        
        all_results = []
        
        # 执行SIFT特征匹配
        for method in methods:
            try:
                if method == 'feature_match_SIFT':
                    results = self.feature_match(scene_image, template_image, 'SIFT')
                else:
                    print(f"不支持的匹配方法: {method}")
                    continue
                
                all_results.extend(results)
                
            except Exception as e:
                print(f"执行匹配方法 {method} 时出错: {e}")
                continue
        
        # 根据置信度排序
        all_results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return all_results
    
    def draw_matches(self, scene_image: np.ndarray, matches: List[Dict[str, Any]], 
                    output_path: str = None) -> np.ndarray:
        """
        在场景图上绘制匹配结果
        
        Args:
            scene_image: 场景图像
            matches: 匹配结果列表
            output_path: 输出图像路径，如果为None则不保存
            
        Returns:
            绘制了匹配结果的图像
        """
        try:
            result_image = scene_image.copy()
            
            for i, match in enumerate(matches):
                # 选择不同的颜色
                colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
                color = colors[i % len(colors)]
                
                # 绘制边界框
                cv2.rectangle(result_image, match['top_left'], match['bottom_right'], color, 2)
                
                # 绘制中心点
                cv2.circle(result_image, match['center'], 5, color, -1)
                
                # 添加标签
                label = f"{match['method']}: {match['confidence']:.2f}"
                cv2.putText(result_image, label, 
                           (match['top_left'][0], match['top_left'][1] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                
                # 如果有角点信息，绘制角点
                if 'corners' in match:
                    corners = match['corners']
                    for j in range(len(corners)):
                        cv2.circle(result_image, tuple(corners[j]), 3, color, -1)
                        # 连接角点形成多边形
                        cv2.polylines(result_image, [corners], True, color, 2)
            
            if output_path:
                cv2.imwrite(output_path, result_image)
                print(f"结果图像已保存到: {output_path}")
            
            return result_image
            
        except Exception as e:
            print(f"绘制匹配结果时出错: {e}")
            return scene_image
