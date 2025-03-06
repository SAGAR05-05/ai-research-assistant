import streamlit as st
import requests 

st.title("🧠 NLP Research Assistant")

# Select function
option = st.selectbox("Choose a function:", ("Question Answering", "Summarization"))

# Question Answering Section
if option == "Question Answering":
    st.subheader("Ask a Question Based on Context")
    context = st.text_area("Enter the research paper text or context:")
    question = st.text_input("Enter your question:")
    
    if st.button("Get Answer"):
        if context and question:
            try:
                response = requests.post("http://127.0.0.1:5000/qa/", json={"question": question, "context": context})
                st.write("🔍 Debugging Response:", response.text)  # Show raw API response
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found.")
                    st.success(f"**Answer:** {answer}")
                else:
                    st.error(f"API Error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API request failed: {e}")
        else:
            st.warning("⚠️ Please enter both context and question.")

# Summarization Section
elif option == "Summarization":
    st.subheader("Summarize Research Papers")
    text = st.text_area("Enter the research text:")

    if st.button("Summarize"):
        if text:
            try:
                response = requests.post("http://127.0.0.1:5000/summarize/", json={"text": text})
                st.write("🔍 Debugging Response:", response.text)  # Show raw API response
                if response.status_code == 200:
                    summary = response.json().get("summary", "No summary found.")
                    st.success(f"**Summary:** {summary}")
                else:
                    st.error(f"API Error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API request failed: {e}")
        else:
            st.warning("⚠️ Please enter some text to summarize.")
