import streamlit as st

from src.ollama_chain import OllamaChain, OllamaRAGChain
from src.llama_cpp_chains import LlamaChain
from src.pdf_handler import extract_pdf
from src.vqa import answer_visual_question
from src.audio_processor import AudioProcessor
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from dotenv import load_dotenv
import os

load_dotenv()

audio_processor = AudioProcessor()

@st.cache_resource
def load_chain(_chat_memory):
    if st.session_state.pdf_chat:
        return OllamaRAGChain(_chat_memory)
    else:
        return OllamaChain(_chat_memory)


def file_uploader_change():
    if st.session_state.uploaded_file:
        if not st.session_state.pdf_chat:
            clear_cache()
            st.session_state.pdf_chat = True

        st.session_state.knowledge_change = True

    else:
        clear_cache()
        st.session_state.pdf_chat = False


def toggle_pdf_chat_change():
    clear_cache()
    if st.session_state.pdf_chat and st.session_state.uploaded_file:
        st.session_state.knowledge_change = True


def clear_input_field():
    # store the question
    st.session_state.user_question = st.session_state.user_input
    # clear the variable
    st.session_state.user_input = ""


def set_send_input():
    st.session_state.send_input = True
    clear_input_field()


def clear_cache():
    st.cache_resource.clear()


def initial_session_state():
    st.session_state.send_input = False
    st.session_state.knowledge_change = False


def main():
    # Initialize
    # Title
    st.title('OVERKILL LLM')
    chat_container = st.container()

    # sidebar
    # st.sidebar.title('Chat Session')

    # file upload
    st.sidebar.toggle('PDF Chat', value=False, key='pdf_chat', on_change=toggle_pdf_chat_change)
    uploaded_pdf = st.sidebar.file_uploader('Upload your pdf files',
                                            type='pdf',
                                            accept_multiple_files=True,
                                            key='uploaded_file',
                                            on_change=file_uploader_change)

    # Image upload
    uploaded_image = st.sidebar.file_uploader('Upload Images', type=['jpg', 'jpeg', 'png'], key='uploaded_image')

    # Audio upload
    uploaded_audio = st.sidebar.file_uploader('Upload Audio', type=['wav', 'mp3'], key='uploaded_audio')

    # Input objects
    user_input = st.text_input('Message OVERKILL', key='user_input', on_change=set_send_input)
    send_button = st.button('Send', key='send_button')

    # Session state
    if 'send_input' not in st.session_state:
        initial_session_state()
    # ----------------------------------------------------------------------------------------------------

    chat_history = StreamlitChatMessageHistory(key='history')

    with chat_container:
        for msg in chat_history.messages:
            st.chat_message(msg.type).write(msg.content)

    llm_chain = load_chain(chat_history)
    if st.session_state.knowledge_change:
        with st.spinner('Updating knowledge base'):
            llm_chain.update_chain(uploaded_pdf)
            st.session_state.knowledge_change = False

    # we use "or" operation here because user can press 'Enter' instead of 'Send' button
    if (send_button or st.session_state.send_input) and st.session_state.user_question != "":
        with chat_container:
            st.chat_message('user').write(st.session_state.user_question)
            
            if uploaded_image:
                image_path = os.path.join('./.cache/temp_files', uploaded_image.name)
                with open(image_path, 'wb') as f:
                    f.write(uploaded_image.getvalue())
                llm_response = answer_visual_question(image_path, st.session_state.user_question)
            elif uploaded_audio:
                audio_path = os.path.join('./.cache/temp_files', uploaded_audio.name)
                with open(audio_path, 'wb') as f:
                    f.write(uploaded_audio.getvalue())
                st.write(f"Processing audio file: {audio_path}")  # Debug statement
                st.session_state.user_question = audio_processor.audio_to_text(audio_path)
                st.write(f"Converted audio to text: {st.session_state.user_question}")  # Debug statement
                llm_response = llm_chain.run(user_input=st.session_state.user_question)
            else:
                llm_response = llm_chain.run(user_input=st.session_state.user_question)
            
            st.session_state.user_question = ""
            st.chat_message('ai').write(llm_response)

            # Convert response to speech and play it
            audio_file = audio_processor.text_to_speech(llm_response)
            audio_bytes = open(audio_file, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3')


if __name__ == '__main__':
    main()