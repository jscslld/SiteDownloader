# SiteDownloader
基于selenium的Themeforest模板整站下载器
## 原理
利用selenium模拟访问，获取模板页面所有资源文件。再通过HTML解析，分析所有内链，递归地克隆整站。
## 使用方式
修改main.py第15行的downloadurl，运行main.py即可开始下载
## 已知问题
~~1.针对不同浏览器设置的不同网站favicon，目前只能下载其中一个~~

2.若其内链为绝对引用，暂无法下载（这个比例很少，Themeforest上绝大多数模板为相对引用。我会尽快修复）

3.无法下载React、Vue等编写的模板，仅支持纯HTML编写的网站。（暂无法修复）
