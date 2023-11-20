import streamlit as st
import pandas as pd
import numpy as npb
import os
import asyncio
import string as str
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

path_root = r"C:\Users\user\Sains Data\Text Mining\Destinasi"
path_source = r"C:\Users\user\Sains Data\Text Mining\Source"
path_tfidf = os.path.join(path_root,"TF-IDF")

def search_text_in_directory(query, path_tfidf):
    results = []
    for root, dirs, files in os.walk(path_root):
        if 'TF-IDF' in dirs:
            dir_tfidf = os.path.join(root, 'TF-IDF')
            for root_tf, dirs_tf, files_tf in os.walk(dir_tfidf):
                for file_tf in files_tf:
                    if file_tf.endswith('.txt'):
                        file_path = os.path.join(root_tf, file_tf)
                        with open(file_path, "r", encoding="utf-8") as file:
                            lines = file.readlines()
                            for line in lines:
                                parts = line.strip().split(": ")
                                if len(parts) == 2:  # Check if there are two parts
                                    keyword, tfidf = parts
                                    if query in keyword:
                                        results.append((file_tf,keyword, tfidf))
    # Sort results by TF-IDF value in descending order
    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)

    return sorted_results


def read_docx(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Pencarian
search_query = st.text_input("Cari teks:")
if st.button("Cari"):
    if search_query:
        results = search_text_in_directory(search_query, path_tfidf)
        if results:
            st.success("Hasil Pencarian:")
            tfidf_data=[]
            
            for i, result in enumerate(results, 1):  # Start index at 1
                file_path, keyword, tfidf = result
                st.subheader(f"Hasil {i}:")
                st.write(f"File: {file_path}\n")
                st.write(f"Keyword: {keyword}\n")
                st.write(f"TF-IDF: {tfidf}\n")
                
                file_path = file_path.replace("tfidf_", "")
                docx_path = file_path.replace('.txt', '.docx')
                split_folder = docx_path.split('_')
                split_folder = split_folder[0]
                docx_path_source = os.path.join(path_source,split_folder,docx_path)
                docx_text = read_docx(docx_path_source)
                st.subheader(f'Isi dokumen:{docx_path_source}')
                st.write(docx_text)

#                 # Perform TF-IDF calculation on the DOCX text
#                 tfidf_vectorizer = TfidfVectorizer()
#                 tfidf_matrix = tfidf_vectorizer.fit_transform([docx_text])
#                 feature_names = tfidf_vectorizer.get_feature_names_out()
#                 dense = tfidf_matrix.todense()
#                 docx_tfidf = pd.DataFrame(dense, columns=feature_names)

#                 tfidf_data.append((file_path, keyword, tfidf, docx_tfidf))

            # Display or save the TF-IDF data as needed
            # For example, you can display it as a table:
#             st.subheader("TF-IDF Data:")
#             for i, (file_path, keyword, tfidf, docx_tfidf) in enumerate(tfidf_data, 1):
#                 st.subheader(f"Hasil {i} TF-IDF Data:")
#                 st.write(docx_tfidf)
                
        else:
            st.warning("Tidak ditemukan hasil yang sesuai.")
            st.write(results)
    else:
        st.warning("Masukkan teks untuk pencarian.")