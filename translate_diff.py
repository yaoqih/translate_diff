import yaml
import os
import git
import shutil
import difflib
import traceback
import filecmp
import stat
import time
def delete_file(filePath):
    if not os.path.exists(filePath):
        return "no filepath"
    for fileList in os.walk(filePath):
        for name in fileList[2]:
            os.chmod(os.path.join(fileList[0],name), stat.S_IWRITE)
            os.remove(os.path.join(fileList[0],name))
    shutil.rmtree(filePath)
    return "delete ok"
def count_path_deep(file_path):
    if file_path[-1]=='/':
        file_path=file_path[:-1]
    return '../'*file_path.count('/')
# 读取配置文件
if not os.path.exists('./translate_diff/translate_diff_config.yml'):
    print('Error:translate_diff_config.yml not found please check the file and path')
    exit(1)
try:
    with open('./translate_diff/translate_diff_config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
except Exception:
    print("Error:open translate_diff_config.yml error please check the file and path")
    traceback.print_exc()
    exit(1)
# 创建和检测临时文件夹
relative_path = config['relavate_path']
git_url = config['git_url']
git_branch=config['git_branch']
try:
    if not os.path.exists(f'{relative_path}translate_diff_temp'):
        os.makedirs(f'{relative_path}translate_diff_temp')
except Exception:
    print(
        f"Error:create {relative_path}translate_diff_temp floder error , please check the relavate path in yaml file")
    traceback.print_exc()
    exit(1)
if len(os.listdir(f'{relative_path}translate_diff_temp')) != 0:
    delete_file(f'{relative_path}translate_diff_temp/')
if len(os.listdir(f'{relative_path}translate_diff')) != 0:
    delete_file(f'{relative_path}translate_diff')
if not os.path.exists(f'{relative_path}translate_diff'):
    os.makedirs(f'{relative_path}translate_diff')
#clone 仓库
clone_count=0
while True:
    try:
        git.Repo.clone_from(git_url, to_path=f"{relative_path}translate_diff_temp")
    except Exception:
        clone_count+=1
        if clone_count<5:
            print(f"Warning: git clone fail try again {clone_count}/5")
            continue
        else:
            print("Error: git clone fail , please check url and network!")
            exit(1)
    break
repo = git.Repo(f'{relative_path}translate_diff_temp')
git_hash_date=repo.head.commit.authored_datetime.strftime('%Y/%m/%d %H:%M:%S')+' UTC+8'
git_hash_now=repo.head.commit.hexsha
task_list=[]
for check_list in config['check_list']:
    target_file = check_list['目标语言文件']
    origin_file = check_list['源语言文件']
    git_hash = check_list['翻译版本的git hash']
    #读取源语言文件最新版本
    if not os.path.exists(f'{relative_path}translate_diff_temp/{origin_file}'):
        print(f"Warning: origin file [{origin_file}] not exist")
        continue
    replace_filename = origin_file.replace("/", "_").replace("\\", "_")
    shutil.copyfile(f'{relative_path}translate_diff_temp/{origin_file}', f'{relative_path}new_{replace_filename}')
    #读取源语言文件指定hash的版本
    repo.git.checkout(git_branch,b='old_translate_branch')
    repo.git.reset('--hard', git_hash)
    if not os.path.exists(f'{relative_path}translate_diff_temp/{origin_file}'):
        print(f"Warning: The git log of the hash corresponding to the file  [{origin_file}]  cannot be found")
        os.remove(f'{relative_path}new_{replace_filename}')
        repo.git.checkout(git_branch)
        repo.git.branch("-D", "old_translate_branch") 
        continue
    #比较不同
    shutil.copyfile(f'{relative_path}translate_diff_temp/{origin_file}',f'{relative_path}old_{replace_filename}')
    if filecmp.cmp(f'{relative_path}old_{replace_filename}',f'{relative_path}new_{replace_filename}'):
        print('Massage: The git log of the hash of {origin_file} not changes')
        os.remove(f'{relative_path}new_{replace_filename}')
        os.remove(f'{relative_path}old_{replace_filename}')
        repo.git.checkout(git_branch)
        repo.git.branch("-D", "old_translate_branch") 
        continue
    htmlContent = difflib.HtmlDiff(wrapcolumn=70).make_file(open(f'{relative_path}old_{replace_filename}', 'r', encoding='utf-8'), open(
        f'{relative_path}new_{replace_filename}', 'r', encoding='utf-8'), fromdesc=f"old_{replace_filename}", todesc=f"new_{replace_filename}", context=True)
    with open(f'{relative_path}translate_diff/diff_{replace_filename}.html', 'w+', encoding='utf-8') as f:
        f.write(htmlContent)
    #清理
    task_list.append(
        [
            f'{count_path_deep(relative_path)}{origin_file}',
            f'{count_path_deep(relative_path)}{target_file}',
            f'{relative_path}/diff_{replace_filename}.html',
        ]
    )
    repo.git.checkout(git_branch)
    repo.git.branch("-D", "old_translate_branch")
    os.remove(f'{relative_path}old_{replace_filename}')
    os.remove(f'{relative_path}new_{replace_filename}')
markdown_list=['|index|origin_path|translate_path|origin_diff|','|---|---|---|---|']
[markdown_list.append(f"|{task_index}|[{task_list[task_index][0]}]({task_list[task_index][0]})|[{task_list[task_index][1]}]({task_list[task_index][1]})|[{task_list[task_index][2]}]({task_list[task_index][2]})|") for task_index in range(len(task_list))]
with open(f'{relative_path}translate_diff_report.md', 'w', encoding='utf-8') as f:
    f.write(f"## translate update check\n check sha: `{git_hash_now}` \n  check sha date: `{git_hash_date}` \n"+"\n".join(markdown_list))
del repo
delete_file(f'{relative_path}translate_diff_temp/')