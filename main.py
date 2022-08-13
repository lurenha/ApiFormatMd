import os
import re

# 作者
author = '江火似流萤'
# 载入外部类目录
root_path = r"/Users/apple/java-project/spring-boot-demo"
# 生成md文件目录
write_path = r"/Users/apple/Desktop"
# 预设类型
basic_type = set(
    ['BigDecimal', 'String', 'Timestamp', 'Long', 'Integer', 'Boolean', 'boolean', 'Map', 'List', 'BigInteger', 'T',
     'Date', 'long', 'int', 'void', 'Void', 'byte', 'Byte', 'short', 'Short', 'float', 'Float', 'double', 'Double',
     'Character', 'char'])
class_todo_set = set()
class_content_dic = {}
class_path_dic = {}
class_parent_dic = {}
# ------------------------
template1 = '''<h5 id="{name_class}">{name_class}</h5>\n\n
|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |\n{table}'''
# ------------------------
template2 = '''<h5 id="{name_enum}">{name_enum}</h5>\n
```java
{table}
```
'''
# ------------------------
template_txt = '''
## 接口说明

|名称|描述|
|:--:|:--:|
|功能|**{describe}**|
|负责人|**{name}**|


## HTTP请求地址
- 地址: `http://domain/{url}`

### 请求方式
- {method}

## 参数说明
### 请求参数说明
{request}
\n
### 返回参数说明
{response}
\n
### 补充实体说明
{other}
\n
'''


# ------------------------

def generate_class_path(cur_path=root_path):
    # 查找文件代码
    files = os.listdir(cur_path)
    for s in files:
        s_path = os.path.join(cur_path, s)
        if os.path.isdir(s_path) and 'target' != s:
            generate_class_path(s_path)
        elif os.path.isfile(s_path):
            pre = s.split(".")[0]
            if '.java' in s:
                class_path_dic[pre] = s_path


def read_content_by_file_path(file_path):
    if not file_path:
        return None
    with open(file_path, encoding='utf-8') as file:
        r = file.read()
        return r


def beautify_enum(name_enum, content):
    return template2.format(name_enum=name_enum, table=re.search('enum\s' + name_enum + '.*?;', content, re.S).group())


def dfs_generate_table(name_class, cur_table, content):
    if name_class in class_parent_dic and class_parent_dic[name_class] in class_content_dic:
        parent = class_parent_dic[name_class]
        dfs_generate_table(parent, cur_table, class_content_dic[parent])
    cur_about = []
    cur_extend = []
    for line in content.split('\n'):
        about = re.search('(//|\*).*', line)
        extend = re.search('ApiModelProperty.*?"(.*?)"', line)
        if about:
            about = about.group().replace('*', '').replace('/', '')
            if len(about) > 1:
                cur_about.append(about)
        if extend:
            extend = extend.group(1)
            if len(extend) > 1:
                cur_extend.append(extend)
        m = re.search('(private|protected)\s([a-zA-Z<>,\s]+)\s([_a-zA-Z0-9]+)\s?[=;]', line)
        if m:
            if 'static' in m.group(2):
                continue
            cur_table.append(
                "|%s|%s|-|%s|%s|\n" % (
                    m.group(3), format_and_todo_type(m.group(2)),
                    ','.join(cur_extend).replace('|', ',') if cur_extend else '-',
                    ','.join(cur_about).replace('|', ',') if cur_about else '-'))
            cur_about.clear()
            cur_extend.clear()


def beautify_class(name_class, content):
    cur_table = []
    dfs_generate_table(name_class, cur_table, content)

    table = ''
    for t in cur_table:
        table += t
    table += '---\n\n'

    return template1.format(name_class=name_class, table=table)


def generate_request(param_list):
    res = '''
|参数名|类型|必填|示例|说明|
| :----: | :----: | :----: | :----: | :----: |\n'''
    for p in param_list:
        res += "|%s|%s|-|-|-|\n" % (
            p[-1], format_and_todo_type(p[-2]))
    return res


def generate_response(dto):
    res = '''
|参数名|类型|示例|说明|
| :----: | :----: | :----: | :----: |
|code|String|"0"|状态码(非0为异常情况)|
|message |String|请求成功|信息描述|
|data|{dto}|-|- |\n'''.format(dto=format_and_todo_type(dto))
    return res


def generate_enum(name_enum):
    if name_enum in class_content_dic:
        return beautify_enum(name_enum, class_content_dic[name_enum])
    else:
        return 'None\n---\n\n'


def generate_class(name_class):
    name_class = name_class.split('.')[-1]
    if name_class in class_content_dic:
        return beautify_class(name_class, class_content_dic[name_class])
    else:
        return 'None\n---\n\n'


def format_and_todo_type(vo_name):
    vo_name = vo_name.strip()
    r = re.search('<(.+)>', vo_name)
    if r:
        s = r.start()
        pre = vo_name[:s].strip()
        inter = r.group(1)
        r = format_and_todo_type(pre)
        if '<' not in inter:
            r += '<' + ','.join([format_and_todo_type(i) for i in inter.split(',')]) + '>'
        else:
            r += '<' + format_and_todo_type(inter) + '>'
        return r
    else:
        if vo_name in basic_type:
            return vo_name
        else:
            class_todo_set.add(vo_name)
            return '''[{dto}](#{dto_url})'''.format(dto=vo_name, dto_url=vo_name.split('.')[-1])


def find_right_end_idx(text, begin_idx):
    stack = []
    if text[begin_idx] == '{':
        stack.append(begin_idx)

    for i in range(begin_idx + 1, len(text)):
        if text[i] == '{':
            stack.append(i)
        elif text[i] == '}':
            if text[stack[-1]] == '{':
                stack.pop()
                if not stack:
                    return i
            else:
                stack.append(i)


def dfs_load_class_by_content(source):
    all_content_list = re.findall('class\s.*?{', source)
    for cur_content in all_content_list:
        cur_class_name = re.search('class\s([a-zA-Z]+)\s?(<|>|,|implements|extends|\{)', cur_content).group(1)
        begin = source.find(cur_content) + len(cur_content) - 1
        end = find_right_end_idx(source, begin)
        cur_source = source[begin + 1:end]
        f = re.search('class\s.*?{', cur_source)
        if f:
            # 剔除内部类
            cur_source = cur_source[:cur_source.find(f.group())]
        # 处理当前类和内部类
        print('add:' + cur_class_name)
        class_content_dic[cur_class_name] = cur_source
        p = re.search('\sextends\s(.*?)\s(\{|implements)', cur_content)
        if p:
            parent = p.group(1)
            class_parent_dic[cur_class_name] = parent
            if parent not in class_content_dic:
                if parent in class_path_dic:
                    dfs_load_class_by_content(read_content_by_file_path(class_path_dic[parent]))


def load_class_by_name(class_name):
    if "Enum" in class_name and class_name in class_path_dic and class_name not in class_content_dic:
        class_content_dic[class_name] = read_content_by_file_path(class_path_dic[class_name])
    else:
        sp = class_name.split('.')
        if sp[-1] not in class_content_dic:
            if sp[0] in class_path_dic:
                dfs_load_class_by_content(read_content_by_file_path(class_path_dic[sp[0]]))


def generate_other():
    over_type = set()
    res = ''
    while class_todo_set:
        redo_type_slave = class_todo_set.copy()
        class_todo_set.clear()
        for i in redo_type_slave - over_type:
            load_class_by_name(i)
            if "Enum" in i:
                res += generate_enum(i)
            else:
                res += generate_class(i)
        over_type = over_type | redo_type_slave
    return res


def write_file(name, text):
    with open(os.path.join(write_path, name) + '.md', 'w', encoding='utf-8') as f:
        f.write(text)


def generate_res(source_txt, des='找不到名字了用这个吧'):
    # method
    r1 = re.search('@RequestMapping.*?RequestMethod\.(.*?)[,\s\)]', source_txt)
    method = r1.group(1) if r1 else re.search('@(.*)?Mapping', source_txt).group(1)

    # url
    r2 = re.search('@RequestMapping.*?value.*?"(.*?)"', source_txt)
    url = r2.group(1) if r2 else re.search('Mapping.*?value.*?"(.*?)"', source_txt).group(1)

    # describe
    r3 = re.search('@ApiOperation.*?value.*?"(.*?)"', source_txt)
    describe = r3.group(1) if r3 else des

    # 请求参数说明
    param_list = []
    request_body = re.search('@RequestBody\s([a-zA-Z<>,\s]+)\s([_a-zA-Z0-9]+)\s?[,\)]', source_txt)
    path_variable = re.search('@PathVariable(.*?)\s([a-zA-Z<>,\s]+)\s([_a-zA-Z0-9]+)\s?[,\)]', source_txt)
    param_list.extend(re.findall('@RequestParam.*?\s?([a-zA-Z<>,\s]+)\s([_a-zA-Z0-9]+)\s?[,\)]', source_txt))
    if request_body:
        param_list.append((request_body.group(1), request_body.group(2)))
    if path_variable:
        param_list.append((path_variable.group(2), path_variable.group(3)))
    request = generate_request(param_list)

    # 返回参数说明
    res_dto = re.search('public\s([a-zA-Z<>,\.\s]+)\s([_a-zA-Z0-9]+)\s?\(', source_txt).group(1).strip()
    response = generate_response(res_dto)

    # 补充实体说明
    other = generate_other()
    # 填充到模板
    res = template_txt.format(name=author, describe=describe, url=url, method=method, request=request,
                              response=response, other=other)
    print('success')
    return res


if __name__ == '__main__':
    param = read_content_by_file_path(r"./param.txt")
    generate_class_path(root_path)
    write_file('找不到名字了用这个吧', generate_res(param))
