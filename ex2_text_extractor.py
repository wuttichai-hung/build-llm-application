from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI

class Person(BaseModel):
    name: Optional[str] = Field(default=None, description="The name of the person")
    hair_color: Optional[str] = Field(default=None, description="The color of the peron's hair if known")
    height_in_meters: Optional[str] = Field(default=None, description="Height measured in meters")

format_instructions = parser.get_format_instructions()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value."
            "if data in the different unit please convert it"
            "{format_instructions}",
        ),
        ("human", "{text}"),
    ]
)

parser = JsonOutputParser(pydantic_object=Person)

model = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
runnable = prompt | model | parser

text = "Alan Smith is 6 feet tall and has blond hair."
res = runnable.invoke({"text": text, "format_instructions": format_instructions})
res
