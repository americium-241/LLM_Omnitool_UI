import streamlit as st
from streamlit_extras.stateful_button import button
from streamlit_ace import st_ace
from streamlit_elements import elements, mui, html

import os

from storage.logger_config import logger
from tools.utils import evaluate_function_string
from tools.tool_manager import ToolManager
from time import sleep
Local_DIR= os.path.dirname(os.path.realpath(__file__))


def tool_settings():
    st.session_state.selected_tools = []
   
    tool_search=st.text_input('Filter',placeholder='Filter tools',key='tool_search',label_visibility="collapsed")
    if tool_search !='':   
        st.session_state.tool_filtered=[tool for tool in st.session_state.tool_manager.get_tool_names() if tool_search in tool or tool_search in st.session_state.tool_manager.tools_description[tool]  ]
    else: 
        st.session_state.tool_filtered = st.session_state.tool_manager.get_tool_names()
    with elements(key="cards"):
        with mui.Grid(container=True, spacing=2):
            for tool_name in st.session_state.tool_filtered:
                tool=st.session_state.tool_manager.get_selected_tools([tool_name])[0]
                make_mui_card(tool)
               
        st.session_state.tools = st.session_state.tool_manager.get_selected_tools(st.session_state.selected_tools)
        print('----------------------',st.session_state.tools )
        logger.debug('Tools selected : '+str(st.session_state.selected_tools))

def defautui():
    pass
def make_mui_card(tool):
    # tool is a base_tool
    #This is redundant but it displays what can be changed
    
    if not hasattr(tool, 'icon') : 

        tool_name = tool.name 
        tool_icon = '🔧 ' if 'StructuredTool' in tool.__class__.__name__ else '🦜️ '
        tool_link =r'https://github.com/americium-241/Omnitool_UI/tree/master'if 'StructuredTool' in tool.__class__.__name__ else r'https://integrations.langchain.com/tools' 
        tool_title = tool_name
        tool_description = tool.description 
        tool_ui = defautui
    
    else:

        tool_name = tool.name 
        tool_icon = tool.icon 
        tool_link = tool.link 
        tool_title = tool.title 
        tool_description = tool.description 
        tool_ui = tool._ui 
    

    is_clicked = st.session_state.clicked_cards.get(tool_name, False)
    # Set border highlight if card is clicked
    border_style = "3px solid rgb(255,75,75)" if is_clicked else None
    if is_clicked :
        st.session_state.selected_tools.append(tool_name)
        print(tool_name)
    with mui.Grid(item=True, xs=4):
        # Card content without expander
        threshold_length = 130  # Set your desired threshold length
        # Determine if hover styles should be applied based on description length
        hover_styles = {}
        if len(tool_description) > threshold_length:
            hover_styles = {
                "height": "auto",  # Adjust height dynamically based on content
                ".description": {
                "maxHeight": "none",
                "overflow": "visible",
                "transition": "0.1s"}}

        with mui.Card(elevation=3, variant="outlined", 
            sx={
            "border": border_style, 
            "cursor": "pointer", 
            "height": "150px", 
            "&:hover": hover_styles,
            "transition": "0.1s"}, 
            onClick=make_card_click_handler(tool_name), 
            className="card-hover"):

            with mui.CardContent(style={"padding": "10px"}):
                # Container for the first two Typographies
                with mui.Box(style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}):
                    # First Typography (name + icon)
                    mui.Typography(tool_icon + tool_title[:11], variant="h5", component="div", style={"display": 'inline-block', "font-size": "21px"})
                    
                    # Link Typography pushed to the right
                    with mui.Link(href=tool_link, target="_blank", rel="noopener noreferrer", sx={'textDecoration': 'none', 'color': 'inherit', 'marginLeft': 'auto'}):
                        mui.Typography('🔗', style={"display": 'inline-block', "font-size": "20px"})
                
                # Description Typography below the flex container
                mui.Typography(tool_description, variant="body2", color="text.secondary", sx={"overflow": "hidden", "maxHeight": "100px", "transition": "0.15s"}, className="description")

        tool_ui()

# Function to handle card click
def handle_card_click(event, tool_name):
    st.session_state.clicked_cards[tool_name] = not st.session_state.clicked_cards.get(tool_name, False)
   
def make_card_click_handler(tool_name):
    def handler(event):
        handle_card_click(event, tool_name)
    return handler

def add_tool():
    '''Sketchy way to add a tool by appending code to a monitored file : newtools.py. Interesting to allow chatbot to make its own tools'''
    if button("Create tool",key='button_create_tool'):
        with st.form("my_form"):
            st.write("Create new tool")
            new_tool_name = st.text_input("Tool file name")
            new_tool_function= st_ace('',theme='tomorrow_night',language='python',auto_update =True,key='menu_geneprompt',placeholder='def function_name(): \n    """Tool description (be accurate)"" \n    tool code...')
            submitted = st.form_submit_button("Submit")
            if submitted:
                run,doc,name=evaluate_function_string(new_tool_function)
                
                if run is True and doc is True :
                    tools_path = os.path.join(Local_DIR,"..", "tools", "tools_list", f"{new_tool_name}.py")
                    f = open(tools_path, "w") 
                    f.write(new_tool_function)
                    f.close()
                    st.session_state.tool_manager = ToolManager()
                    st.session_state.tool_list = st.session_state.tool_manager.structured_tools
                    st.success('Tool created')
                    sleep(1)
                    st.rerun() 
                else :
                    st.error('Error in function :'+str(run)+' \n Add a \""" docstring \""" below function def')
                    st.stop()
                

def tools_page():
    tool_settings()
    add_tool()
    
 