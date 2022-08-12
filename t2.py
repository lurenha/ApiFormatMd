import re

source = '''
package com.ccbscf.remote.biz.cr.model;

import com.ccbscf.biz.ci.constants.CcbscfTeamRoleEnum;
import com.google.common.base.Strings;
import lombok.*;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


@Data
public class ProjectManagerExcelDataBO implements Serializable {

    public ProjectManagerExcelDataBO(Long lineNum, String staffName, String mobilePhone, String corpName, CcbscfTeamRoleEnum ccbscfTeamRole) {
        this.lineNum = lineNum;
        this.staffName = staffName;
        this.mobilePhone = mobilePhone;
        this.corpName = corpName;
        this.ccbscfTeamRole = ccbscfTeamRole;
    }

    public ProjectManagerExcelDataBO() {
    }
    
    private Long lineNum;
    private String staffName;
    private String mobilePhone;
 
    private String corpName;
 
    private CcbscfTeamRoleEnum ccbscfTeamRole;
    //---------------------------
 
    @Setter
    private String pkStaff;
 
    @Setter
    private String pkCore;
 
    @Setter
    private String pkTeam;
    //---------------------------
 
    private Boolean needsImport = true;
 
    private List<ErrorMsg> errorMsgList = new ArrayList<>();
 
    private List<InfoMsg> infoMsgList = new ArrayList<>();

    public void addErrorMsg(String corpName, String msg) {
        needsImport = false;
        errorMsgList.add(new ErrorMsg(corpName, msg));
    }

    public void addInfoMsg(String corpName, String msg) {
        infoMsgList.add(new InfoMsg(corpName, msg));
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ErrorMsg extends ProjectManVerifyMsgBO {
        public void f1(String corpName, String msg) {
            f.add(new InfoMsg(corpName, msg));
        }
        private String corpName;
        private String msg;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class InfoMsg extends ProjectManVerifyMsgBO {
        private String corpName;
        private String msg;
    }
}

'''


# r = re.search('class\sProjectManagerExcelDataBO.*}', source, flags=re.S).group()

def dfs(text):
    l = text.rfind('{')
    r = text.rfind('}')
    print(text[l + 1, r])
    dfs(text[l + 1, r])


def find_right_idx(text, left_idx):
    left_num = 0
    cur_idx = left_idx
    while True:
        cur_idx = text.find('{', cur_idx + 1)
        if cur_idx > -1:
            left_num += 1
        else:
            break

    while True:
        cur_idx = text.find('}', cur_idx + 1)
        if cur_idx > -1:
            left_num -= 1
        else:
            break
        if left_num == 0:
            return cur_idx


def find_left_num(text, num):
    cur_idx = -1
    while num > 0:
        num -= 1
        cur_idx = text.find('{', cur_idx + 1)
        if cur_idx < 0:
            return cur_idx
    return cur_idx


# l = find_left_num(source, 2)
# r = find_right_idx(source, l)
#
# print(source[l + 1:r])


# def find(text):
#     left_stack = []
#     right_stack = []
#     idx = -1
#     while True:
#         idx = text.find('{', idx + 1)
#         if idx > -1:
#             left_stack.append(idx)
#         else:
#             break
#     idx = len(text)
#     while True:
#         idx = text.rfind('}', 0, idx - 1)
#         if idx > -1:
#             right_stack.append(idx)
#         else:
#             break
#     while left_stack:
#         print(text[left_stack.pop(): right_stack.pop() + 1])
#         print('--------------------------------------------')


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


# for begin in [i for i in range(len(source)) if source[i] == '{']:
#     end = find_right_end_idx(source, begin)
#     print(source[begin + 1:end])
#     print('------------------------------')


class_content_dic = {}


def dfs_load_class_by_name(source):
    all_content_list = re.findall('class\s.*?{', source)
    for cur_content in all_content_list:
        cur_class_name = re.search('class\s([a-zA-Z<>,]+)\s?(implements|extends|\{)', cur_content).group(1)
        begin = source.find(cur_content) + len(cur_content) - 1
        end = find_right_end_idx(source, begin)
        cur_source = source[begin + 1:end]
        f = re.search('class\s.*?{', cur_source)
        if f:
            # 剔除内部类
            cur_source = cur_source[:cur_source.find(f.group())]
        # 处理当前类和内部类
        class_content_dic[cur_class_name] = cur_source
        p = re.search('\sextends\s(.*?)\s(\{|implements)', cur_content)
        if p:
            parent = p.group(1)
            if parent not in class_content_dic:
                pass  # 处理父类


print(class_content_dic)
