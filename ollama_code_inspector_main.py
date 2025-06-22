import streamlit as st
from streamlit_ace import st_ace

import ollama

def process_response(prompt):
    messages = [
        {"role": "system", "content": f"You are an AI python code inspector who helps the people in coding by reviewing their code this is the code of the user{prompt}  and analyse their code and explain them the code in a simplified manner"},
        {"role": "system", "content": f"if you find any error  in their code that is {prompt} solve those error and explain them how they can improve their code"},
        {"role": "system", "content": f"you are a python code inspector you can help only in python you are not familiar with other languages"}
        
    ]

    response = ollama.chat(model="llama3.2", messages=messages  ,stream=True
                           )
    
    
    return response
# 
def stream_parser(stream):
    for chunk in stream:
        yield chunk['message']['content']


# Center-align an image
# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:
#     st.image(r"C:\Users\moham\Downloads\WhatsApp_Image_2024-04-23_at_18.17.51_5f88427c-removebg-preview.png", 
#              caption="", 
#             width=350,
#              use_column_width=False,)

# Set colored page title
st.title(":red[🤖Python Code Inspector]")

# User input section
st.header(":orange[Enter Your Python Code]",divider='violet')
prompt = st_ace(language="python", theme="twilight", key="code_input", height=300, font_size=20)

# Button to trigger code review
if st.button("Review the Code"):
    st.markdown("<h2 style='color:blue;'>Review Result</h2>", unsafe_allow_html=True)
    response = process_response(prompt)
    st.write(stream_parser(response))

    
    st.write_stream(response)
    with st.chat_message("assistant"):
            stream_parser(response) 
    
    st.write(response)
   
   
   
    api_key ="your api key" 

    gemini.configure(api_key=api_key)
    model = gemini.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                system_instruction="""You are AI Assistant who helps the people in coding by 
                                revieing their code  andsolving the errors in them and providing suggestions on how to improve it.""")
    
    # Display the generated text
    generated_text =  model.generate_content(f"review this code {prompt} and check wether the code is correct or not if error found give them suggestion how to correct it")
    st.write_stream(generated_text)

   
