import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

os.environ["GROQ_API_KEY"] = "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"
# Initialize the Groq chat model
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=500,
)

# Create a prompt template for generating meal titles
prompt_template = PromptTemplate.from_template(
    "List {n} cooking/meal titles for {cuisine} cuisine (name only)."
)

# Create a runnable chain using the pipe operator
chain = prompt_template | llm

# Run the chain with specific parameters
response = chain.invoke({
    "n": 8,
    "cuisine": "Italian"
})

# Print the response
print("\nPrompt: List 8 cooking/meal titles for Italian cuisine (name only).")
print("\nResponse:")
print(response.content)