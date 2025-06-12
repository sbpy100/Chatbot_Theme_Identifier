import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Document Research & Theme Identifier", layout="wide")
st.title("📄 Document Theme Identifier Chatbot")
st.header("Upload Your Documents")
uploaded_files = st.file_uploader(
    "Upload PDFs or images", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True
)

if st.button("Upload Files"):
    if uploaded_files:
        with st.spinner("Uploading and processing..."):
            files = [("files", (file.name, file.getvalue())) for file in uploaded_files]
            try:
                res = requests.post("http://localhost:5000/upload", files=files)
                if res.status_code == 200:
                    st.success("Files processed successfully.")
                else:
                    st.error(f"Upload failed. Status code: {res.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload at least one file.")

# Question Section
st.header("Ask a Question About the Documents")
question = st.text_input("Enter your question (e.g., What are the key themes?)")

if st.button("Submit Question"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Getting answer..."):
            try:
                res = requests.post("http://localhost:5000/query", json={"question": question})

                if res.status_code != 200:
                    st.error(f" Backend error: {res.status_code}")
                else:
                    data = res.json()

                    # Document Section
                    st.subheader("📑 Individual Document Answers")

                    table_data = []
                    for doc in data["citations"]:
                        doc_id = doc["doc_id"]
                        answer = doc["text"].replace("\n", " ")[:500] + "..."
                        citation = doc["citation"]  # now like "Page 2"
                        table_data.append([doc_id, answer, citation])

                    df = pd.DataFrame(table_data, columns=["Document ID", "Extracted Answer", "Citation"])
                    st.dataframe(df, use_container_width=True)

                    st.subheader("🧠 Synthesized Theme Summary")
                    st.success(data.get("themes", "No summary returned."))

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

