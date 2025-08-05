# 该项目是一个简单的仓库管理系统，使用 Flask 框架构建，支持设备的添加、出入库操作和查看操作历史。

## 文件结构

```
warehouse_management
├── app.py                     # 应用程序的主文件，定义了Flask应用的路由和处理逻辑
├── templates                  # 存放HTML模板的文件夹
│   ├── index.html            # 首页模板，显示设备库存信息
│   ├── add_device.html       # 添加设备的模板，提供表单以输入设备名称和数量
│   ├── operation.html        # 出入库操作的模板，提供表单以选择设备和输入操作类型及数量
│   └── history.html          # 查看操作历史的模板，显示所有设备的操作记录
├── requirements.txt           # 列出项目所需的Python库及其版本
└── README.md                  # 项目的文档，介绍项目的功能、安装和使用说明
```

## 功能

- **设备管理**：可以添加新设备并指定其数量。
- **出入库操作**：可以对设备进行出库和入库操作，实时更新设备库存。
- **操作历史**：可以查看所有设备的操作记录，了解设备的使用情况。

## 安装

1. 克隆此项目到本地：
   ```
   git clone <repository-url>
   ```
2. 进入项目目录：
   ```
   cd warehouse_management
   ```
3. 安装所需的依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用

1. 运行应用程序：
   ```
   python app.py
   ```
2. 打开浏览器，访问 `http://127.0.0.1:5000` 查看应用程序。

## 依赖

- Flask
- SQLite3

请根据需要修改和扩展此文档。
# WareHouse_Management
