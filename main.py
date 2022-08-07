import re
import os

source_txt = '''
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
author = '江火似流萤'

root_path = r"D:\ccbscf"
write_path = r"C:\Users\weipeng\Desktop"

basic_type = set(
    ['BigDecimal', 'String', 'Timestamp', 'Long', 'Integer', 'Boolean', 'boolean', 'Map', 'List', 'BigInteger', 'T'])
redo_type = set()
dto_dic = {}


def find_file_by_name(filename, root_path=root_path):
    # 查找文件代码
    files = os.listdir(root_path)
    for s in files:
        s_path = os.path.join(root_path, s)
        if os.path.isdir(s_path):
            r = find_file_by_name(filename, s_path)
            if r:
                return r
        elif os.path.isfile(s_path) and filename == s:
            return s_path


def read_file(file_path):
    if file_path:
        with open(file_path, encoding='utf-8') as file:
            r = file.read()
            return r


def beautify_enum(name_enum, content):
    return '<h5 id="' + name_enum + '">' + name_enum + '</h5>\n\n```java\n' + content.split(name_enum + "(")[
        0] + '}\n```\n'


def beautify_dto(name_dto, content):
    class_split = content.split("static class")
    content = class_split[0]
    r = re.findall('ApiModelProperty.*?"(.*?)"', content)
    x = re.findall('private(.*?);', content)
    for i in range(len(x) - 1, -1, -1):
        if 'static' in x[i]:
            print("delete:" + x[i])
            x.pop(i)

    res = '<h5 id="' + name_dto + '">' + name_dto + '</h5>\n\n' + '''
|字段|类型|必填|示例|说明|
| :----: | :----: | :----: | :----: | :----: |\n'''
    for i in range(len(x)):
        split = str.split(x[i].strip(), "=")[0]
        tar = str.split(split.strip(), " ")
        res += "|%s|%s|-|-|%s|\n" % (
            tar[-1], format_type(tar[0]), r[i] if i < len(r) else '-')
    for i in range(1, len(class_split)):
        y = re.search('(.*?)\{', class_split[i])
        if y:
            if y.group(1).strip() not in dto_dic:
                dto_dic[y.group(1).strip()] = class_split[i]
                print("dic add:" + y.group(1).strip())
    return res


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
    content = read_file(find_file_by_name(name_enum + ".java"))
    if not content:
        return 'None\n'
    return beautify_enum(name_enum, content)


def generate_dto(name_dto):
    if name_dto in dto_dic:
        return beautify_dto(name_dto, dto_dic[name_dto])
    content = read_file(find_file_by_name(name_dto + ".java"))
    if not content:
        return 'None\n'
    return beautify_dto(name_dto, content)


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
            if "Enum" in i:
                res += generate_enum(i)
            else:
                res += generate_dto(i)
        over_type = over_type & redo_type_slave
    return res


def write_file(name, text):
    with open(os.path.join(write_path, name) + '.md', 'w', encoding='utf-8') as f:
        f.write(text)


def run():
    method = re.search('@RequestMapping.*?RequestMethod\.(.*?)[,\s\)]', source_txt).group(1)
    url = re.search('@RequestMapping.*?value.*?"(.*?)"', source_txt).group(1)
    describe = re.search('@ApiOperation.*?value.*?"(.*?)"', source_txt)
    describe = describe.group(1) if describe else 'describe'

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
    res_dto = re.search('public(.*?)\(', source_txt).group(1)
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
    run()
