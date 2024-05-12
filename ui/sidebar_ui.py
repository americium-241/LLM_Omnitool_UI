import streamlit as st
from datetime import datetime
                          
def sidebar():
    with st.sidebar:
        st.markdown("---")  # Separator
        
        if st.button("Start New Session", use_container_width=True): # !!!!! BAD comportement pas bon
            st.session_state.session_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            st.session_state.selected_page = 'Chat'
           
    
        st.markdown("---")

        session_id_list = st.session_state.storage.get_all_sessions()
        st.session_state.session_name=st.session_state.storage.get_all_sessions_names()
        session_expander = st.expander(label='Sessions', expanded=True)

        with session_expander:
            if session_id_list:
               
                for session_id in reversed(session_id_list):

                    button_container=st.empty()
                    session_name = st.session_state.session_name.get(session_id, session_id)
                    col1, col2 = st.columns([5,1])
                    with button_container:
                        with st.container():
                            if st.button(session_name, use_container_width=True):
                                st.session_state.session_id = session_id
                                col1.text_input('Rename', key='new_name',placeholder='Rename : ' + str(session_id)[5:] , label_visibility="collapsed",on_change=change_session_name)
                                col2.button('❌', use_container_width=True,on_click=del_session)
        st.session_state.token_count_placeholder=st.empty()
                             
def del_session():
        st.session_state.storage.delete_session(st.session_state.session_id)
def change_session_name():
     st.session_state.storage.save_session_name( st.session_state.session_id , st.session_state.new_name)
         
