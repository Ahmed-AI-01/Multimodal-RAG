from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

from src.utils import load_config


class LlamaChain:
    def __init__(self, chat_memory) -> None:
        prompt = PromptTemplate(
            template="""<|begin_of_text|>
            <|start_header_id|>system<|end_header_id|>
            You are a helpful and knowledgeable AI assistant.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>
            Previous conversation={chat_history}
            Question: {input} 
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=['chat_history', 'input']
        )

        self.memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            chat_memory=chat_memory,
            k=3,
            return_messages=True
        )

        config = load_config()
        llm = LlamaCpp(**config['chat_model'])

        self.llm_chain = RunnableSequence(prompt | llm | self.memory | StrOutputParser())

    def run(self, user_input):
        response = self.llm_chain.invoke(user_input)
        return response['text']