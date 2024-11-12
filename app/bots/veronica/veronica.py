from dotenv import load_dotenv, find_dotenv
import os
import json

from app.config.utils import retrieve_prompt
from app.bots.openai_model import OpenAiModel
from langchain_openai import ChatOpenAI, OpenAI
from langchain.agents import initialize_agent, create_react_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.chains import LLMChain, ConversationChain
from langchain.schema.messages import HumanMessage, SystemMessage

load_dotenv(find_dotenv())

class Veronica:
    def __init__(self):
        bot_name = "veronica"
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.0,
            openai_api_key=os.environ.get('OPENAI_API_KEY'),
            verbose=True,
        )
        self.open_ai = OpenAiModel()

        self.agent_kwargs = {
            "extra_prompt_messages": [
                SystemMessage(content=retrieve_prompt('veronica')),
                MessagesPlaceholder(variable_name="memory")
            ],
        }
        self.setup_agent()
    
    def invoke(self, user_input, audio_file=None):
        if audio_file:
            transcription = self.open_ai.transcribe_audio(audio_file)
            user_input = f"Audio content: {transcription}\n\nUser input: {user_input}"

        inputs = {'input': user_input}
        response = self.agent.invoke(inputs)
        return response['output']

    def setup_agent(self):
        self.agent = initialize_agent(
            llm=self.llm,
            tools=self.tools(),
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs=self.agent_kwargs,
            memory=self.memory_manager()
        )

    def tools(self):
        return [
                Tool(
                    name="NoOpTool",
                    func=lambda x: x,  
                    description="A placeholder tool"
                )
            ]
    
    def memory_manager(self):
        return ConversationBufferMemory(
            memory_key="memory",
            return_messages=True
        )