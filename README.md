# SiteDownloader
基于selenium的HTML5整站下载器
## 原理
利用selenium模拟访问，获取该页面所有资源文件。再通过HTML解析，分析所有外链，递归地克隆整站。
## 使用方式
修改main.py第15行的downloadurl，运行main.py即可开始下载
## 已知问题
针对不同浏览器设置的不同网站favicon，目前只能下载其中一个。
