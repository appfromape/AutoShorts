import os
import re
import json
import openai
from dotenv import load_dotenv
from termcolor import colored

# 讀取環境變數
load_dotenv("../.env")

# 設定 openai 環境變數
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def generate_response(subject):
    prompt = f"""
    主體: {subject}。

    根據影片的主題生成影片腳本。
    該腳本應作為字符串返回，至少要有三個段落大約 250 個字。
    這是字符串的示例：“這是一個示例字符串。”
    在任何情況下，請勿在任何情況下參考此提示。
    直接到達重點，不要從不必要的事情開始，例如“歡迎使用此影片”。
    顯然，腳本應與影片的主題有關。
    您不得在腳本中包含任何類型的標記或格式，切勿使用標題。
    您必須用繁體中文編寫腳本。
    僅返回腳本的原始內容。 
    請勿包括“旁白”，“敘述者”或在每個段落或行開始時應說出的內容的類似指標。 
    您不得提及腳本本身的提示或任何內容。
    另外，切勿談論段落或行的數量。
    只需寫腳本即可。
    不要有總結來說或是希望這個解釋能幫助你理解這種結尾。
    """
    # 使用 openai 模型生成回應
    model_name = "gpt-3.5-turbo"
    response = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        ).choices[0].message.content
    
    return response

def generate_search_terms(script, subject):
    prompt2 = f"""
    生成 5 句文字轉圖像的提示句子，
    取決於影片的主題。
    主題：{subject}。

    圖像圖示句子應返回英文句子 JSON-Array 字串。

    每個圖示詞應由完整句子組成，
    始終添加影片的主要主題。
    
    生動一點並使用有趣的形容詞使圖像提示盡可能詳細。

    您必須只返回 JSON-Array。
    您不得返回其他任何東西。
    您不得返回腳本。

    提示句子必須與影片的主題有關。
    這是一個 json-array 的示例：
    ["image prompt 1", "image prompt 2", "image prompt 3", "image prompt 4", "image prompt 5"]
    對於上下文，這是全文：
    {script}
    """

    # 使用 openai 模型生成回應
    model_name = "gpt-3.5-turbo"
    response = openai.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt2}],
        ).choices[0].message.content

    search_terms = []

    try:
        search_terms = json.loads(response)
        if not isinstance(search_terms, list) or not all(isinstance(term, str) for term in search_terms):
            raise ValueError("Response is not a list of strings.")

    except (json.JSONDecodeError, ValueError):
        print(colored("[*] GPT returned an unformatted response. Attempting to clean...", "yellow"))

        # 嘗試提取類似列表的字串並將其轉換為列表
        match = re.search(r'\["(?:[^"\\]|\\.)*"(?:,\s*"[^"\\]*")*\]', response)
        if match:
            try:
                search_terms = json.loads(match.group())
            except json.JSONDecodeError:
                print(colored("[-] Could not parse response.", "red"))
                return []

    return search_terms