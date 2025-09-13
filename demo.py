import yaml
from notion_client import Client
import requests
import json

# 🔐 获取 Notion Token 和 Database ID
# ntn_o31628992033r9lgU0h148O033gIqHNmTF7H22LxTL19E7
# 读取 YAML 文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

notion_token = config['NOTION_TOKEN']
database_id = config['DATABASE_ID']


# 🧠 提示词模板（可自定义）
prompt_template = "请帮我写一篇关于“{}”的旅游推荐文案，适合发布在小红书上，内容吸引人，有场景感。"

import os
from volcenginesdkarkruntime import Ark

api_key = config['AI_KEY']
# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=api_key,
)
# 初始化 Notion 客户端
notion = Client(auth=notion_token)

# 查询数据库内容
response = notion.databases.query(database_id=database_id)
rows = response["results"]

# 遍历每一行
for row in rows:
    title_property = row["properties"]["Name"]["title"]
    if not title_property:
        continue  # 跳过空标题

    title = title_property[0]["plain_text"]
    print(f"\n📌 当前处理标题：{title}")

    # 构造 prompt
    user_prompt = prompt_template.format(title)


    print("----- streaming request -----")
    stream = client.chat.completions.create(
        model="kimi-k2-250905",
        messages=[
            {"role": "system", "content": "你是旅游小助手."},
            {"role": "user", "content": user_prompt},
        ],
        # 响应内容是否流式返回
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        print(chunk.choices[0].delta.content, end="")
    print()

