import requests
import main

param = '''
'''


if __name__ == '__main__':
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

    main.generate_class_path()

    data = {
        'page_id': '9213252099951342',
        'item_id': '2040347871634336',
        'page_title': '测试',
        'page_content': main.generate_res(param),
        'is_urlencode': '1',
        'cat_id': '',
        'is_notify': '0',
        'notify_content': '',
        'user_token': '1ae97c56c1bfc129fb04f2a42ec4d47fd408f04d46264e463048770060bfe936',
        '_item_pwd': 'null',
    }
    response = requests.post('https://source.showdoc.com.cn/server/index.php?s=/api/page/save', headers=headers,
                             data=data)
    print(response.content)
