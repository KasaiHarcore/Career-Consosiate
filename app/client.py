# In one work state, contain: CV_data, Chat History, Model
# Chat model: Weak AI (Less params). CV process: Strong AI (More params)

import gradio as gr

def message_and_history(input, history): 
    history = history or [] 
    s = list(sum(history, ())) 
    s.append(input) 
    inp = ' '.join(s) 
    output = "Auto spawn yes"
    history.append((input, output)) 
    return history, history 

block = gr.Blocks(theme = gr.themes.Monochrome())
with block as app: 
    gr.Markdown("""<h1><center>Demo Chat</center></h1>""") 
    chatbot = gr.Chatbot(show_label = False, scale = 10) 
    message = gr.Textbox(placeholder = "Start your first message...", show_label = False) 
    state = gr.State() 
    submit = gr.Button("SEND") 
    submit.click(message_and_history,  
                 inputs = [message, state],  
                 outputs = [chatbot, state]) 

