# TOOLS.md - 本地配置模板（不随技能发布）

## 数据库连接

本技能**仅连接本地 MySQL**，不连接任何远程数据库。

```bash
# 环境变量方式（推荐）
export MYSQL_SOCKET="/tmp/mysql.sock"   # MySQL socket 文件路径（推荐）
export MYSQL_USER="your_user"           # MySQL 用户名
export MYSQL_PASSWORD="your_password"  # MySQL 密码
export MYSQL_DATABASE="workout_tracker" # 数据库名
```

**注意：不支持 MYSQL_HOST（远程连接），仅支持本地 socket 或 localhost:3306。**

## 初始化数据库

```bash
# 创建专用数据库用户（最小权限原则）
mysql -u root -p -S /tmp/mysql.sock -e "
CREATE USER IF NOT EXISTS 'workout_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT INSERT, SELECT, UPDATE, DELETE ON workout_tracker.* TO 'workout_user'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS workout_tracker;
"
```

## 创建表结构

```sql
CREATE TABLE exercise_types (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  muscle_group VARCHAR(50),
  equipment VARCHAR(50),
  unit VARCHAR(10) DEFAULT '次'
);

CREATE TABLE gym_equipment (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL UNIQUE,
  category VARCHAR(30),
  muscle_main VARCHAR(50),
  muscle_sec VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_sessions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL DEFAULT 1,
  workout_date DATE NOT NULL,
  duration_min INT,
  workout_type VARCHAR(30),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workout_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id INT NOT NULL,
  exercise_type_id INT NOT NULL,
  set_order INT DEFAULT 1,
  reps INT,
  weight_kg DECIMAL(6,2),
  notes VARCHAR(100),
  FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE,
  FOREIGN KEY (exercise_type_id) REFERENCES exercise_types(id)
);
```

## 注意事项

- **仅限本地连接**：不暴露数据库到外部网络
- **最小权限用户**：数据库用户仅授予 INSERT/SELECT/UPDATE/DELETE，不授予 DROP 或 ADMIN 权限
- **用户 ID**：默认为 1，可在安装后自行修改
- **数据存储**：所有训练数据仅存储在本地，不上传任何外部服务
