LLM Omnitool UI
=============================

A minimalistic streamlit chatbot UI to combine and customize tools for langchain llm agents. OpenAI or local quantized Llama or Mistral models can be used to power the chatbot. The simple integration of custom tools and agents gives a straightforward experience to build a chatbot adapted to one's specific needs. Custom tools can be any python function. So any call to third party agents can be integrated as a tool, from langchain, hugging face or autogen for instance, offering an endless combination of functionnalities to the chatbot. 

For an illustrative breakdown of the application's structure and flow, refer to our schema: 

<p >
  <img src="./assets/streamlit_schema.png " width="600" />
</p>


The project integrates voice commands to push for seamless interaction and leverage vector data base for relevant document retriving. 
Advanced users can modify the project very easily thanks to its modular architecture, giving you full control to extend the chatbot functionnalities. Manage API keys, configure chatbot settings, connect it to all your custom tools and data and unleash the full potential of AI chatbot, I mean, hopefully one day, when this project will be complete. In the meantime, please have a look and enjoy the ride. 

Here is a x2 speed demonstration of the app: 

https://github.com/americium-241/Omnitool_UI/assets/64111755/63f8406a-1cec-44b1-946a-abbaa374010c

## Disclaimer

This app has been developped to run locally on your private network. Any use in a multi-user public network should be avoided without important modifications to the project. We recommand the use of a docker environment to run the app, which garanties basic safety. Do not forget that some tools allow the chatbot to automatically execute any type of code, so don't ask it to mess with your computer, otherwise it sure will. 


## Try the app

We propose a streamlit cloud version that garanties the security of api keys but keep in mind that the chat history (question/answers) is shared among users, so do not reveal private matters. You can delete your session history afterwards if you click on it. Most features and tools are available in this version but because of the limitations of the streamlit cloud host some are not working (local models, voice commands, powershell execution ...). 

Have a look and try the app at : https://omnitoolui-stcloud.streamlit.app/

Summary
  -------
  
  1. **Main Features**
  2. **Customizability**
  3. **Tools showcase**
  4. **Installation Methods**
    
  -------

1. **Main Features**:
- Browse arxiv and wikipedia
![Streamlit App](./assets/welcome_screen.png)
- Browse web and in-app display

https://github.com/americium-241/Omnitool_UI/assets/64111755/146e15b0-8cab-4aae-93e3-cf082ea3186e

- Terminal navigation


https://github.com/americium-241/Omnitool_UI/assets/64111755/8af2e98a-278f-4fd7-8711-851a6857a994

2. **Tools showcase**:

| Autogen agents         | Stable diffusion       |
| ---------------------- | ---------------------- |
| ![autogen](./assets/autogen_screen.png) | ![stablediff](./assets/stable_diff_ex.png) |

| Hugging face agents    | Database query         |
| ---------------------- | ---------------------- |
| ![hugface](./assets/hugging_face.png) | ![dbq](./assets/db_query.png) |

| Code                   | Run local         |
| ---------------------- | ---------------------- |
| ![hugface](./assets/code.png) | ![dbq](./assets/local_run.png) |


3. **Customizability**:

The projet is built so important features can easily be modified, such as custom: tools, agents, callbacks and config parameters.

The project tree diagram below gives precisions on which file/folder can easily be modified:

```
.
│   config.py # Modify lists of : KEYS, AGENTS, MODELS ... And many parameters
│   docker-compose.yml # Docker orchestrator
│   Dockerfile.streamlit # Docker python image to create app environment 
│   Omnitool_UI.py # Main
│   requirements.txt # pip install this file in a virtual environment
├───agents 
│   │   agent.py # Base agent config 
│   ├───agents_list # Monitored folder to create new agents 
│   │   │   new_agent.py # Custom agent exemple
├───storage
│   │   document.py # Document manager
│   │   logger_config.py # logger config
│   │   storage.py # Database app storage
├───tools
│   │   base_tools.py # Base UI_tool 
│   │   browser_tool.py # Custom subprocess tool exemple
│   │   tool_manager.py # Tool lists manager
│   │   utils.py # Usefull functions
│   ├───tools_list # Monitored folder to create new tools 
│   │   │   test_tool.py # Custom class tool exemple
│   │   │   tools_list.py # All pre-built tools
├───ui
│   │   callbacks_ui.py # Manage llm callbacks to enhance interactivity
│   │   chat_ui.py # Handle Chat page 
│   │   info_ui.py  # Handle Info page 
│   │   settings_ui.py # Handle Settings page 
│   │   sidebar_ui.py # Handle sidebar 
│   │   tools_ui.py  # Handle Tool page 
```

  - **Crafting Custom Agents**:
   
      Creating a new custom agent involves adding a dedicated file to the `agents_list` directory :
    
      * Navigate to `Omnitool_UI\agents\agents_list\` 
      * Create a `.py` file
      * Write a single class with an `initialize_agent` method that returns a `langchain.agents.AgentExecutor` object. 

      You can find a custom agent exemple in `agents_list` folder, or can't you ? Not so sure, you should check.     

  - **Crafting Custom Tools**:
   
      Creating a new custom tool involves adding a dedicated file to the `tools_list` directory. Here's a procedure to add a custom tool:

       - Navigate to `Omnitool_UI\tools\tools_list\`
       - Add a `.py` file in the folder 
       - Implement your tool class. If you don't need custom options, implement a simple function with a docstring and a return for          the chatbot. Files added to this folder will be automatically integrated into the app as a tool available for the chatbot.

      A sample tool class structure is provided below:
     

     ```python
      import streamlit as st
      from streamlit_elements import elements, mui, html
      import os 
      from storage.logger_config import logger
      from tools.base_tools import Ui_Tool

      class Testtool(Ui_Tool):
         name = 'Testtool'
         icon = '🌍'
         title = 'Test tool'
         description =  'This function is used so the human can make test, thank you to proceed, input : anything'

         def _run(self, a):
            # This function is executed by the chatbot when using tool
            st.success(a)
            logger.debug('During the test tool execution and with input : ' + a)
            return 'Success'

         def _ui(self):
            # This function is executed at the creation of the tool card in the tool page
            if "test_state" not in st.session_state: 
                  st.session_state.test_state = False

            def checkstate(value):
                  st.session_state.test_state = value['target']['checked']
                  if st.session_state.test_state is True : 
                     st.success('Find me at '+ Local_dir)

            # Expander placed outside (below) the card
            with mui.Accordion():
                  with mui.AccordionSummary(expandIcon=mui.icon.ExpandMore):
                     mui.Typography("Options")
                  with mui.AccordionDetails():
                     mui.FormControlLabel(
                        control=mui.Checkbox(onChange=checkstate,checked= st.session_state.test_state),
                        label="Try to change me !")
               
     ```

4. **Installation Methods**:

  **Anaconda install**
  
  1. **Clone the Repository**:
  
      Download zip file or 
  
  ```bash
  git clone https://github.com/americium-241/Omnitool_UI.git
  ```
   
  2. **Navigate to the Repository Directory**:
     
  ```bash
  cd ./Omnitool_UI
  ```
  
  Using virtual environment is highly recommanded:
  
  3. **Create a New Anaconda Environment**:
  
      Replace `your_env_name` with a name for your new environment.
  
  ```bash
  conda create --name your_env_name python=3.8
  ```
  
  4. **Activate the Environment**:
  
  ```bash
  conda activate your_env_name
  ```
  
  Requirements : 
  
  5. **Install Dependencies**:
  
      Ensure you have `pip` installed. Then, execute the following command:
  
  ```bash
  pip install -r requirements.txt
  ```
        
  Run app : 
  
  6. **Run the Streamlit App**:
  
     Once installed, initiate the application by navigating to the root directory and executing the following command to start              the Streamlit server:
     
   ```bash
   streamlit run Omnitool_UI.py
   ```
       
  **Docker-based Deployment**:
  
  For those familiar with Docker, a `docker-compose` configuration is provided for streamlined deployment:
      
  ```bash
  docker-compose up
  ```
  

     

