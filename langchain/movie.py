# The description helps the LLM to know what it should put in there.
import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate


os.environ["GROQ_API_KEY"] = "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"
# Initialize the Groq chat model
chat_model = ChatGroq(
      model="llama3-70b-8192",
      temperature=0.7,  # Slightly higher temperature for more creative responses
      max_tokens=500,
)
class Movie(BaseModel):
    title: str = Field(description="The title of the movie.")
    genre: list[str] = Field(description="The genre of the movie.")
    year: int = Field(description="The year the movie was released.")

parser = PydanticOutputParser(pydantic_object=Movie)

prompt_template_text = """
Response with a movie recommendation based on the query:\n
{format_instructions}\n
{query}
"""

format_instructions = parser.get_format_instructions()
prompt_template = PromptTemplate(
    template=prompt_template_text,
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

prompt = prompt_template.format(query="A 90s movie with Nicolas Cage.")
text_output = chat_model.invoke(prompt)
print(text_output.content)  # printed in JSON format
parsed_output = parser.parse(text_output.content)
print(parsed_output)    

# Using LangChain Expression Language (LCEL)
chain = prompt_template | chat_model | parser
response = chain.invoke({"query": "A 90s movie with Nicolas Cage."})
print(response)