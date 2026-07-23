# 第8天学生项目：Flask数据看板强化

## 运行方法

```bash
python -m pip install -r requirements.txt
python validate_day08_environment.py
python app.py
```

浏览器访问 `http://127.0.0.1:5000`。

- 用户名：`student`
- 密码：`day07`

## 第8天学习目标

本项目承接第7天的电商数据看板。在原有页面、登录和问答功能基础上，已完成新的路由、JSON接口、查询参数处理、统一错误响应和自动化测试。

登录后重点测试：`/dashboard`、`/assistant`、`/health`、`/api/metrics` 和 `/api/categories?category=Fashion`。

## 已完成功能

- `/health`：无需登录的服务健康检查；
- `/api/metrics`：返回四张指标卡，保留 `label`、`value`、`note` 字段；
- `/api/categories`：支持通过 `category` 查询参数筛选品类记录；
- 无效品类、无效 JSON 和空问题统一返回包含 `ok`、`error` 的 400 JSON；
- 数据服务会将 pandas / NumPy 值转换为可由 `jsonify` 序列化的普通 Python 值；
- `tests/test_app.py` 包含健康检查、登录保护、指标接口、品类筛选和错误响应测试。

## 运行测试

```bash
python -m unittest discover -s tests -v
python validate_day08_environment.py
python validate_day08_submission.py
```

## 提交方式

不要新建GitHub仓库。继续使用第7天的课程仓库，在其中新增 `day08_flask_upgrade/` 目录，或按教师指定的第8天目录提交。提交前运行：

```bash
python validate_day08_environment.py
python validate_day08_submission.py
git status
git add day08_flask_upgrade
git diff --cached
git commit -m "完成第8天Flask项目强化"
git push
```

不要提交 `.venv/`、`__pycache__/`、`.env`、真实密钥或其他缓存文件。

## 学生信息

- 姓名：许倚帆
- 学号：24012460
- 已完成路由或接口：`/health`、`/api/metrics`、`/api/categories`、`/api/ask` 错误处理
- 测试文件：`tests/test_app.py`（7条测试）
- 尚未解决的问题：无已知问题
