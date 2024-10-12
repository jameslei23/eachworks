import pandas as pd
import requests
import json

def return_label(prompt):

    url = "https://api.deepseek.com/chat/completions"

    payload = json.dumps({
        "messages": [
            {
                "content": "You are a helpful assistant",
                "role": "system"
            },
            {
                "content": prompt,
                "role": "user"
            }
        ],
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer sk-bece9bab5cd14ea2bede32d059c0c837'
    }
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }

    response = requests.request("POST", url, headers=headers, data=payload,
                                proxies=proxies
                                )

    response_output = json.loads(response.text)['choices'][0]['message']['content']
    return response_output

def get_product_label(product_name):
    prompt = f'''
                根据商品名称{product_name}，找到这个产品归属的类别，从这里【巧克力系列，糕点与挞壳，奶酪与乳制品，果酱与果泥，烘焙原料，水果制品，其他】只返回一个最符合的类别，直接返回结果，字符串格式，不要加任何说明。
                '''
    output = return_label(prompt)
    return output

def add_response():
    data = pd.read_excel('../input/Sinodis-产品.xlsx')
    data['label'] = data['Product_Description'].apply(get_product_label)
    print(data)
    # print(get_product_label('卫斯白巧克力（29%可可脂）@5千克'))
    # data.to_excel('../output/Sinodis-产品-标签_deepseek1.xlsx', index=False)
    return data



if __name__ == '__main__':
    add_response()