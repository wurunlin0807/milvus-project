import milvusadmeo
import lei.myopenapi

while True:
    user_input = input("输入'exit', 'quit', '退出'结束对话\n‘查询’全量数据\n‘删除’删除数据库\n‘相似度’查询相似度\n请输入你的问题：")    
    print("-" * 30)
    if user_input.strip().lower() in ['exit', 'quit', '退出']:
        print("\n AI: 再见！期待下次与你聊天。")
        break
    if not user_input:
        print("请输入问题，不能为空")
        continue
    if user_input.strip().lower() in ['查询']:
        results =milvusadmeo.MilvusClient1()
        select_data = results.search_data()
        # 3. 打印查询结果
        print(f"共查询到 {len(select_data)} 条数据：")
        for i, row in enumerate(select_data):
            print(f"--- 第 {i+1} 条 ---")
            print(f"  ID      : {row['id']}")
            print(f"  内容    : {row['user_input']}")
            print(f"  向量维度 : {len(row['vector'])} 维")
            print()
        continue
    if user_input.strip().lower() in ['删除']:
        results =milvusadmeo.MilvusClient1()
        results.delete_collection()
        print("数据库已删除")
        continue
    if user_input.strip().lower() in ['相似度','xiangsidu']:
        search_data = input("请输入要查询的内容：")
        to_search_data = lei.myopenapi.MyOpenembed()
        search_data_embedding = to_search_data.embed(search_data)# 获取查询内容的向量表示
        results =milvusadmeo.MilvusClient1() 
        results.search_data(search_data_embedding) # 查询相似度
        print("相似度查询结果已打印")
        continue
