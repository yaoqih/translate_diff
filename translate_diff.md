# 比对翻译版本的不同

## 功能分析

比对指定分支当前指定文件在git上与某分支下，某次提交的文件区别

## 功能分解

* [ ] 读取git指定分支的文件
* [ ] 确定已翻译文本的信息记录规范
* [ ] 对比文件计算diff，生成diff文本
* [ ] 生成一个issue任务

## 翻译信息记录规范

### 翻译配置文件

目标语言文件的路径

源语言文件的路径

翻译时对应的git链接

翻译时对应的git hash

## 使用方法

1. 填写 `translate_diff_config.yml` 文件
   ```yaml
   check_list:
   - 源语言文件: 翻译前的文件地址(例如：chapters/en/chapter0/1.mdx)
     目标语言文件: 翻译后的文件地址(例如：chapters/zh-CN/chapter0/1.mdx)
     翻译版本的git hash: 在上一次翻译版本的 git hash（例如：c4a44e43fa3169bbfa8c4c8b1466a59c4e334be4）
   git_branch: git hash所在分支（例如：main）
   git_url:本项目git的url（例如：https://github.com/huggingface/course） 
   relavate_path:transleate_diff.py相对于工作路径的相对路径（例如：./translate_diff/ 或者'./'）

   ```
2. 运行 `translate_diff.py`
