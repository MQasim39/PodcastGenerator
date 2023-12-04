import os 
import logging

import streamlit as st

from _langchain import get_response
from _elevenlabs import with_custom_voice, with_premade_voice, get_voices

#Configure the logger ot help debugging
logging.basicConfig(format= "\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

#Configuring the streamlit page and its state
st.set_page_config(page_title="LLM Podcast", page_icon="🎧")

#Now we will initialize the Streamlit state. 
# It allows us 2 things: to store the app's state and usage in different parts of the app
if "podcast_generate" not in st.session_state:
    st.session_state.podcast_generate=""
if "output_file_path" not in st.session_state:
    st.session_state.output_file_path=""
if "input_file_path" not in st.session_state:
    st.session_state.input_file_path=""
if "text_error" not in st.session_state:
    st.session_state.text_error=""
if "visibility" not in st.session_state:
    st.session_state.visibility="visible"


#To allow for responsivness on different devices here is some custom CSS
st.write("""
<style>
[data-testid="column"]{
        width: calc(50%-1rem);
        flex: 1 1 calc(50%-1rem);
        min_width: calc(50%-1rem);
}         
</style>
""", unsafe_allow_html=True)

#Time to render the streamlit page
#The title for this app
st.title("Podcast Generator")

#A short description of the app
st.markdown("This web app is built with langchain and elevenlabs to generate podcasts upon prompting")

#Adding an option to upload voice file
File = st.file_uploader(label="Upload file",type=["mp3",])
if File is not None:
    Filename = "sample.mp3"
    with open(Filename,"wb") as f:
        f.write(File.getbuffer())
    st.session_state.input_file_path = "sample.mp3"

#Creating a dropdown menu for choosing a specific voice
Voice = st.selectbox("Choose your voice ", (v for v in get_voices()))

#Creating columns for better UX
Col_1, Col_2 = st.columns(2)

#First column is for the podcaster/host
with Col_1:
    podcaster = st.text_input(label="Podcaster", placehoolder="Ex. Joe Rogan")

#Second column is for the guest
with Col_2:
    guest = st.text_input(label="Guest", placeholder="Elon Musk")

#Text area for user to prompt the podcast topic
prompt = st.text_area(label="Podcast Topic", placeholder="For example Elon Musk joins Joe Rogan to talk about weed and the uses of it in Neuralink"
                      ,height=100)

#Now we define two important functions: generate_podcast and generate_podcast_text
#generate_podcast_text will be used in the generate_podcast function
def generate_podcast_text(Prompt, Podcaster, Guest):
    return get_response(prompt=Prompt,podcaster=Podcaster,guest=Guest)

def generate_podcast(voice, prompt, podcaster, guest):
    if prompt == "":
        st.session_state.text_error = "Please enter a prompt"

        return
    
    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query....."):
            g_podcast = generate_podcast_text(prompt=prompt,podcaster=podcaster,guest=guest)

            st.session_state.podcast_generate = (g_podcast)

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process the query....."):

            if st.session_state.input_file_path != "":
                audio_path = with_custom_voice(podcaster=podcaster, guest=guest, Description=prompt, 
                                               prompt=st.session_state.podcast_generate, file_path=st.session_state.input_file_path)

                if audio_path != "":
                    st.session_state.output_file_path= audio_path
                
            else:
                audio_path = with_premade_voice(prompt=st.session_state.podcast_generate,voice=voice)
        

                if audio_path != "":
                    st.session_state.output_file_path  = audio_path



#The button which will geenrate the podcast when clicked
st.button(
    label="Generate Podcast", #button name
          help = "Click the button to generate podcast of your choice", #when hovering upon the button this text appears
          key="generate_podcast", #key to generate the podcast
          type="primary", #default red button by Streamlit
          on_click=generate_podcast, #function to be called on clicking
          args=(Voice, prompt, podcaster, guest) #arguments to be passed to the function
        )

#Now we check session states
text_spinner_placeholder=st.empty()

if st.session_state.text_eror:
    st.error(st.session_state.text_erior)

#Output the trnscription of the podcast generated
if st.session_state.podcast_generate:
    st.markdown("""---""")
    st.subheader("Read Podcast")
    st.text_area(label="You may read the podcast's audio while it is being generated.", 
                 value=st.session_state.podcast_generate)
    
#Output the audio generated
if st.session_state.output_file_path:
    st.markdown("""---""")
    st.subheader("Listen to the generated Podcast")

    with open(st.session_state.output_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/mp3", start_time=0)


