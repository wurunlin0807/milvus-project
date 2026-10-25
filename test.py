"""
aimain.py - Milvus Lite 连接测试 (Python 3.14 + Windows)
"""
import sys
import os

print(f"Python 路径: {sys.executable}")
print(f"Python 版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")
print("=" * 50)

# ---- 测试 1: 导入 pymilvus ----
try:
    from pymilvus import MilvusClient
    print("✅ [1/4] pymilvus 导入成功")
except ImportError as e:
    print(f"❌ [1/4] pymilvus 导入失败: {e}")
    print("   → 请确认虚拟环境已正确配置")
    sys.exit(1)

# ---- 测试 2: 连接 Milvus Lite ----
try:
    # 数据库文件放在脚本同目录下
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_data.db")
    print(f"\n数据库文件将存储在: {db_path}")
    
    client = MilvusClient(db_path)
    print("✅ [2/4] Milvus Lite 连接成功！")
except Exception as e:
    print(f"❌ [2/4] Milvus Lite 连接失败: {e}")
    print("   → milvus-lite 可能未安装或不兼容当前 Python 版本")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ---- 测试 3: 增删改查 ----
try:
    COLLECTION = "_test_verify"
    
    # 清理旧数据
    if client.has_collection(COLLECTION):
        client.drop_collection(COLLECTION)
    
    # 创建集合
    client.create_collection(collection_name=COLLECTION, dimension=4)
    print("✅ [3/4] 集合创建成功")
    
    # 插入数据
    client.insert(COLLECTION, data=[
        {"id": 1, "vector": [0.1, 0.2, 0.3, 0.4], "text": "人工智能"},
        {"id": 2, "vector": [0.5, 0.6, 0.7, 0.8], "text": "机器学习"},
        {"id": 3, "vector": [0.9, 0.1, 0.2, 0.3], "text": "深度学习"},
    ])
    print("   数据插入成功 (3条)")
    
    # 搜索
    results = client.search(
        collection_name=COLLECTION,
        data=[[0.1, 0.2, 0.3, 0.4]],
        limit=2,
        output_fields=["text"],
    )
    top_result = results[0][0]['entity']['text']
    print(f"   搜索成功，最相似结果: \"{top_result}\"")
    
    # 清理
    client.drop_collection(COLLECTION)
    print("✅ [4/4] 全部操作完成，测试数据已清理")
    
except Exception as e:
    print(f"❌ [3-4/4] 数据操作失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("🎉🎉 全部验证通过！")
print(f"   Python {sys.version.split()[0]} + pymilvus + milvus-lite")
print(f"   在 Windows 上完美运行！")
print("=" * 50)