import os
import re
from volcenginesdkarkruntime import Ark
from dotenv import load_dotenv,find_dotenv
import lei.mytest

class MyAI:
    def __init__(self):
        api_key1 = os.environ.get('DOUBAO_ARK_API_KEY')
        print(api_key1)
        base_url1 = os.environ.get('DOUBAO_base_url')
        print(base_url1)
        client = Ark(api_key=api_key1, base_url=base_url1)
        self.client = client
        self.previous_response_id = None

    def chat(self, use_inport):
        print("开始对话现在和你对话的是火山引擎")
        self.use_inport = use_inport
        create_params = {}
        if self.previous_response_id is None:
            print("self.previous_response_id is None第一次")
            create_params["input"] = [
            {"role": "system", "content": lei.mytest.MyTest.prompt()},
            {"role": "user", "content": use_inport}
        ]
        else: 
            print(f"这是后续对话的id：{self.previous_response_id}")
            create_params["previous_response_id"] = self.previous_response_id
            create_params["input"] = [{"role": "user", "content": use_inport}]
        response1 = self.client.responses.create(
        model="doubao-seed-2-0-mini-260428",
        **create_params,
        # input=[
        #     {"role": "system", "content": lei.mytest.MyTest.prompt()},
        #     {"role": "user", "content": use_inport}
        # ],
        
        # text={
        #     "format": {
        #         "type": "json_schema",
        #         "name": "struct_result",
        #         "strict": True,
        #         "schema": {
        #             "type": "object",
        #             "properties": {
        #                 "core_view": {"type": "string", "description": "原文核心观点"},
        #                 "core_view2": {"type": "string", "description": "原文次级观点"},
        #                 "value_subject": {"type": "array", "items": {"type": "string"}, "description": "原文中提及的地点/角色/法宝"}
        #             },
        #             "required": ["core_view2", "value_subject"]
        #         }
        #     }
        # },
    )
        reasoning_content = " AI 未进行深度思考"
        answer_content = "AI 未返回文本内容"
        self.previous_response_id = response1.id
        for item in response1.output:
            if item.type == "reasoning":
                print("这是深度思考条目")
                reasoning_content=item.summary[0].text
            
            elif item.type == "message":
                print("\n这是文本问答条目")
                answer_content=item.content[0].text
        return {
            "reasoning": reasoning_content,
            "answer": answer_content
        }


