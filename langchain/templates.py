import os
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=500,
)



# Create a prompt template for generating meal titles
prompt_template = PromptTemplate.from_template(
    "List {n} cooking/meal titles for {cuisine} cuisine (name only)."
)

prompt = prompt_template.format(n=3, cuisine="italian")
repsonse = llm.invoke(prompt)
print(repsonse)
