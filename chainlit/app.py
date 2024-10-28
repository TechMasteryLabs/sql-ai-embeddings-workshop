import os
from dotenv import load_dotenv

from utilities import get_products

from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

import chainlit as cl

load_dotenv()

@cl.on_chat_start
async def on_chat_start():
    openai = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        streaming=True
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "ai",
                """ 
                You are a sales assistant who helps customers find the right products for their question and activities.
                """,
            ),
            (
                "human",
                """
                The products available are the following: 
                {products}                
                """
            ),
            (
                "human",                
                "{question}"
            ),
        ]
    )

    # Use an agent retriever to get products
    retriever = RunnableLambda(get_products, name="GetProducts").bind() 

    runnable = {"products": retriever, "question": RunnablePassthrough()} | prompt | openai | StrOutputParser()
    cl.user_session.set("runnable", runnable)    

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable
    
    msg = cl.Message(content="")

    for chunk in await cl.make_async(runnable.stream)(
        input=message.content,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()

