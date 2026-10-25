import os
from time import sleep
from openai import OpenAI
import lei.mytest
from dotenv import load_dotenv, find_dotenv

class MyOpenAI:
    def __init__(self):
        #读取配置
        providers_dict, current_key = lei.mytest.MyTest.model_PROVIDERS()
        config = providers_dict[current_key]
        api_key = config["api_key_env"]
        base_url = config["base_url"]
        self.model = config["model"]
        print(f" 当前服务商: {current_key}")
        # 第三步：创建 OpenAI 客户端
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        # 第四步：初始化上下文管理
        self.previous_response_id = None
        # liushi对话核心步骤 1：创建一个“记事本”（列表），用来存储所有的历史对话.我们先放入一条 system（系统）提示词，给 AI 设定一个人设
        self.chat_history = [
            {"role": "system", "content": lei.mytest.MyTest.prompt()}
        ]       
        self.cishu_sum = 0

    def chat(self, use_inport):
        print("开始对话现在和你对话的是openai总线")
        self.use_inport = use_inport
        create_params = {}
        #判断是否首次对话
        if self.previous_response_id is None:
            print("第一次对话，添加 system prompt")
            create_params["input"] = [
                {"role": "system", "content": lei.mytest.MyTest.promptafter()},
                {"role": "user", "content": use_inport}
            ]
        else:
            print(f"后续对话，id：{self.previous_response_id}")
            create_params["previous_response_id"] = self.previous_response_id
            create_params["input"] = [
                {"role": "user", "content": use_inport}
            ]
            #请求接口
        response1 = self.client.responses.create(
            model=self.model,
            **create_params,
        )
        reasoning_content = " AI 未进行深度思考"
        answer_content = "AI 未返回文本内容"
        self.previous_response_id = response1.id
        for item in response1.output:
            if item.type == "reasoning":
                reasoning_content = item.summary[0].text
            elif item.type == "message":
                answer_content = item.content[0].text
        #输出结果
        return {
            "reasoning": reasoning_content,
            "answer": answer_content
        }
    
    def chat_liushi(self,use_inport):
        
        self.cishu_sum = self.cishu_sum + 1
        print("现在调用的是openai总线的流式输出",flush=True)
        # 核心步骤 2：把用户的新问题，追加（append）到“记事本”中
        self.chat_history.append({"role": "user", "content": use_inport})
        # 用于收集 AI 这次回复的完整内容（因为流式输出是碎片的）
        print(f"第{self.cishu_sum}次",self.chat_history)
        full_response = "" 
        try:
            # 3. 发起 API 请求
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_history, # 👈 注意这里：传入的是整个列表！
                stream=True
            )
            print(f"流的内容：{stream}")
            print(f"-"*30)
            # 4. 流式接收数据（打字机效果）
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        print(delta.content, end="", flush=True)
                        sleep(0.1) 
                        full_response += delta.content # 把碎片拼起来
            print() # AI 回答完毕后换行
            # 这样下一轮对话时，AI 就能知道自己刚才说了什么
            self.chat_history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(f"\n❌ 哎呀，调用 API 出错了: {e}")
            # 如果出错了，把刚才加进去的用户问题撤回，防止污染历史记录
            self.chat_history.pop()
        return full_response

class MyOpenembed:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.LMstudioembd_url = os.environ.get('LMstudioembd_url')
        print(self.LMstudioembd_url)
        self.LMstudioembd = os.environ.get('LMstudioembd')               
        print(self.LMstudioembd)
        self.clientembed=OpenAI(
            base_url=self.LMstudioembd_url,
            api_key=self.LMstudioembd
        )

    def embed(self, text):
        if isinstance(text, str):
            text = [text]
        print("开始生成嵌入向量",text)
        responseembed = self.clientembed.embeddings.create(
            model=self.LMstudioembd,
            input=text
        )
        vectors = [item.embedding for item in responseembed.data]
        print("嵌入向量输出模型：", responseembed.model)
        print("嵌入向量结果：", len(vectors[0]))
        return vectors