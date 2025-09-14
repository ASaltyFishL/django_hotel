import pymysql

# 配置PyMySQL与Django 4.2兼容
pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()
