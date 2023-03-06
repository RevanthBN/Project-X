import openai
import streamlit as st
import os
import emoji
import requests
import json

# Setting the page config
st.set_page_config(page_title="DeScribe AI")
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Remove any emoji used in the front-end
def strip_emoji(text_str):
    return emoji.replace_emoji(text_str).strip().lower()

# Function to construct the prompt based on the given action/tone/input_text combo
def construct_prompt(action, tone, input_text):
    tone = strip_emoji(tone)
    action = strip_emoji(action)
    # Take care of the prompt when in shakespearean style
    if action == "shakespearean style":
        prompt = "rewrite the following text in shakespearean style"
    # Take care of the other prompts as it is
    else:
        prompt = action + " the following text"
    # Adding the tone if needed and stitching the input text
    if tone != "default":
        prompt = prompt+ " with a {} tone:\n".format(tone) + input_text
    else:
        prompt = prompt + ":\n" + input_text
    return prompt
    
# Some html formatting of the background
html_temp = """
                <div style="background-color:{};padding:1px">
                
                </div>
                """

# Creating the sidebar for additional information
with st.sidebar:
    st.markdown("""
    # About 
    **DeScribe AI** is a helper tool ⛏ built on GPT-3 to perform summarization of text with styling. 
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    # What does it do? 🤔
    **DeScribe AI** can perform the following actions on **text snippets**  sent to it.
    - Rewrite and reduce text.
    - Change the style of the input text.
    - Rewrite the text with a custom tone sent from the front end.
    """)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown("""
    Made by [@revanth_banala](https://www.revanthbanala.com/)
    """,
    unsafe_allow_html=True,
    )

# Main display elements
st.markdown("""
    # DeScribe AI 🤖 
    """)
input = st.text_area(label="**Enter your text here: 👇** ", value="", height=250 )

set_action = st.selectbox(
            "**Choose the action to be taken on the text: 📝**" ,
            ["Rewrite 💭", "Reduce 🔏", "Shakespearean style ✍️"],
            help="Based on the action, the text will be rewritten, reduced or written in the style of Shakespeare!", )

# # Potential advanced feature to set a parameter to control how concise the result is (i.e, how many words)
# if set_action == "Reduce 🔏":
#     n_words = st.slider("How many words in the reduction?")

set_tone = st.radio(
            "**Choose the tone 🎷 to rewrite the text with:**",
            ["Default 📝", "Assertive 🙂", "Persuasive 😎", "Casual 😀", "Witty 😛", "Serious 😐"],
            help="The text will be rewritten in the chosen tone, the default would be the generic tone set.",
            horizontal=True
        )
show_stats = st.checkbox('Show usage stats 📈')
submit = st.button('Let the magic begin! 🪄')

if submit:
    try:
        prompt=construct_prompt(action=set_action,tone=set_tone,input_text=input)
        inputs = {"prompt":prompt,"key":st.secrets["OPENAI_API_KEY"]}
        response = requests.post(url="https://openai-endpoint.onrender.com/query",data=json.dumps(inputs))
        # response = openai.Completion.create(
        # model="text-davinci-003",
        # ,
        # temperature=0.7,
        # max_tokens=256,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0
        # ).choices[0]["text"].strip()
        st.write('**Summarized text:** 😎')
        st.write(response.json()['output'].strip())
        if show_stats:
            st.write('**Usage Stats** 📈')
            st.json(response.json()['stats'])
            
    except:

        st.error("An error occured! Please shorten your prompt to 4097 tokens and try again!",icon="🚨")
