import streamlit as st
import inspect
import ast

import sys 
import os 
import importlib




def monitorFolder(folder_path):
    """Monitor a folder path and return the list of .py files inside"""

    if folder_path not in sys.path:
         sys.path.append(folder_path)

    # List all .py files in the tools directory (excluding __init__.py).
    python_files = [f[:-3] for f in os.listdir(folder_path) if f.endswith('.py') and f != "__init__.py"]

    # Dynamically import all modules from the tools directory.
    monitored_files=[]
    for f in python_files: 
        try : 
            monitored_files.append(importlib.import_module(f))
        except Exception as e : 
            st.error('Cannot import '+f+ 'file, with error : '+str(e))
    return monitored_files

def get_class_func_from_module(module):
    """Filter the classes and functions found inside a given module"""
    members = inspect.getmembers(module)
    # Filter and store only functions and classes defined inside module
    fonctions = []
    classes = []
    for name, member in members:
        if inspect.isfunction(member) and  member.__module__ == module.__name__ :
            try :
                doc=member.__doc__+' check doc'
                fonctions.append((name, member))
            except Exception as e: 
                st.error('Cannot import '+name+'function because it lacks a doctring')
            
        if inspect.isclass(member) and  member.__module__ == module.__name__ :
            classes.append((name, member))
        
    return classes,fonctions



def has_docstring(function_node):
    """
    Check if the provided function node from AST has a docstring.
    """
    if isinstance(function_node.body[0], ast.Expr) and isinstance(function_node.body[0].value, ast.Str):
        return True
    return False

def evaluate_function_string(func_str):
    """
    Evaluates the provided function string to check:
    1. If it runs without errors
    2. If the function in the string has a docstring
    
    Returns a tuple (runs_without_error: bool, has_doc: bool, toolname: str)
    """
    try:
        parsed_ast = ast.parse(func_str)
        
        # Check if the parsed AST contains a FunctionDef (function definition)
        if not any(isinstance(node, ast.FunctionDef) for node in parsed_ast.body):
            return False, False, None

        function_node = next(node for node in parsed_ast.body if isinstance(node, ast.FunctionDef))
        
        # Extract tool name
        tool_name = function_node.name

        # Compiling the function string
        compiled_func = compile(func_str, '<string>', 'exec')
        exec(compiled_func, globals())

        # Check for docstring
        doc_exist = has_docstring(function_node)

        return True, doc_exist, tool_name

    except Exception as e:
        return e, False, None

# Usefull general functions
def executecode(code):
    """Execute code inside the streamlit app python console"""
    try:
        st.session_state.executed_code.append(code)
        exec(code, globals(), locals())
    except Exception as e:
        st.error(f"An error occurred while executing the code: {e}")
        
        return f"An error occurred while executing the code: {e}"


