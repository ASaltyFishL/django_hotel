#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class HotelManagementSystemTest(unittest.TestCase):
    
    def setUp(self):
        # 初始化WebDriver，这里使用Edge浏览器，需要下载对应版本的msedgedriver
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)  # 隐式等待
        self.base_url = "http://127.0.0.1:8000"
        
        # 随机生成测试数据，避免重复
        self.random_id = str(random.randint(10000, 99999))
        self.random_name = f"测试用户{self.random_id}"
        self.random_room = str(random.randint(100, 999))
        self.random_food = f"测试菜品{self.random_id}"
    
    def tearDown(self):
        # 测试结束后关闭浏览器
        self.driver.quit()
        
    def test_login(self):
        """测试登录功能"""
        driver = self.driver
        driver.get(f"{self.base_url}/login/")
        
        # 输入用户名和密码（注：根据项目实际情况修改，这里假设使用admin/admin）
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        
        username_input.send_keys("admin")
        password_input.send_keys("admin")
        
        # 点击登录按钮
        login_button = driver.find_element(By.ID, "submit")
        login_button.click()
        
        # 验证登录是否成功（这里假设登录成功后会跳转到首页）
        try:
            WebDriverWait(driver, 10).until(
                EC.title_contains("酒店管理系统")
            )
            print("登录测试通过")
        except:
            self.fail("登录测试失败：未能成功登录系统")
    
    def test_staff_management(self):
        """测试员工信息管理功能"""
        driver = self.driver
        
        # 先登录系统
        self._login()
        
        # 1. 测试添加员工
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
        
        # 2. 测试查询员工
        search_form = driver.find_element(By.XPATH, "//form[contains(@action, 'search_staff')]")
        if search_form:
            search_columns = search_form.find_element(By.NAME, "columns")
            search_value = search_form.find_element(By.NAME, "value")
            
            search_columns.send_keys("姓名")
            search_value.send_keys(self.random_name)
            
            search_button = search_form.find_element(By.XPATH, "//input[@type='submit']")
            search_button.click()
            
            # 验证查询结果
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
                )
                print("员工管理测试通过：成功添加和查询员工")
            except:
                self.fail("员工管理测试失败：添加员工后未能查询到")
    
    def test_client_management(self):
        """测试顾客信息管理功能"""
        driver = self.driver
        
        # 先登录系统
        self._login()
        
        # 进入顾客管理页面
        driver.get(f"{self.base_url}/insert_client/")
        
        # 填写顾客信息
        id_input = driver.find_element(By.NAME, "id")
        name_input = driver.find_element(By.NAME, "name")
        identify_input = driver.find_element(By.NAME, "identify")
        
        id_input.send_keys(self.random_id)
        name_input.send_keys(self.random_name)
        identify_input.send_keys(f"11010119900101{self.random_id[:6]}")
        
        # 提交表单
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        # 验证顾客是否添加成功
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
            )
            print("顾客管理测试通过：成功添加顾客")
        except:
            self.fail("顾客管理测试失败：添加顾客后未能显示")
    
    def test_room_management(self):
        """测试客房信息管理功能"""
        driver = self.driver
        
        # 先登录系统
        self._login()
        
        # 进入客房管理页面
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
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_room}')]"))
            )
            print("客房管理测试通过：成功添加客房")
        except:
            self.fail("客房管理测试失败：添加客房后未能显示")
    
    def test_food_management(self):
        """测试餐厅信息管理功能"""
        driver = self.driver
        
        # 先登录系统
        self._login()
        
        # 进入餐厅管理页面
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
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_food}')]"))
            )
            print("餐厅管理测试通过：成功添加菜品")
        except:
            self.fail("餐厅管理测试失败：添加菜品后未能显示")
    
    def test_vip_management(self):
        """测试会员信息管理功能"""
        driver = self.driver
        
        # 先登录系统
        self._login()
        
        # 进入会员管理页面
        driver.get(f"{self.base_url}/insert_vip/")
        
        # 填写会员信息
        id_input = driver.find_element(By.NAME, "id")
        name_input = driver.find_element(By.NAME, "name")
        rank_input = driver.find_element(By.NAME, "rank")
        tel_input = driver.find_element(By.NAME, "tel")
        
        id_input.send_keys(self.random_id)
        name_input.send_keys(self.random_name)
        rank_input.send_keys("金卡会员")
        tel_input.send_keys(f"13800138{self.random_id[:4]}")
        
        # 提交表单
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        # 验证会员是否添加成功
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_name}')]"))
            )
            print("会员管理测试通过：成功添加会员")
        except:
            self.fail("会员管理测试失败：添加会员后未能显示")
    
    def test_park_management(self):
        """测试停车场信息管理功能"""
        driver = self.driver
        
        # 先登录系统
        self._login()
        
        # 进入停车场管理页面
        driver.get(f"{self.base_url}/insert_park/")
        
        # 填写停车场信息
        id_input = driver.find_element(By.NAME, "id")
        status_input = driver.find_element(By.NAME, "status")
        num_input = driver.find_element(By.NAME, "num")
        
        id_input.send_keys(self.random_id)
        status_input.send_keys("已占用")
        num_input.send_keys(f"京A{self.random_id[:5]}")
        
        # 提交表单
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        # 验证停车位是否添加成功
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.random_id}')]"))
            )
            print("停车场管理测试通过：成功添加停车位信息")
        except:
            self.fail("停车场管理测试失败：添加停车位信息后未能显示")
    
    def _login(self):
        """辅助方法：登录系统"""
        driver = self.driver
        driver.get(f"{self.base_url}/login/")
        
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

if __name__ == "__main__":
    unittest.main()