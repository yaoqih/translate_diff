import os
import yaml
task_list = []
for chapter in [f'chapter{i}' for i in range(9)]:
    task_list.extend(
        {
            '目标语言文件': f'chapters/zh-CN/{chapter}/{file}',
            '源语言文件': f'chapters/en/{chapter}/{file}',
            '翻译版本的git hash': 'c4a44e43fa3169bbfa8c4c8b1466a59c4e334be4',
        }
        for file in os.listdir(f'./chapters/zh-CN/{chapter}/')
        if file.endswith('.mdx')
    )
for chapter in [f'chapter{i}' for i in range(9,10)]:
    task_list.extend(
        {
            '目标语言文件': f'chapters/zh-CN/{chapter}/{file}',
            '源语言文件': f'chapters/en/{chapter}/{file}',
            '翻译版本的git hash': '0ef247f21a2f71711c68a12f841e21b49bb296ee',
        }
        for file in os.listdir(f'./chapters/zh-CN/{chapter}/')
        if file.endswith('.mdx')
    )
with open('./translate_diff/translate_diff_config.yml', 'w', encoding='utf-8') as f:
    yaml.dump({'relavate_path': './translate_diff/',
               'git_url': 'https://github.com/huggingface/course',
               'git_branch': 'main','check_list': task_list}, f, allow_unicode=True)
