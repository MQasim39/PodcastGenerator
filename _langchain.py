#importing necessary functions and classes from langchain
import openai
from langchain.prompts.chat import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SytemMessagePromptTemplate,
    HumanMessagePromptTemplate)

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os

#Setting up OPENAI API KEY
os.environ['OPENAI_API_KEY'] = 'api-key'

#Creating prompt template to generate conversation
#This template is similar to a list of messages that will do the above stated job
Prompt = ChatPromptTemplate.from_messages([SytemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
                                           MessagesPlaceholder(variable_name="history"),
                                           HumanMessagePromptTemplate.from_template("{input}")])

#Here starts the creation of the LLM. We will be using OpenAI api here 
Llm = ChatOpenAI(temperature=0, openai_api_key=os.environ.get("OPENAI_API_KEY"))
Memory = ConversationBufferMemory(return_messages=True)
Conversation = ConversationChain(memory=Memory, prompt=Prompt, llm=Llm)



#Now time to create the podcast generator function
#Here the following parameters mean this:
# 1.) prompt for the topic of the podcast. Could be about guest's personal life, or any other topic
# 2.) podcaster is the host of this podcast. It will be of type string and will be the name of the host.
# 3.) guest for the guest of this podcast. It will be of type string and will be the name of the guest.
def get_response(prompt, podcaster, guest):
    _prompt = f"""

    Generate a podcast between {podcaster} and {guest}. They are discussing about {prompt}.

    """

    response = Conversation.predict(input=_prompt)

    return response

