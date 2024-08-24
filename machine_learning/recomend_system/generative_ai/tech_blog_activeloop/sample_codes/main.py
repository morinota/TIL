from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core import GPTListIndex
from llama_index.agent


llm = OpenAI(model="gpt-4", temperature=0.2)


documents = SimpleDirectoryReader(input_dir="./data").load_data()
print(documents)
list_index = GPTListIndex.from_documents(documents)

query_engine = list_index.as_query_engine()

response = query_engine.query("日本の大統領は??")

for i in response.response.split("。"):
    print(i + "。")
