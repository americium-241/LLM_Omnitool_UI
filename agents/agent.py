import streamlit as st
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentType, initialize_agent
from langchain.llms import CTransformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from storage.logger_config import logger
from config import MAX_ITERATIONS,TEMPERATURE, gguf_models
from ui.callbacks_ui import Custom_chat_callback,ToolCallback
class AgentConfig:
    def __init__(self,model, agent_type, tools, chat_history, memory):

        if model in list(gguf_models.keys()):
            config = {'context_length': 2048,'temperature':TEMPERATURE+0.1}
            llm = CTransformers(model=gguf_models[model]['model'], model_file = gguf_models[model]['file'], callbacks=[StreamingStdOutCallbackHandler(),Custom_chat_callback(),ToolCallback()],config=config)#TheBloke/Llama-2-7B-Chat-GGML" #llama-2-7b-chat.ggmlv3.q2_K.bin
        else : 
            llm = ChatOpenAI(temperature=TEMPERATURE,model=model,streaming=True,verbose=True)

        self.model=model
        self.llm = llm
        self.agent_type = agent_type
        self.tools = tools
        self.chat_history = chat_history
        self.memory = memory

        if st.session_state.plan_execute == True : 
            self.planner = load_chat_planner(self.llm)
            self.executor = load_agent_executor(self.llm, tools,include_task_in_prompt=True)


    def _handle_error(self,error):
        return f'Error in agent execution : \n  {error}'

    def initialize_agent(self):
        # allowed kwargs should be checked automatically
        input_variables = ["input", "agent_scratchpad","chat_history"]
        if self.agent_type == AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION or self.agent_type == AgentType.ZERO_SHOT_REACT_DESCRIPTION :
            input_variables = ["input", "agent_scratchpad"]

    
   
        agent_kwargs={
               "extra_prompt_messages": [self.chat_history], #Used for OpenAI agents
                "memory_prompts": [self.chat_history],# Used for non OpenAI agents
                "input_variables": input_variables,
            }
        
        if st.session_state.plan_execute == True :
            st.write("Plan exec is ON") 
       
            return PlanAndExecute(planner=self.planner, executor=self.executor, memory=self.memory,
                agent_kwargs=agent_kwargs,
                verbose=True,handle_parsing_errors=True)
        else :
            return initialize_agent(
                self.tools, 
                self.llm, 
                agent=self.agent_type, 
                verbose=True,
                memory=self.memory,
                agent_kwargs=agent_kwargs,
                max_iterations=MAX_ITERATIONS,
                streaming=True,
                handle_parsing_errors=self._handle_error,

            )






