import json, sys
from os import listdir
def indent(dep, key, key_value):#以深度为缩进步长输出信息
    print('')
    for i in range(dep):
        print('│   ', end='')
    print('├─', end='')
    print(key, key_value, end='')
def read_all(js, depth):#递归输出内容
    depth += 1
    for i in js:
        if i == 'name':
            indent(depth, i, js[i] )
        if i == 'bend':
            if 'x' in js[i]['axis'] and 'y' not in js[i]['axis'] and 'z' not in js[i]['axis']:
                print('     <-   [可转化为IK部件]', end='')
        if i == 'parts':
            for i in range(len(js['parts'])):
                read_all(js['parts'][i], depth)

def show_info(js):
    print('')
    print('├───────────────────────────────────────\n│    部件名:', js['name'], '\n│    可转化:', end='')
    if 'bend' in js:
        if 'x' in js['bend']['axis'] and 'y' not in js['bend']['axis'] and 'z' not in js['bend']['axis']:
            print(' Yes')
        else:   print(' No')
    else: print(' No')
    if 'bend' in js:
        print('│    偏置值: ', end='')
        if 'end_offset' in js['bend']:
            print(js['bend']['end_offset'])
        else:
            print('N/A')
    print('└───────────────────────────────────────')
    
def set_IK(js):
    if 'bend' in js:
        js['bend']['end_offset'] = input('\n│    Set "end_offset" to :')
        show_info(js)
    else:   print('\n│    不可设置为IK部件')

def save(name):
    with open(name+'.mimodel', 'w') as saved_file:
        json.dump(file_content, saved_file, indent=8)
    print('│ 保存为：\n├─────────────────────────────────────── ', name, end='')

def select(js):#主循环
    inp = input('Input:')
    print('')
    print('┌───────────────────────────────────────', end='')
    if str.isdigit(inp):
        inp = int(inp)
        if 'parts' in js:
            if inp <= len(js['parts']) and inp > 0:
                read_all(js['parts'][inp-1], -1)
                show_info(js['parts'][inp-1])
                if js:
                    select(js['parts'][inp-1])
                else:
                    select(js)
            else:
                print('\n│ 列表越界\n├─────────────────────────────────────── ', end='')
    elif inp == 'w':
        set_IK(js)
    elif inp == 'r':
        read_all(file_content, -1)
        print('\n└───────────────────────────────────────')
        print('\n┌───────────────────────────────────────\n│ 回到根节点\n└───────────────────────────────────────')
        select(file_content)
    elif inp == 's':
        save(input('\n│ 存储为：'))
    elif inp == 'q':
        print('\n│ 退出\n└───────────────────────────────────────')
        sys.exit(0)


    read_all(js, -1)
    show_info(js)
    select(js)


print('  ______________________ ')
print(' |                      |')
print(' | IK  helper           |')
print(' |            by_绅士君 |')
print(' |______________________|')
print('\n建议将脚本放在项目文件夹下\n')
print('当前文件：')
print('┌───────────────────────────────────────')
for i in listdir('.'):
    print('│', i)
print('└───────────────────────────────────────')
file_name = input('输入文件名( 不输入后缀名)：')
if file_name+'.mimodel' in listdir('.'):
    with open(file_name+'.mimodel', mode = 'r') as file:
        file_content = json.load(file)
else:
    print('\n未找到该文件，退出...\n')
    sys.exit(0)

print('\n使用方法：\n使用数字键选择进入的子项部件，符合转化条件的部件将被标出\n（部件具有弯曲属性，且只在X轴弯曲）\n输入1,2,3...进入子项\n输入"r"回到根节点\n输入"w"修改偏置值\n输入"s"保存文件到某个文件名\n输入"q"退出')
print('┌───────────────────────────────────────', end='')
print('', end='')
read_all(file_content, -1)
print('\n└───────────────────────────────────────')

select(file_content)
