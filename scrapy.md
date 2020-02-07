# Scrapy Notes

## 简单使用
- 安装
```bash
pip install scrapy
```

- 创建项目
```bash
scrapy startproject xxx
cd xxx
```

- 查看文件目录。我们可以看到如下信息
```bash
xxx
├── xxx
│   ├── items.py       # 数据模型文件
│   ├── middlewares.py # 中间件文件，配置所有中间件 
│   ├── pipelines.py   # 管道文件，用于处理数据输出
│   ├── settings.py    # douban_demo 的配置文件
│   └── spiders        # Spider类文件夹，所有的Spider均在此存放
└── scrapy.cfg         # 整个Scrapy的配置文件，由Scrapy自动生成
```

## 描述一个爬虫
- 新建一个爬虫，xxx/spiders底下。
```bash
scrapy genspider douban douban.com
```
