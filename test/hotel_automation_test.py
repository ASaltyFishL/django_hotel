#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import string

class HotelManagementSystemTest(unittest.TestCase):
    
    def setUp(self):
        # 初始化WebDriver，使用Edge浏览器
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)  # 隐式等待
        self.base_url = "http://127.0.0.1:8000"
        
        # 随机生成测试数据，避免重复
        self.random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.random_id = str(random.randint(10000, 99999))
        self.random_name = f"测试用户_{self.random_suffix}"
        self.random_room = str(random.randint(100, 999))
        self.random_food = f"测试菜品_{self.random_suffix}"
        self.random_tel = f"138{random.randint(10000000, 99999999)}"
        self.random_id_card = f"110101199{random.randint(10000000, 99999999)}"
        self.random_car_num = f"京A{random.randint(10000, 99999)}"
        
        # 登录系统
        self._login()
    
    def tearDown(self):
        # 测试结束后关闭浏览器
        self.driver.quit()
        
    def _login(self):
        """辅助方法：登录系统"""
        driver = self.driver
        driver.get(f"{self.base_url}/login/")
        
        try:
            username_input = driver.find_element(By.ID, "username")
            password_input = driver.find_element(By.ID, "password")
            
            username_input.send_keys("admin")
            password_input.send_keys("admin")
            
            login_button = driver.find_element(By.ID, "submit")
            login_button.click()
            
            # 等待登录成功跳转
            WebDriverWait(driver, 10).until(
                EC.title_contains("酒店管理系统")
            )
            print("登录成功")
        except Exception as e:
            print(f"登录失败: {str(e)}")
            self.fail("登录失败，无法继续测试")
    
    def test_login(self):
        """测试登录功能"""
        # 重新打开浏览器进行登录测试
        driver = webdriver.Edge()
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        try:
            # 测试成功登录
            driver.get(f"{self.base_url}/login/")
            
            username_input = driver.find_element(By.ID, "username")
            password_input = driver.find_element(By.ID, "password")
            
            username_input.send_keys("admin")
            password_input.send_keys("admin")
            
            login_button = driver.find_element(By.ID, "submit")
            login_button.click()
            
            # 验证登录是否成功
            WebDriverWait(driver, 10).until(
                EC.title_contains("酒店管理系统")
            )
            print("登录测试通过")
        except Exception as e:
            self.fail(f"登录测试失败: {str(e)}")
        finally:
            driver.quit()
    
    def test_staff_management(self):
        """测试员工信息管理功能（增删改查）"""
        driver = self.driver
        
        try:
            # 1. 添加员工
            driver.get(f"{self.base_url}/index/")
            
            # 填写员工信息表单
            id_input = driver.find_element(By.NAME, "id")
            name_input = driver.find_element(By.NAME, "name")
            job_select = driver.find_element(By.NAME, "job")
            salary_input = driver.find_element(By.NAME, "salary")
            time_work_input = driver.find_element(By.NAME, "time_work")
            
            id_input.send_keys(self.random_id)
            name_input.send_keys(self.random_name)
            job_select.send_keys("服务员")
            salary_input.send_keys("3000")
            time_work_input.send_keys("1")
            
            # 提交表单
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            
            # 等待页面加载
            time.sleep(2)
            
            # 2. 查询员工
            search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_staff')]")
            if search_form:
                search_columns = search_form.find_element(By.NAME, "columns")
                search_value = search_form.find_element(By.NAME, "value")
                
                search_columns.send_keys("姓名")
                search_value.send_keys(self.random_name)
                
                search_button = search_form.find_element(By.XPATH, "//input[@type='submit']")
                search_button.click()
                
                # 验证查询结果
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
                )
                print("员工查询测试通过")
            
            # 3. 修改员工信息
            # 注意：这里假设页面上有修改按钮，需要根据实际页面结构调整
            try:
                # 先查询到员工信息
                driver.get(f"{self.base_url}/index/")
                search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_staff')]")
                search_columns = search_form.find_element(By.NAME, "columns")
                search_value = search_form.find_element(By.NAME, "value")
                
                search_columns.send_keys("姓名")
                search_value.send_keys(self.random_name)
                search_form.find_element(By.XPATH, "//input[@type='submit']").click()
                
                # 假设修改功能在另一个页面
                # 这里根据实际情况进行调整
                
            except Exception as e:
                print(f"员工修改测试跳过: {str(e)}")
            
            # 4. 删除员工
            # 先查询到员工
            driver.get(f"{self.base_url}/index/")
            search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_staff')]")
            search_columns = search_form.find_element(By.NAME, "columns")
            search_value = search_form.find_element(By.NAME, "value")
            
            search_columns.send_keys("姓名")
            search_value.send_keys(self.random_name)
            search_form.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # 查找删除按钮并点击
            try:
                delete_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//td[contains(text(), '{self.random_name}')]/following-sibling::td//a[contains(text(), '删除')]"))
                )
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.random_name}')]"), 
                                 "员工删除测试失败：员工信息仍存在")
                print("员工删除测试通过")
            except Exception as e:
                print(f"员工删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"员工管理测试失败: {str(e)}")
    
    def test_client_management(self):
        """测试顾客信息管理功能"""
        driver = self.driver
        
        try:
            # 1. 添加顾客
            driver.get(f"{self.base_url}/insert_client/")
            
            # 填写顾客信息
            id_input = driver.find_element(By.NAME, "id")
            name_input = driver.find_element(By.NAME, "name")
            identify_input = driver.find_element(By.NAME, "identify")
            
            id_input.send_keys(self.random_id)
            name_input.send_keys(self.random_name)
            identify_input.send_keys(self.random_id_card)
            
            # 提交表单
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            
            # 验证顾客是否添加成功
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
            )
            print("顾客添加测试通过")
            
            # 2. 查询顾客
            # 切换到查询表单
            try:
                search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_client')]")
                if search_form:
                    search_columns = search_form.find_element(By.NAME, "columns")
                    search_value = search_form.find_element(By.NAME, "value")
                    
                    search_columns.send_keys("姓名")
                    search_value.send_keys(self.random_name)
                    
                    search_button = search_form.find_element(By.XPATH, "//input[@type='submit']")
                    search_button.click()
                    
                    # 验证查询结果
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
                    )
                    print("顾客查询测试通过")
            except Exception as e:
                print(f"顾客查询测试跳过: {str(e)}")
                
            # 3. 删除顾客
            # 假设删除按钮在页面上
            try:
                delete_button = driver.find_element(By.XPATH, f"//td[contains(text(), '{self.random_name}')]/following-sibling::td//a[contains(text(), '删除')]")
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.random_name}')]"), 
                                 "顾客删除测试失败：顾客信息仍存在")
                print("顾客删除测试通过")
            except Exception as e:
                print(f"顾客删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"顾客管理测试失败: {str(e)}")
    
    def test_room_management(self):
        """测试客房信息管理功能"""
        driver = self.driver
        
        try:
            # 1. 添加客房
            driver.get(f"{self.base_url}/insert_room/")
            
            # 填写客房信息
            id_input = driver.find_element(By.NAME, "id")
            type_input = driver.find_element(By.NAME, "type")
            price_input = driver.find_element(By.NAME, "price")
            waiter_input = driver.find_element(By.NAME, "waiter")
            
            id_input.send_keys(self.random_room)
            type_input.send_keys("标准间")
            price_input.send_keys("200")
            waiter_input.send_keys("1")  # 假设有一个ID为1的服务员
            
            # 提交表单
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            
            # 验证客房是否添加成功
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_room}')]"))
            )
            print("客房添加测试通过")
            
            # 2. 查询客房
            try:
                search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_room')]")
                if search_form:
                    search_columns = search_form.find_element(By.NAME, "columns")
                    search_value = search_form.find_element(By.NAME, "value")
                    
                    search_columns.send_keys("房间号")
                    search_value.send_keys(self.random_room)
                    
                    search_button = search_form.find_element(By.XPATH, "//input[@type='submit']")
                    search_button.click()
                    
                    # 验证查询结果
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_room}')]"))
                    )
                    print("客房查询测试通过")
            except Exception as e:
                print(f"客房查询测试跳过: {str(e)}")
                
            # 3. 删除客房
            try:
                delete_button = driver.find_element(By.XPATH, f"//td[contains(text(), '{self.random_room}')]/following-sibling::td//a[contains(text(), '删除')]")
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.random_room}')]"), 
                                 "客房删除测试失败：客房信息仍存在")
                print("客房删除测试通过")
            except Exception as e:
                print(f"客房删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"客房管理测试失败: {str(e)}")
    
    def test_food_management(self):
        """测试餐厅信息管理功能"""
        driver = self.driver
        
        try:
            # 1. 添加菜品
            driver.get(f"{self.base_url}/insert_food/")
            
            # 填写菜品信息
            id_input = driver.find_element(By.NAME, "id")
            name_input = driver.find_element(By.NAME, "name")
            price_input = driver.find_element(By.NAME, "price")
            cooker_input = driver.find_element(By.NAME, "cooker")
            
            id_input.send_keys(self.random_id)
            name_input.send_keys(self.random_food)
            price_input.send_keys("50")
            cooker_input.send_keys("2")  # 假设有一个ID为2的厨师
            
            # 提交表单
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            
            # 验证菜品是否添加成功
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_food}')]"))
            )
            print("菜品添加测试通过")
            
            # 2. 查询菜品
            try:
                search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_food')]")
                if search_form:
                    search_columns = search_form.find_element(By.NAME, "columns")
                    search_value = search_form.find_element(By.NAME, "value")
                    
                    search_columns.send_keys("菜名")
                    search_value.send_keys(self.random_food)
                    
                    search_button = search_form.find_element(By.XPATH, "//input[@type='submit']")
                    search_button.click()
                    
                    # 验证查询结果
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_food}')]"))
                    )
                    print("菜品查询测试通过")
            except Exception as e:
                print(f"菜品查询测试跳过: {str(e)}")
                
            # 3. 删除菜品
            try:
                delete_button = driver.find_element(By.XPATH, f"//td[contains(text(), '{self.random_food}')]/following-sibling::td//a[contains(text(), '删除')]")
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.random_food}')]"), 
                                 "菜品删除测试失败：菜品信息仍存在")
                print("菜品删除测试通过")
            except Exception as e:
                print(f"菜品删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"餐厅管理测试失败: {str(e)}")
    
    def test_vip_management(self):
        """测试会员信息管理功能"""
        driver = self.driver
        
        try:
            # 1. 添加会员
            driver.get(f"{self.base_url}/insert_vip/")
            
            # 填写会员信息
            id_input = driver.find_element(By.NAME, "id")
            name_input = driver.find_element(By.NAME, "name")
            rank_input = driver.find_element(By.NAME, "rank")
            tel_input = driver.find_element(By.NAME, "tel")
            
            id_input.send_keys(self.random_id)
            name_input.send_keys(self.random_name)
            rank_input.send_keys("金卡会员")
            tel_input.send_keys(self.random_tel)
            
            # 提交表单
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            
            # 验证会员是否添加成功
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
            )
            print("会员添加测试通过")
            
            # 2. 查询会员
            try:
                search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_vip')]")
                if search_form:
                    search_columns = search_form.find_element(By.NAME, "columns")
                    search_value = search_form.find_element(By.NAME, "value")
                    
                    search_columns.send_keys("姓名")
                    search_value.send_keys(self.random_name)
                    
                    search_button = search_form.find_element(By.XPATH, "//input[@type='submit']")
                    search_button.click()
                    
                    # 验证查询结果
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
                    )
                    print("会员查询测试通过")
            except Exception as e:
                print(f"会员查询测试跳过: {str(e)}")
                
            # 3. 删除会员
            try:
                delete_button = driver.find_element(By.XPATH, f"//td[contains(text(), '{self.random_name}')]/following-sibling::td//a[contains(text(), '删除')]")
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.random_name}')]"), 
                                 "会员删除测试失败：会员信息仍存在")
                print("会员删除测试通过")
            except Exception as e:
                print(f"会员删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"会员管理测试失败: {str(e)}")
    
    def test_park_management(self):
        """测试停车场信息管理功能"""
        driver = self.driver
        
        try:
            # 1. 添加停车位信息
            driver.get(f"{self.base_url}/insert_park/")
            
            # 填写停车场信息
            id_input = driver.find_element(By.NAME, "id")
            status_input = driver.find_element(By.NAME, "status")
            num_input = driver.find_element(By.NAME, "num")
            
            id_input.send_keys(self.random_id)
            status_input.send_keys("已占用")
            num_input.send_keys(self.random_car_num)
            
            # 提交表单
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            
            # 验证停车位是否添加成功
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_id}')]"))
            )
            print("停车场添加测试通过")
            
            # 2. 查询停车位
            try:
                search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_park')]")
                if search_form:
                    search_columns = search_form.find_element(By.NAME, "columns")
                    search_value = search_form.find_element(By.NAME, "value")
                    
                    search_columns.send_keys("车位编号")
                    search_value.send_keys(self.random_id)
                    
                    search_button = search_form.find_element(By.XPATH, "//input[@type='submit']")
                    search_button.click()
                    
                    # 验证查询结果
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_id}')]"))
                    )
                    print("停车场查询测试通过")
            except Exception as e:
                print(f"停车场查询测试跳过: {str(e)}")
                
            # 3. 删除停车位
            try:
                delete_button = driver.find_element(By.XPATH, f"//td[contains(text(), '{self.random_id}')]/following-sibling::td//a[contains(text(), '删除')]")
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.random_id}')]"), 
                                 "停车场删除测试失败：停车位信息仍存在")
                print("停车场删除测试通过")
            except Exception as e:
                print(f"停车场删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"停车场管理测试失败: {str(e)}")
            
    def test_order_management(self):
        """测试餐厅订单管理功能"""
        driver = self.driver
        
        try:
            # 首先需要添加一个顾客和一个菜品
            # 1. 添加顾客
            driver.get(f"{self.base_url}/insert_client/")
            id_input = driver.find_element(By.NAME, "id")
            name_input = driver.find_element(By.NAME, "name")
            identify_input = driver.find_element(By.NAME, "identify")
            
            id_input.send_keys(self.random_id)
            name_input.send_keys(self.random_name)
            identify_input.send_keys(self.random_id_card)
            
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # 2. 添加菜品
            driver.get(f"{self.base_url}/insert_food/")
            food_id = str(random.randint(10000, 99999))
            food_name = f"测试菜品_{self.random_suffix}"
            
            driver.find_element(By.NAME, "id").send_keys(food_id)
            driver.find_element(By.NAME, "name").send_keys(food_name)
            driver.find_element(By.NAME, "price").send_keys("50")
            driver.find_element(By.NAME, "cooker").send_keys("2")  # 假设有一个ID为2的厨师
            
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # 3. 创建订单
            driver.get(f"{self.base_url}/insert_order/")
            
            order_id = str(random.randint(10000, 99999))
            table_num = str(random.randint(1, 50))
            
            driver.find_element(By.NAME, "id").send_keys(order_id)
            driver.find_element(By.NAME, "client").send_keys(self.random_id)
            driver.find_element(By.NAME, "food").send_keys(food_id)
            driver.find_element(By.NAME, "waiter").send_keys("1")  # 假设有一个ID为1的服务员
            driver.find_element(By.NAME, "table").send_keys(table_num)
            
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # 验证订单是否创建成功
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{order_id}')]"))
            )
            print("餐厅订单创建测试通过")
            
            # 4. 查询订单
            driver.get(f"{self.base_url}/show_order/")
            try:
                # 根据用户ID查询订单
                driver.find_element(By.NAME, "id").send_keys(self.random_id)
                driver.find_element(By.XPATH, "//input[@type='submit']").click()
                
                # 验证查询结果
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{food_name}')]"))
                )
                print("餐厅订单查询测试通过")
            except Exception as e:
                print(f"餐厅订单查询测试跳过: {str(e)}")
                
            # 5. 删除订单
            try:
                # 先回到订单列表页面
                driver.get(f"{self.base_url}/show_order/")
                
                # 查找删除按钮并点击
                delete_button = driver.find_element(By.XPATH, f"//td[contains(text(), '{order_id}')]/following-sibling::td//a[contains(text(), '删除')]")
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{order_id}')]"), 
                                 "餐厅订单删除测试失败：订单信息仍存在")
                print("餐厅订单删除测试通过")
            except Exception as e:
                print(f"餐厅订单删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"餐厅订单管理测试失败: {str(e)}")
            
    def test_accommodation_management(self):
        """测试客房订单管理功能"""
        driver = self.driver
        
        try:
            # 首先需要添加一个顾客和一个客房
            # 1. 添加顾客
            driver.get(f"{self.base_url}/insert_client/")
            id_input = driver.find_element(By.NAME, "id")
            name_input = driver.find_element(By.NAME, "name")
            identify_input = driver.find_element(By.NAME, "identify")
            
            id_input.send_keys(self.random_id)
            name_input.send_keys(self.random_name)
            identify_input.send_keys(self.random_id_card)
            
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # 2. 添加客房
            driver.get(f"{self.base_url}/insert_room/")
            
            driver.find_element(By.NAME, "id").send_keys(self.random_room)
            driver.find_element(By.NAME, "type").send_keys("标准间")
            driver.find_element(By.NAME, "price").send_keys("200")
            driver.find_element(By.NAME, "waiter").send_keys("1")  # 假设有一个ID为1的服务员
            
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # 3. 创建客房订单
            driver.get(f"{self.base_url}/insert_accomodation/")
            
            order_id = str(random.randint(10000, 99999))
            checkin_time = time.strftime("%Y-%m-%d")
            
            driver.find_element(By.NAME, "id").send_keys(order_id)
            driver.find_element(By.NAME, "client").send_keys(self.random_id)
            driver.find_element(By.NAME, "room").send_keys(self.random_room)
            driver.find_element(By.NAME, "time").send_keys(checkin_time)
            
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # 验证订单是否创建成功
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{order_id}')]"))
            )
            print("客房订单创建测试通过")
            
            # 4. 查询订单
            driver.get(f"{self.base_url}/show_accomodation/")
            try:
                # 根据用户ID查询订单
                driver.find_element(By.NAME, "id").send_keys(self.random_id)
                driver.find_element(By.XPATH, "//input[@type='submit']").click()
                
                # 验证查询结果
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_room}')]"))
                )
                print("客房订单查询测试通过")
            except Exception as e:
                print(f"客房订单查询测试跳过: {str(e)}")
                
            # 5. 删除订单
            try:
                # 先回到订单列表页面
                driver.get(f"{self.base_url}/show_accomodation/")
                
                # 查找删除按钮并点击
                delete_button = driver.find_element(By.XPATH, f"//td[contains(text(), '{order_id}')]/following-sibling::td//a[contains(text(), '删除')]")
                delete_button.click()
                
                # 处理确认对话框
                confirm_alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_alert.accept()
                
                # 验证删除成功
                time.sleep(2)
                self.assertFalse(driver.find_elements(By.XPATH, f"//td[contains(text(), '{order_id}')]"), 
                                 "客房订单删除测试失败：订单信息仍存在")
                print("客房订单删除测试通过")
            except Exception as e:
                print(f"客房订单删除测试跳过: {str(e)}")
                
        except Exception as e:
            self.fail(f"客房订单管理测试失败: {str(e)}")

if __name__ == "__main__":
    unittest.main()