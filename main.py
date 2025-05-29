from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
import json
import time
import os

load_dotenv()

# print(os.getenv("GROQ_API_KEY"))
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"


st.title("Online Price Value")
st.markdown(
    "**Check prices online and get an estimated price and summary of the product"
)

models_list=["Groq Model", "OpenAI Model"]
selected_model=st.selectbox("Select a model:", models_list
                            )
class Product(BaseModel):
    product_name: str=Field(description="Product Name")
    product_description:str=Field(description="Small escription about the product ")
    price:str=Field(description="Price in INR")

parser = JsonOutputParser(pydantic_object=Product)

if selected_model=="Groq Model":
    model=ChatGroq(model="gemma2-9b-it")
else:
    st.warning("Open AI is paid version please check with admin or try using Groq model")
    st.stop()


prompt = PromptTemplate(
    template="""You are an expert who know everything about amazon and ecommerce website and its products.
    If there is anything that you dont know please reply with the answer that currently I dont have the information will update you soon 
    Please check later.  
    Incase if user only enter company name like "Microsoft" then in price section show the company valuation like 1.2 billion dollar valuation
    Respond only with JSON format:
    Please answer the user query,\n{format_instructions}\n{query}\n""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)



chain = prompt|model|parser

user_input = st.text_input("Enter you Product name: ")

if st.button("Submit",type="primary"):
    with st.spinner("Searching...."):
        try:
            response = chain.invoke({"query": user_input})
            st.json(response)
        except Exception as e:
            st.write("An exception occured ")
