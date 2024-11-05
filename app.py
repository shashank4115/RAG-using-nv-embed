import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplate import css, bot_template, user_template
from langchain_community.chat_models import ChatOllama

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_vectorstore(text_chunks):
    #Replace here
    #embeddings = HuggingFaceBgeEmbeddings(model_name='hkunlp/instructor-xl')
    #vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    #return vectorstore
    model_kwargs = {
        'trust_remote_code':True
        }
    encode_kwargs = {'normalize_embeddings': True,
                     'batch_size': 2,
                    }
    embeddings = HuggingFaceBgeEmbeddings(model_name="nvidia/NV-Embed-v2",model_kwargs=model_kwargs,encode_kwargs=encode_kwargs,show_progress=True)
    vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

#If you have a powerful enough system to build using nv-embed replace the following code in the location *Replace here*

#model_kwargs = {
    #'trust_remote_code':True
    #}
#encode_kwargs = {'normalize_embeddings': True}
#embeddings = HuggingFaceBgeEmbeddings(model_name="nvidia/NV-Embed-v2",model_kwargs=model_kwargs,encode_kwargs=encode_kwargs,show_progress=True)
#vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
#return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOllama(model="llama3.1", temperature=0.2)
    memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_query(user_query):
    response = st.session_state.conversation({'question': user_query})
    st.session_state.chat_history = response['chat_history']

    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 ==0:
            st.write(user_template.replace("{{MSG}}",msg.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",msg.content),unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="ChatBot")
    
    st.write(css,unsafe_allow_html=True)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    st.header("ChatBot")
    user_query = st.text_input("Message your Docs")
    if user_query:
        handle_user_query(user_query)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get text chunks
                text_chunks = get_text_chunks(raw_text)
                
                # create vector store with faiss
                vectorstore = create_vectorstore(text_chunks)
                print('vector store created')
                
                #create a conversation
                st.session_state.conversation = get_conversation_chain(vectorstore)
                    
if __name__ == '__main__':
    main()