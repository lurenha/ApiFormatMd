import os
import re

# 作者
author = '江火似流萤'
# 载入外部类目录
root_path = r"D:\ccbscf"
# 生产文件目录
write_path = r"C:\Users\weipeng\Desktop"
# 预设类型
basic_type = set(
    ['BigDecimal', 'String', 'Timestamp', 'Long', 'Integer', 'Boolean', 'boolean', 'Map', 'List', 'BigInteger', 'T',
     'Date', 'long', 'int'])
redo_class_set = set()
java_class_dic = {}
dto_path_dic = {}
# ------------------------
template1 = '''<h5 id="{name_class}">{name_class}</h5>\n\n
|字段|类型|必填|说明|备注|
| :----: | :----: | :----: | :----: | :----: |\n{table}'''
# ------------------------
template2 = '''<h5 id="{name_enum}">{name_enum}</h5>\n
```java
  \n
{table}
```\n'''
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

def find_all_java_file_path(cur_path=root_path):
    # 查找文件代码
    files = os.listdir(cur_path)
    for s in files:
        s_path = os.path.join(cur_path, s)
        if os.path.isdir(s_path) and 'target' != s:
            find_all_java_file_path(s_path)
        elif os.path.isfile(s_path):
            pre = s.split(".")[0]
            if '.java' in s:
                dto_path_dic[pre] = s_path


def read_content_by_file_path(file_path):
    if not file_path:
        return None
    with open(file_path, encoding='utf-8') as file:
        r = file.read()
        return r


def beautify_enum(name_enum, content):
    m = content.split('enum ' + name_enum)[1]
    return template2.format(name_enum=name_enum, table='enum ' + name_enum + m[:m.index(';') + 1])


def dfs_generate_table(name_class, cur_table, content):
    parent = re.search(name_class.split('.')[-1]
                       + '\sextends\s(.*?)\s(\{|implements)', content)
    if parent:
        parent = parent.group(1).strip()
        # 先处理父类
        if parent not in java_class_dic:
            return
        dfs_generate_table(parent, cur_table, java_class_dic[parent])
    cur_about = []
    cur_extend = []
    for line in content.split('\n'):
        about = re.search('(//|\*).*', line)
        extend = re.search('ApiModelProperty.*?"(.*?)"', line)
        if about:
            cur_about.append(about.group().replace('*', '').replace('/', ''))
        if extend:
            cur_extend.append(extend.group(1))

        m = re.search('(private|protected)\s([a-zA-Z<>,\s]+)\s([_a-zA-Z0-9]+)\s?[=;]', line)
        if m:
            if 'static' in m.group(2):
                continue
            cur_table.append(
                "|%s|%s|-|%s|%s|\n" % (
                    m.group(3), format_type(m.group(2)), ','.join(cur_extend) if cur_extend else '-',
                    ','.join(cur_about) if cur_about else '-'))
            cur_about.clear()
            cur_extend.clear()


def beautify_class(name_class, content):
    class_chin = name_class.split('.')
    if len(class_chin) > 1:
        beautify_class(class_chin[0], read_content_by_file_path(dto_path_dic[class_chin[0]]))

    class_split = content.split(" class")
    # 内部类 文件遍历时找不到内部类 在此处处理
    for i in range(2, len(class_split)):
        y = re.search('(.*?)(extends|implements|\{)', class_split[i])
        if y:
            if y.group(1).strip() not in java_class_dic:
                java_class_dic[y.group(1).strip()] = "pre class" + class_split[i]
                print("dic add inner class:" + y.group(1).strip())
    # 替换主类
    java_class_dic[name_class] = class_split[1]

    cur_table = []
    dfs_generate_table(name_class, cur_table, class_split[1])

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
            p[-1], format_type(p[-2]))
    return res


def generate_response(dto):
    res = '''
|参数名|类型|示例|说明|
| :----: | :----: | :----: | :----: |
|code|String|"0"|状态码(非0为异常情况)|
|message |String|请求成功|信息描述|
|data|{dto}|-|- |\n'''.format(dto=format_type(dto))
    return res


def generate_enum(name_enum):
    if name_enum in java_class_dic:
        return beautify_enum(name_enum, java_class_dic[name_enum])
    else:
        return 'None\n---\n\n'


def generate_class(name_class):
    if name_class in java_class_dic:
        return beautify_class(name_class, java_class_dic[name_class])
    else:
        return 'None\n---\n\n'


def format_type(dto):
    dto = dto.strip()
    r = re.search('<(.+)>', dto)
    if r:
        s = r.start()
        pre = dto[:s].strip()
        inter = r.group(1)
        r = format_type(pre)
        r += '<' + ','.join([format_type(i) for i in inter.split(',')]) + '>'
        return r
    else:
        if dto in basic_type:
            return dto
        else:
            redo_class_set.add(dto)
            return '''[{dto}](#{dto})'''.format(dto=dto)


def generate_other():
    over_type = set()
    res = ''
    while redo_class_set:
        redo_type_slave = redo_class_set.copy()
        redo_class_set.clear()
        for i in redo_type_slave - over_type:
            if i not in java_class_dic:
                sp = i.split('.')
                tem = read_content_by_file_path(dto_path_dic[sp[0]])
                # 内部类处理
                for cur in sp[1:]:
                    tem = 'pre ' + tem[re.search('class.*?' + cur + '.*{', tem).start():]
                java_class_dic[i] = tem
                java_class_dic[sp[-1]] = tem
            print("generate class:" + i)
            if len(sp) > 1:
                print("generate class:" + sp[-1])
            if "Enum" in i:
                res += generate_enum(i)
            else:
                res += generate_class(i)
            print("----------------------------")
        over_type = over_type | redo_type_slave
    return res


def write_file(name, text):
    with open(os.path.join(write_path, name) + '.md', 'w', encoding='utf-8') as f:
        f.write(text)


def generate_res(source_txt, des='describe'):
    r1 = re.search('@RequestMapping.*?RequestMethod\.(.*?)[,\s\)]', source_txt)
    if r1:
        method = r1.group(1)
    else:
        method = re.search('@(.*)?Mapping', source_txt).group(1)

    r2 = re.search('@RequestMapping.*?value.*?"(.*?)"', source_txt)
    if r2:
        url = r2.group(1)
    else:
        url = re.search('Mapping.*?value.*?"(.*?)"', source_txt).group(1)

    describe = re.search('@ApiOperation.*?value.*?"(.*?)"', source_txt)
    describe = describe.group(1) if describe else des

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
    return res


if __name__ == '__main__':
    param = '''
'''
    find_all_java_file_path(root_path)
    write_file('随便起个名', generate_res(param))
