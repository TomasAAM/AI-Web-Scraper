import streamlit as st
from scrape import *
from parse import parse_with_ollama

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        
        st.write("Scraping the website...")

        # Scrape the website
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)
        df = cleaned_to_csv(cleaned_content)
        print(df)
        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = df

        # Initialize chat history in session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.dataframe(df)

# Step 2: Chat with the DOM content
if "dom_content" in st.session_state:
    # Mostrar historial de chat si existe
    if st.session_state.chat_history:
        st.write("Historial de Chat:")
        for message in st.session_state.chat_history:
            st.write(f"Tú: {message['question']}")
            st.write(f"AI: {message['answer']}")

    # Entrada para una nueva pregunta
    new_question = st.text_input("Haz una pregunta sobre el contenido")

    if st.button("Enviar"):
        if new_question:
            st.write("Analizando el contenido...")

            # Parsear el contenido con Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content.to_string())
            parsed_result = parse_with_ollama(dom_chunks, new_question)

            # Añadir la nueva pregunta y el resultado al historial de chat
            st.session_state.chat_history.append({
                "question": new_question,
                "answer": parsed_result
            })

            # Mostrar la respuesta
            st.write(f"AI: {parsed_result}")

 