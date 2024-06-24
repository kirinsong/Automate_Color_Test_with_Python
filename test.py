from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 初始化浏览器
driver = webdriver.Chrome()

try:
    # 打开目标网页
    driver.get('https://www.shj.work/tools/secha/')

    # 等待页面加载并点击“开始测试”按钮
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.play-btn'))
    )
    start_button.click()
    print("点击开始测试按钮成功")

    # 示例：循环进行多个关卡的处理
    while True:
        # 等待颜色方框加载
        color_boxes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#box span'))
        )
        print(f"加载了{len(color_boxes)}个颜色方框")

        # 点击与其他颜色不同的方框
        def find_and_click_different_box(color_boxes):
            # 统计各种颜色的出现次数
            color_count = {}
            for box in color_boxes:
                color = box.value_of_css_property('background-color')
                color_count[color] = color_count.get(color, 0) + 1

            # 找到出现次数为1的颜色，即与其他颜色不同的颜色
            for box in color_boxes:
                color = box.value_of_css_property('background-color')
                if color_count[color] == 1:
                    box.click()
                    print("点击了与其他颜色不同的颜色方框")
                    return True  # 如果点击成功，返回True
            return False  # 如果未找到与其他颜色不同的方框，返回False

        # 调用函数
        if find_and_click_different_box(color_boxes):
            # 如果点击成功，等待新的颜色方框加载
            WebDriverWait(driver, 10).until(
                EC.staleness_of(color_boxes[0])  # 等待第一个颜色方框消失
            )
        else:
            # 如果未找到与其他颜色不同的方框，说明当前关卡已完成，退出循环
            print("未找到与其他颜色不同的颜色方框，当前关卡已完成")
            break

except Exception as e:
    print("游戏结束:", e)

finally:
    # 关闭浏览器
    time.sleep(5)  # 等待几秒钟以查看结果
    driver.quit()
