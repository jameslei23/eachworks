from flask import Flask, request, send_file, render_template
import os
import tempfile
import pandas as pd
import requests
import json

app = Flask(__name__)

def return_label(prompt):
    url = "https://api.deepseek.com/chat/completions"
    payload = json.dumps({
        "messages": [
            {"content": "You are a helpful assistant", "role": "system"},
            {"content": prompt, "role": "user"}
        ],
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "response_format": {"type": "text"},
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
    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
    response_output = json.loads(response.text)['choices'][0]['message']['content']
    return response_output

def get_product_label(product_name, user_prompt):
    # prompt = f'''
    #             根据商品名称{product_name}，找到这个产品归属的类别，从这里【巧克力系列，糕点与挞壳，奶酪与乳制品，果酱与果泥，烘焙原料，水果制品，其他】只返回一个最符合的类别，直接返回结果，字符串格式，不要加任何说明。
    #             {user_prompt}
    #             '''
    prompt = f'''
    根据{product_name},
    {user_prompt},直接返回结果，不要加任何说明。
    '''
    # print(prompt)
    output = return_label(prompt)
    return output

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    user_prompt = request.form.get('prompt', '')
    if file:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)
        data = pd.read_excel(file_path)
        data['label'] = data.iloc[:,0].apply(lambda x: get_product_label(x, user_prompt))
        output_file_path = os.path.join(temp_dir, 'processed_' + file.filename)
        data.to_excel(output_file_path, index=False)
        return send_file(output_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
