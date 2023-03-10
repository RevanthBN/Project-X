import streamlit as st
import os
import emoji
import requests
import json
import random

# Setting the page config
st.set_page_config(page_title="DeScribe AI")
# openai.api_key = os.getenv("OPENAI_API_KEY")

# v1 of the prompts
dict_v1 = {"shakespearean style": "Your task is to rewrite the following text in Shakespearean style. \
        Please provide a response that captures the essence of the original text while using language and phrasing typical of Shakespeare's works. \
        Please note that your response should be flexible enough to allow for various creative and relevant interpretations, as long as they are consistent with Shakespearean style: \n",
        "reduce": "Your task is to rewrite a reduced and summarized version of a given passage while retaining important information, statistics, or figures mentioned in the original passage.\
         The length of the output should be one-third of the original passage. Before writing the reduced version, you should carefully read and analyze the original text to identify key points that must be retained. \
        You should then use your own words to summarize these points while maintaining accuracy and clarity. Please note that you should not copy sentences directly from the original passage.",
        "rewrite":"Your task is to create a well-written and accurate version of a given text while retaining all key elements and without changing the meaning. Your goal is to make the text more concise and clear by using active voice, clear and specific language, and avoiding redundant or unnecessary words. You should retain at least 75% of the original text and maintain the tone and style of the original text.\
         Your response should be flexible enough to accommodate different types of texts with varying levels of complexity."}
# v2 of the prompts
dict_v2 = {"reduce": """Given below is an example of how to reduce the input text without losing the important information but keeping it precise: \
          # Input: Liberalism is founded on the belief in human liberty. Unlike rats and monkeys, human beings are supposed to have free will. This is what makes human choices the ultimate moral and political authority in the world. If you happened to be amid the riots in Washington on the day after Martin Luther King was assassinated, or in Paris in May 1968, or at the Democratic party’s convention in Chicago in August 1968, you might well have thought that the end was near. While Washington, Paris and Chicago were descending into chaos, the Soviet system seemed destined to endure forever. Yet 20 years later it was the Soviet system that collapsed. The clashes of the 1960s strengthened liberal democracy, while the stifling climate in the Soviet bloc presaged its demise.\ 
          Reduced output: Human liberty defines liberalism. The concept of free will is exclusive to humans and gives us moral and political authority. During the 1960s, liberalism was undergoing a crisis in the West. Contrasted with the chaos in liberalism, the illiberal system in the Soviet Union seemed to be flourishing. However, in a matter of two decades, it was the Soviet system that collapsed, while liberal democracy strengthened by adapting itself. # \
          Using the above example, rewrite a reduced summarized version of the following text keeping in mind the following rules: \
          - Keep the length of the output to one-third of the original passage. \
          - Before writing the reduced version, keep the important information intact while trying to retain any statistics or figures mentioned in the original passage. \
          - Don't use the same sentences in the original passage. Input:\n """,
          "shakespearean style": """ Input: "The first successful powered flight by humans occurred on December 17, 1903, by the Wright brothers in North Carolina, USA." \
          Output: "Hark! On December 17th in the year of our Lord 1903, in the land of North Carolina, USA, the Wright brothers did achieve a feat never before seen by man! A wondrous powered flight, soaring through the heavens, achieved by human hands! Oh, the glory and wonder of that day, when men did take to the air like eagles!" \
          Dear ChatGPT, for this task, please imagine you are a language model that has been trained on a vast amount of text but has never seen any Shakespearean text before. Your task is to understand the above example and rewrite the following text in Shakespearean-style:  Your response should capture the essence of the original text while using language and phrasing typical of Shakespeare's works, without any explicit instruction on how to do so. \n """,
           "rewrite":"""Given below is an example of how text is rewritten for any given input. 
        Input: The biggest issue with stereotyping today would be in the business world. Lets take hiring new employees as the main problem. It may not always be race that is a deciding factor as much as it is sex. Some jobs a woman may be hired over a man due to her nurturing nature. On the other hand a man may be hired over a woman due to the fact that he may be stronger. In some cases the sex of a person may be the deciding factor on whether they even get a call. \n
        Output: Much of today’s stereotyping takes place in the business world, particularly when hiring employees. Surprisingly often, sex is more of a deciding factor than race. For some jobs women may be hired over men because they are seen as nurturers; on the other hand, men may be preferred because of their physical strength. \n
        Understanding how this is done, rewrite the following text without changing the meaning and keeping the details intact:"""}
# v3 of the prompts
dict_v3 = {"rewrite":["The objective of this task is to produce a rewritten version of a given text that retains all relevant details and does not alter the meaning. Your aim is to make the text more concise and clear by using appropriate phrasing and sentence structure, avoiding redundant or unnecessary words, and maintaining the tone and style of the original text. Use active voice and clear language, and retain at least 75% of the original text. Your response should be flexible enough to handle different types of texts with varying levels of complexity.", 
 "Your task is to rephrase a given text while retaining all pertinent information and ensuring that the meaning remains unchanged. Your objective is to make the text more concise and clear by utilizing active voice, clear and precise language, and avoiding redundant or unnecessary words. You should retain at least 75% of the original text and maintain the tone and style of the original text. Your response should be adaptable to different types of texts with varying levels of complexity.",
 "You are required to rewrite a given text while retaining all essential details and without altering the meaning. Your goal is to make the text more concise and clear by using active voice, clear and specific language, and avoiding redundant or unnecessary words. Retain at least 75% of the original text and maintain the tone and style of the original text. Your response should be flexible enough to accommodate different types of texts with varying levels of complexity."],
 "reduce":["You are required to condense a given passage into a shorter version, while preserving vital information, facts, or figures. The new version should be one-third the length of the original passage. Before starting, you must thoroughly examine and comprehend the original text to identify critical points that must not be left out. Then, you should summarize these points in your own words, ensuring accuracy and clarity. Avoid copying sentences directly from the original passage.",
           "Your assignment is to create a concise and summarized version of a given passage, keeping important information, statistics, or figures intact. The length of your output should be one-third of the original passage. First, thoroughly read and analyze the original text to identify crucial points that cannot be omitted. Then, using your own words, summarize these points while ensuring that the information is accurate and comprehensible. Avoid directly copying sentences from the original passage.",
           "The objective is to condense a provided passage into a shorter version while preserving crucial information, statistics, or figures. Your output should be one-third the length of the original passage. To begin, carefully read and comprehend the original text to identify important points that must be retained. After that, use your own words to summarize these points, ensuring that the information is accurate and comprehensible. Do not directly copy sentences from the original passage."],
 "shakespearean style":  ["Compose a Shakespearean-style response to the given text, dear ChatGPT. The goal is to maintain the essence of the original while utilizing phrasing and language akin to the bard's own. Be sure to allow for some creative interpretation, so long as it fits the established style.",
"Task thyself with transmuting the following text into the tongue of Shakespeare. Make certain the core of the text remains, yet is transformed into phrasing typical of the bard's works. Be creative and interpretive, but stay within the bounds of the established style.",
"Lend thy quill, dear ChatGPT, and rewrite this text in the grandeur of Shakespeare's prose. Be true to the essence of the original, but do not hesitate to add thine own spin in the style of the bard.",
"Hark, ChatGPT, and take up the challenge of rewriting this text in the language and phrasing of Shakespeare. Let the essence of the original ring true, while using your wit and creativity to transform it into the style of the bard."]      }

# results dict
result_header = ["V1 - using improved prompts","V2 - using Few shot learning", "V3 - ChatGPT-generated prompts" ]

# Remove any emoji used in the front-end
def strip_emoji(text_str):
    return emoji.replace_emoji(text_str).strip().lower()

# Function to construct the prompt based on the given action/tone/input_text combo
def construct_prompt(action, tone, input_text):
    tone = strip_emoji(tone)
    action = strip_emoji(action)
    # Take care of the prompt based on all of the variations available
    prompt_1 = dict_v1[action]+ "\n"
    prompt_2 = dict_v2[action]+ "\n"
    prompt_3 = random.choice(dict_v3[action])+ "\n"
    prompts_all = [prompt_1, prompt_2, prompt_3]
    # Adding the tone if needed and stitching the input text
    if tone != "default":
        add_tone = "Now add a {} tone to the written text.".format(tone)
        prompts = [prompt+ 'Text: \n"{}" \n'.format(input_text) + add_tone for prompt in prompts_all]
    else:
        prompts = [prompt+ 'Text: \n"{}" \n'.format(input_text) + add_tone for prompt in prompts_all]
    return prompts
    
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
        st.header("Results generated: 😎")
        prompts=construct_prompt(action=set_action,tone=set_tone,input_text=input)
        for idx, prompt in enumerate(prompts):
            inputs = {"prompt":prompt,"key":st.secrets["OPENAI_API_KEY"]}
            response = requests.post(url="https://openai-endpoint.onrender.com/query",data=json.dumps(inputs))
            st.write('**{}**'.format(result_header[idx]))
            st.write(response.json()['output'].strip())
        
        if show_stats:
            st.write('**Usage Stats** 📈')
            st.json(response.json()['stats'])
            
    except:

        st.error("An error occured! Please shorten your prompt to 4097 tokens and try again!",icon="🚨")
