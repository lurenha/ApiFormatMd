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
redo_type = set()
java_class_dic = {}
dto_dic_path = {}
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


def find_all_java_file_path(cur_path):
    # 查找文件代码
    files = os.listdir(cur_path)
    for s in files:
        s_path = os.path.join(cur_path, s)
        if os.path.isdir(s_path) and 'target' != s:
            find_all_java_file_path(s_path)
        elif os.path.isfile(s_path):
            pre = s.split(".")[0]
            if '.java' in s:
                dto_dic_path[pre] = s_path


def read_content_by_file_path(file_path):
    if not file_path:
        return None
    with open(file_path, encoding='utf-8') as file:
        r = file.read()
        return r


def beautify_enum(name_enum, content):
    template2 = '''<h5 id="{name_enum}">{name_enum}</h5>\n
```java
  \n
{table}
```\n'''
    return template2.format(name_enum=name_enum, table=content.split(name_enum + "(")[0] + '}')


def beautify_class(name_class, content):
    template1 = '''<h5 id="{name_class}">{name_class}</h5>\n\n
|字段|类型|必填|示例|说明|
| :----: | :----: | :----: | :----: | :----: |\n{table}'''

    class_split = content.split("static class")
    content = class_split[0]
    r = re.findall('ApiModelProperty.*?"(.*?)"', content)
    x = re.findall('(private|protected)(.*?);', content)
    for i in range(len(x) - 1, -1, -1):
        if 'static' in x[i][1]:
            print("delete line:" + x[i][1])
            x.pop(i)

    table = ''
    for i in range(len(x)):
        split = str.split(x[i][1].strip(), "=")[0]
        if not split:
            continue
        tar = str.split(split.strip(), " ")
        table += "|%s|%s|-|-|%s|\n" % (
            tar[-1], format_type(tar[-2]), r[i] if i < len(r) else '-')
    table += '---\n\n'

    for i in range(1, len(class_split)):
        y = re.search('(.*?)(extends|\{)', class_split[i])
        if y:
            if y.group(1).strip() not in java_class_dic:
                java_class_dic[y.group(1).strip()] = class_split[i]
                print("dic add inner class:" + y.group(1).strip())

    return template1.format(name_class=name_class, table=table)


def generate_request(param_list):
    res = '''
|参数名|类型|必填|示例|说明|
| :----: | :----: | :----: | :----: | :----: |\n'''
    for param in param_list:
        s = str.split(param[1].strip(), " ")
        res += "|%s|%s|-|-|-|\n" % (
            s[-1], format_type(s[-2]))
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


def format_type(type):
    r = re.search('<(.*)>', type)
    if r:
        s = r.start()
        exter = type[:s].strip()
        inter = r.group(1)
        r = format_type(exter)
        r += '<'
        for i in inter.split(','):
            r += format_type(i)
            r += ","
        r = r[:-1]
        r += '>'
        return r
    else:
        if type in basic_type:
            return type
        else:
            redo_type.add(type)
            return '[' + type + '](#' + type + ')'


def generate_other():
    over_type = set()
    res = ''
    while redo_type:
        redo_type_slave = redo_type.copy()
        redo_type.clear()
        for i in redo_type_slave - over_type:
            if i not in java_class_dic:
                java_class_dic[i] = read_content_by_file_path(dto_dic_path[i])
            print("generate class:" + i)
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


def run(source_txt, des):
    find_all_java_file_path(root_path)
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
    param_list = re.findall('@RequestParam.*?"(.*?)".*?\)(.*?)[,\)]', source_txt)
    request_body = re.search('@RequestBody.*?(.*?)[,\)]', source_txt)
    path_variable = re.search('@PathVariable(.*)[,\)]', source_txt)

    if request_body:
        param_list.insert(0, (request_body.group(1), request_body.group(1)))
    if path_variable:
        param_list.insert(0, (path_variable.group(1), path_variable.group(1)))

    request = generate_request(param_list)
    # 返回参数说明
    res_dto = re.search('public(.*?)\(', source_txt).group(1).strip()
    res_dto = str.split(res_dto.strip(), " ")[0]
    response = generate_response(res_dto)
    # 补充实体说明
    other = generate_other()
    # 填充到模板
    res = template_txt.format(name=author, describe=describe, url=url, method=method, request=request,
                              response=response, other=other)
    # 写入文件
    write_file(describe, res)
    print("succeed!")


if __name__ == '__main__':
    param = '''
    @ApiOperation(value = "平台端根据流程编码查询认证准入信息", notes = "平台端根据流程编码查询认证准入信息")
    @RequestMapping(value = "/v1/corp/real-name/auth/find", method = RequestMethod.GET)
    public BizCorpRealNameAuthResponseVO findCorpRealName(@RequestParam(value = "fkRnProgress") String fkRnProgress) {
        BizCorpRealNameAuthResponseDTO bizCorpRealNameAuthResponseDTO = corpRnAuthService.findCorpRealName(fkRnProgress).tryResult();
        BizCorpRealNameAuthResponseVO bizCorpRealNameAuthResponseVO = BeanUtils.map(bizCorpRealNameAuthResponseDTO, BizCorpRealNameAuthResponseVO.class);
        String currentNodeState = bizCorpRealNameAuthResponseVO.getCurrentNodeState();
        String label = corpRnAuthService.calculateLabel(fkRnProgress, CurrentNodeStateEnum.valueOfCode(currentNodeState)).tryResult();
        bizCorpRealNameAuthResponseVO.setLabel(label);
        setDirectorsProperty(Optional.ofNullable(bizCorpRealNameAuthResponseVO).map(BizCorpRealNameAuthResponseVO::getRnCorp).orElseGet(() -> null));
        return bizCorpRealNameAuthResponseVO;
    }
    '''

    run(param, '是否可以占用额度')
