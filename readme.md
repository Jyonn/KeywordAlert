# KeywordAlert

## 配置手册

### 环境
- Ubuntu 16.04x64
- Apache2
- MySQL Server 5.7.18
- MySQL Client
- phpMyAdmin
- Python3

### 依赖
- Django
- BeautifulSoup4
- zlib
- mysqlclient

## 使用手册

### 链接
- 首页: 183.134.77.25:9876
- 管理: 183.134.77.25:9876/admin (Chaping321@163.com accelworld.)

### 名词解释
- 新闻统计时长: 分析热门关键词时，统计距现在规定时长的所有新闻
- 数据分析间隔: 分析频率，最小为每分钟分析一次
- 总出现次数: 关键词在所有统计的新闻中需要达到规定的出现次数
- 出现网站个数: 关键词在所有统计的新闻所属的网站中需要达到规定的出现个数
- 新闻热词: 在所有关键词中，达到总出现次数和出现网站个数的关键词