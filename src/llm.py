from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Try importing Config, otherwise use defaults
try:
    from src.config import Config
    MODEL_NAME = Config.LLM_MODEL
    BASE_URL = Config.OLLAMA_BASE_URL
except ImportError:
    MODEL_NAME = "llama3"
    BASE_URL = "http://localhost:11434"

# Import the specific instance we created in rag.py
from src.rag import rag

class ResolutionSchema(BaseModel):
    root_cause: str = Field(description="Technical explanation")
    fix_steps: str = Field(description="Steps to resolve")
    code_snippet: str = Field(description="Command or Code")

class ErrorResolver:
    def __init__(self):
        self.llm = ChatOllama(
            model=MODEL_NAME,
            base_url=BASE_URL,
            temperature=0.1, 
            format="json"
        )
        self.parser = JsonOutputParser(pydantic_object=ResolutionSchema)

        # PROMPT: Injects 'context' from RAG
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a Senior SRE at ACME Corp.
            Use the retrieved INTERNAL SOP to fix the error.
            
            INTERNAL SOP CONTEXT:
            {context}
            
            ERROR LOG:
            Service: {service}
            Message: {message}

            INSTRUCTIONS:
            1. If the SOP matches the error, YOU MUST prescribe the specific 'Resolution Step' from the SOP.
            2. If no SOP matches, provide a generic standard fix.
            3. Output strictly in JSON.

            {format_instructions}
            """
        )
        self.chain = self.prompt | self.llm | self.parser

    def resolve(self, log_entry):
        # retrieve Context
        print(f"🔍 Searching Knowledge Base for: {log_entry.service_name}")
        context_data = rag.retrieve(log_entry.message)
        
        # generate Answer
        return self.chain.invoke({
            "context": context_data,
            "service": log_entry.service_name,
            "message": log_entry.message,
            "format_instructions": self.parser.get_format_instructions()
        })




# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from src.config import Config
# from src.rag import rag  
# from pydantic import BaseModel, Field

# class ResolutionSchema(BaseModel):
#     root_cause: str = Field(description="Technical explanation")
#     fix_steps: str = Field(description="Steps to resolve")
#     code_snippet: str = Field(description="Command or Code")

# class ErrorResolver:
#     def __init__(self):
#         self.llm = ChatOllama(
#             model=Config.LLM_MODEL,
#             base_url=Config.OLLAMA_BASE_URL,
#             temperature=0.1, 
#             format="json"
#         )
#         self.parser = JsonOutputParser(pydantic_object=ResolutionSchema)

#         # PROMPT: Injects 'context' from RAG
#         self.prompt = ChatPromptTemplate.from_template(
#             """
#             You are a Senior SRE at ACME Corp.
#             Use the retrieved INTERNAL SOP to fix the error.
            
#             INTERNAL SOP CONTEXT:
#             {context}
            
#             ERROR LOG:
#             Service: {service}
#             Message: {message}

#             INSTRUCTIONS:
#             1. If the SOP matches the error, YOU MUST prescribe the specific 'Resolution Step' from the SOP.
#             2. If no SOP matches, provide a generic standard fix.
#             3. Output strictly in JSON.

#             {format_instructions}
#             """
#         )
#         self.chain = self.prompt | self.llm | self.parser

#     def resolve(self, log_entry):
#         # retrieve Context
#         print(f"🔍 Searching Knowledge Base for: {log_entry.service_name}")
#         context_data = rag.retrieve(log_entry.message)
        
#         # generate Answer
#         return self.chain.invoke({
#             "context": context_data,
#             "service": log_entry.service_name,
#             "message": log_entry.message,
#             "format_instructions": self.parser.get_format_instructions()
#         })