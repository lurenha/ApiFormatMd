import requests
import main

cat_name = '测试专用'

if __name__ == '__main__':
    print('begin...')
    data = {
        'api_key': 'e72099f43984c985ab03f82c48dd71cf1291974737',  # 从shwDoc申请账号后填写
        'api_token': '5cb48df923ae7703c12ca2e9ebb57e122087123806',  # 从shwDoc申请账号后填写
        'cat_name': cat_name,
        'page_title': '',
        'page_content': '',
    }

    main.generate_class_path()

    for i in main.split_param_txt(main.read_content_by_file_path(r"./param.txt")):
        describe, content = main.generate_res(i)
        data['page_title'] = describe
        data['page_content'] = content

        response = requests.post('https://www.showdoc.cc/server/api/item/updateByApi', data=data)
        print(response)
    print('succeed')
    print('https://www.showdoc.com.cn/2040347871634336/')
    # 生成文档地址: https://www.showdoc.com.cn/2040347871634336/
    # showDoc 开放API: https://www.showdoc.com.cn/page/102098
