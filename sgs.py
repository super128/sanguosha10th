import sys
import time
import numpy as np
import pyautogui
import cv2
import logging


class ImageNotFoundException(Exception):
    pass


def find_image(image_path):
    try:
        template = cv2.imread(image_path)
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        # 获取匹配结果
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 如果匹配结果超过设定的阈值，认为找到了
        if max_val > 0.8:
            template_width, template_height = template.shape[1], template.shape[0]
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2

            return center_x, center_y
        else:
            return None
    except Exception as e:
        raise ImageNotFoundException(f"寻找图片时发生异常: {e}")


def find_and_click(image_path, wait_time, i):
    try:
        coordinates = find_image(image_path)
        if coordinates:
            pyautogui.moveTo(coordinates[0], coordinates[1], duration=0.5)
            pyautogui.click()
            time.sleep(wait_time)
        else:
            raise ImageNotFoundException(f"第 {i} 次 未找到 {image_path} 的匹配位置")

    except ImageNotFoundException as e:
        logging.error(f"错误: {e}")


def find_third_and_click(image_path, wait_time, i, max_attempts=50):
    attempts = 0
    while attempts < max_attempts:
        coordinates = find_image(image_path)
        if coordinates:
            print(f"第 {i} 次战斗结束")
            pyautogui.moveTo(coordinates[0], coordinates[1], duration=0.5)
            pyautogui.click()
            break
        else:
            attempts += 1
            logging.warning(f"战斗未结束 第 {attempts} 次获取结束标志 尝试 {attempts}/{max_attempts}")
            time.sleep(wait_time)
    else:
        logging.error(f"第 {attempts} 次 尝试达到最大次数，未获取到结束标志")
        sys.exit(1)


if __name__ == "__main__":
    try:
        num_iterations = input("输入要刷的次数: ")

        # 简单的输入验证
        if not num_iterations.isdigit():
            raise ValueError("请输入有效的数字。")

        num_iterations = int(num_iterations)

        for i in range(1, num_iterations + 1):
            print(f"开始刷逐鹿: 第 {i} 次")

            try:
                steps = [
                    ('images/first.jpg', 1),
                    ('images/second.png', 10),
                    ('images/third.jpg', 1),
                    ('images/fourth.jpg', 1)
                ]

                for image_path, wait_time in steps:
                    if image_path == 'images/third.jpg':
                        find_third_and_click(image_path, wait_time, i)
                    else:
                        find_and_click(image_path, wait_time, i)

            except ImageNotFoundException as e:
                logging.error(f"错误: {e}")

            # 在每次循环之间等待一段时间
            time.sleep(1)

    except Exception as e:
        logging.error(f"发生错误: {e}")
        sys.exit(1)
