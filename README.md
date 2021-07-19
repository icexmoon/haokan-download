# haokan-download

## 用途

本程序用于从好看视频批量下载某个作者的视频

## 注意事项

- 禁止将本程序用于商业用途。
- 本程序使用Python编写，需要Python环境支持。
- 本程序并未使用多线程，出于作者懒和减少服务器压力的原因。
- 核心的下载服务依赖于you-get，感谢you-get项目。
- 下载结果会保存在命令行的当前工作目录，请确保当前目录有足够空间。
- 经过测试发现you-get对haokan视频的支持并不完善，已经有人提交[**pull**](https://github.com/soimort/you-get/pull/2879)改善，但尚未合并到主分支，所以需要自己手动打包安装该分支代码。
  
## 安装

`pip install haokan-download-icexmoon`

## 使用

1. 通过某个好看作者页面获取作者id，比如`http://haokan.hao123.com/author/1682248365073087`，作者id为`1682248365073087`。
2. 运行`python -m haokan_download --uid xxx --limit xxx`进行下载，`uid`选项必须，`limit`非必须，后者可以限制下载数目。
3. 等待下载结果。因为是单进程，下载速度比较慢。

## 更新日志

### 0.0.2

增加缓存机制