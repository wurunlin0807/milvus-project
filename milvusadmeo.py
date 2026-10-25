from pymilvus import MilvusClient, DataType
import os

class MilvusClient1:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_data_milvus.db")
        print(db_path)
        self.client = MilvusClient(db_path)

        if not self.client.has_collection(collection_name="test_collection"):
            schema = self.client.create_schema(auto_id=True)
            schema.add_field("id", datatype=DataType.INT64, is_primary=True)
            schema.add_field("user_input", datatype=DataType.VARCHAR, max_length=100)
            schema.add_field("vector",datatype=DataType.FLOAT_VECTOR, dim=768)
            self.client.create_collection(
                collection_name="test_collection",
                schema=schema
            )
            print("集合创建成功")
        else:
            print("集合已存在，跳过创建")
        # 打印全量合集
        # info = self.client.describe_collection("test_collection")
        # print(info)

    def insert_data(self,embedding_data):# 插入数据
        res = self.client.insert(collection_name="test_collection", data=embedding_data)
        self.client.flush(collection_name="test_collection")
        print(res)

    def search_data(self):# 搜索数据
        self.client.load_collection(collection_name="test_collection")	
        results = self.client.query(
            collection_name="test_collection",
            filter="", 
            output_fields=["*"],  
            limit=100000          
        )
        #print(results) 打印合集
        self.client.release_collection(collection_name="test_collection")	
        return results

    def delete_collection(self):# 删除集合
        self.client.drop_collection(collection_name="test_collection")
        print("集合删除成功")

    def search_data(self, search_data):# 相似度数据
        self.client.load_collection(collection_name="test_collection")	
        results = self.client.search(
            collection_name="test_collection",
            data=search_data,
            limit=2,
            output_fields=["user_input", "id"]
        )
        print("=" * 30)
        print("相似度搜索结果：")
        for hits in results:
            for hit in hits:
                print(f"  ID      : {hit['id']}")
                print(f"  相似度  : {hit['distance']:.4f}")
                print(f"  内容    : {hit['entity'].get('user_input')}")
                print("-" * 30)
        self.client.release_collection(collection_name="test_collection")	
        return results

