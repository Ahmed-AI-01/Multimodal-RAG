# Multimodal-RAG

![Project Summary](path/to/your/image.png)

An AI-powered chat application using text, audio, and images for context-aware responses. It integrates language models and vector databases to enhance retrieval-augmented generation (RAG) capabilities, making it a versatile tool for intelligent conversations.

## Features

- **Text to Speech**: Convert text responses to speech using gTTS.
- **Speech to Text**: Process and transcribe audio files using `speech_recognition` and `Wav2Vec2`.
- **Visual Question Answering**: Answer questions based on uploaded images using BLIP.
- **PDF Knowledge Base**: Upload PDF files to enhance the knowledge base for more accurate responses.
- **Context-Aware Responses**: Use conversation history to provide more relevant answers.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Multimodal-RAG.git
    cd Multimodal-RAG
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a [.env](http://_vscodecontentref_/1) file in the root directory and add your Pinecone API key:
        ```
        PINECONE_API_KEY=your_pinecone_api_key
        ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Interact with the chat application by uploading PDFs, images, or audio files and typing your questions.

## Project Structure

- [app.py](http://_vscodecontentref_/2): Main application file for Streamlit.
- [audio_processor.py](http://_vscodecontentref_/3): Handles audio processing for speech-to-text and text-to-speech.
- [llama_cpp_chains.py](http://_vscodecontentref_/4): Implements Llama-based language model chains.
- [ollama_chain.py](http://_vscodecontentref_/5): Implements Ollama-based language model chains and RAG chains.
- [pdf_handler.py](http://_vscodecontentref_/6): Handles PDF loading and splitting.
- [utils.py](http://_vscodecontentref_/7): Utility functions, including configuration loading.
- [vectorstore.py](http://_vscodecontentref_/8): Manages vector database setup and indexing.
- [vqa.py](http://_vscodecontentref_/9): Handles visual question answering and audio transcription.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](http://_vscodecontentref_/10) file for details.

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [Pinecone](https://www.pinecone.io/)
- [Streamlit](https://streamlit.io/)
- [gTTS](https://gtts.readthedocs.io/)
- [Wav2Vec2](https://huggingface.co/facebook/wav2vec2-base-960h)
- [BLIP](https://huggingface.co/Salesforce/blip-vqa-base)
