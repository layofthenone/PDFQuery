import streamlit as st
import os
import webbrowser
import tempfile
from utils import init_db, search_in_pdfs, display_pdf_page

# Render the Streamlit UI
def render_ui():
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
    }
    .result-card {
        background-color: white;
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-size: 14px;
    }
    .result-card p, .result-card h4 {
        color: #000000;
        margin: 2px 0;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("📑 PDF Search and Viewer")
    st.markdown("<p style='text-align: center; color: #7f8c8d;'>Search through your PDF files quickly and view pages!</p>", unsafe_allow_html=True)

    # State management
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'folder_path' not in st.session_state:
        st.session_state.folder_path = "C:/pdf_folder"
    if 'query' not in st.session_state:
        st.session_state.query = ""

    # Input fields (side by side)
    col1, col2 = st.columns([2, 1])
    with col1:
        folder_path = st.text_input("📂 PDF Folder Path", value=st.session_state.folder_path, placeholder="E.g., C:/Users/YourName/pdfs")
    with col2:
        query = st.text_input("🔍 Search Term", value=st.session_state.query, placeholder="Enter search term")

    # Search button
    if st.button("Search", use_container_width=True):
        if not os.path.exists(folder_path):
            st.error("Invalid folder path!")
        elif not query:
            st.error("Please enter a search term!")
        else:
            with st.spinner("Scanning PDFs..."):
                import time
                start_time = time.time()
                init_db()
                st.session_state.results = search_in_pdfs(folder_path, query)
                st.session_state.folder_path = folder_path
                st.session_state.query = query
                end_time = time.time()
                st.success(f"Search completed: {len(st.session_state.results)} results found ({end_time - start_time:.2f} seconds)")

    # Function to open PDF in browser at specific page
    def open_pdf_in_browser(pdf_path, page_num):
        html_content = f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url=file:///{pdf_path.replace('\\', '/')}#page={page_num}">
        </head>
        <body>
            <p>Opening PDF... If it doesn't open, <a href="file:///{pdf_path.replace('\\', '/')}#page={page_num}">click here</a>.</p>
        </body>
        </html>
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            tmp_file.write(html_content.encode('utf-8'))
            tmp_file_path = tmp_file.name
        webbrowser.open_new_tab(f"file:///{tmp_file_path}")

    # Display results
    if st.session_state.results is not None:
        if st.session_state.results:
            st.markdown("### 🔎 Results")
            for i, result in enumerate(st.session_state.results):
                with st.container():
                    st.markdown(f"""
                    <div class="result-card">
                        <h4>Result {i+1}</h4>
                        <p><strong>File:</strong> {result['pdf_path']}</p>
                        <p><strong>Page:</strong> {result['page_num']}</p>
                        <p><strong>Snippet:</strong> {result['snippet']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    # Buttons side by side with equal width
                    col_view, col_open = st.columns(2)
                    with col_view:
                        if st.button("📄 View PDF", key=f"view_{i}"):
                            with st.spinner("Loading PDF page..."):
                                image = display_pdf_page(result['pdf_path'], result['page_num'])
                                if image:
                                    st.image(image, caption=f"{os.path.basename(result['pdf_path'])} - Page {result['page_num']}", use_container_width=True)
                    with col_open:
                        if st.button("📖 Open PDF", key=f"open_{i}"):
                            pdf_path = result['pdf_path']
                            page_num = result['page_num']
                            open_pdf_in_browser(pdf_path, page_num)
                            st.success(f"{os.path.basename(pdf_path)} opening in browser - Page {page_num}")
        else:
            st.warning("No results found.")