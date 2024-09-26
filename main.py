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

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content

        # Initialize chat history in session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

# Step 2: Chat with the DOM content
if "dom_content" in st.session_state:
    # Display chat history
    if st.session_state.chat_history:
        st.write("Chat History:")
        for message in st.session_state.chat_history:
            st.write(f"You: {message['question']}")
            st.write(f"AI: {message['answer']}")

    # Input for new question
    new_question = st.text_input("Ask something about the content")

    if st.button("Send"):
        if new_question:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, new_question)

            # Append the new question and result to chat history
            st.session_state.chat_history.append({
                "question": new_question,
                "answer": parsed_result
            })

            # Display the answer
            st.write(f"AI: {parsed_result}")
