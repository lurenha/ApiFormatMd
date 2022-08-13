import requests
import main

cat_name = '测试专用'
page_title = '随便起个名字'

if __name__ == '__main__':
    main.generate_class_path()

    headers = {
        'authority': 'source.showdoc.com.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://www.showdoc.com.cn',
        'referer': 'https://www.showdoc.com.cn/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    data = {
        'api_key': 'e72099f43984c985ab03f82c48dd71cf1291974737',  # 从shwDoc申请账号后填写
        'api_token': '5cb48df923ae7703c12ca2e9ebb57e122087123806',  # 从shwDoc申请账号后填写
        'cat_name': cat_name,
        'page_title': page_title,
        'page_content': main.generate_res(main.read_content_by_file_path(r"./param.txt")),
    }
    response = requests.post('https://www.showdoc.cc/server/api/item/updateByApi', headers=headers,
                             data=data)
    print(response)
    # 生成文档地址: https://www.showdoc.com.cn/2040347871634336/
    # showDoc 开放API: https://www.showdoc.com.cn/page/102098
