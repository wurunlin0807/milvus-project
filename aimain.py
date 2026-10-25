import os
from volcenginesdkarkruntime import Ark
from dotenv import load_dotenv,find_dotenv
import lei.myopenapi
import lei.myai
import milvusadmeo

#.\venv\Scripts\Activate.ps1
# 激活虚拟环境

if __name__ == '__main__':
    load_dotenv(find_dotenv()) 
    #该节点调用openai
    ai_bot = lei.myopenapi.MyOpenAI()
    ai_bot2 =lei.myopenapi.MyOpenAI()
    #该节点调用火山引擎
    # ai_bot = lei.myai.MyAI()
    print("现在开始测试")
    while True:
        user_input = input("输入'exit', 'quit', '退出'结束对话\nclear清空历史记录\n请输入你的问题：")    
        if user_input.strip().lower() in ['exit', 'quit', '退出']:
            print("\n AI: 再见！期待下次与你聊天。")
            break
        if not user_input:
            print("请输入问题，不能为空")
            continue
        if user_input.lower() == 'clear':
            ai_bot.chat_history = [ai_bot.chat_history[0]]
            print("历史记录已清空")
            continue
        #这里是非流式返回
        # result1 = ai_bot.chat(user_input)
        # print(result1["reasoning"])
        # print("以下是回答内容")
        # print(result1["answer"])
        # print("-" * 30)
        #这里是流式返回

        # 这里是调用openai外部接口
        # result2 = ai_bot.chat_liushi(user_input)
        # print("您的问题是否是以下内容：", result2)
        # result3 = ai_bot2.chat(result2)
        # print("AI最终回答：", result3["answer"])

        #调用向量引擎
        returnembed= lei.myopenapi.MyOpenembed()
        embedder = returnembed.embed(user_input)
        print("嵌入向量输出数量：", embedder[0])
        print("-" * 30)
        #开始组装数据
        data_to_insert = []
        for i in range(len(embedder)):
            print(f"当前 i = {i}")
            if embedder[i] is not None:
                data_to_insert.append({
                    # "id": i,
                    "user_input": user_input,
                    "vector": embedder[i]
                })
        inserter = milvusadmeo.MilvusClient1()
        inserter.insert_data(data_to_insert)
        print("数据插入完成")
        # 当前轮次向量数据插入完成，等待下一次用户输入
        