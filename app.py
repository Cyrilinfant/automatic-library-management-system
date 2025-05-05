import streamlit as st
import pandas as pd

# Initialize book data
@st.cache_data
def load_data():
    return pd.DataFrame(columns=["Title", "Author", "Genre", "Year", "Status"])

# Load or initialize session data
if 'library_data' not in st.session_state:
    st.session_state.library_data = load_data()

# Set page config
st.set_page_config(page_title="Library System", layout="centered")
st.title("📚 Automatic Library Management System")

# Tabbed Navigation
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Book", "📖 View Books", "🔍 Search", "🔁 Check In/Out"])

# Add Book Tab
with tab1:
    st.subheader("Add a New Book")
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        title = col1.text_input("Book Title")
        author = col2.text_input("Author")
        col3, col4 = st.columns(2)
        genre = col3.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Biography", "Other"])
        year = col4.number_input("Year", min_value=1800, max_value=2100, value=2023)
        submit = st.form_submit_button("📥 Add Book")

    if submit:
        if title and author:
            new_book = {"Title": title, "Author": author, "Genre": genre, "Year": year, "Status": "Available"}
            st.session_state.library_data = pd.concat(
                [st.session_state.library_data, pd.DataFrame([new_book])],
                ignore_index=True
            )
            st.success("✅ Book added!")
        else:
            st.error("❗ Please fill in both Title and Author.")

# View Books Tab
with tab2:
    st.subheader("All Books in Library")
    if st.session_state.library_data.empty:
        st.info("No books added yet.")
    else:
        for i, row in st.session_state.library_data.iterrows():
            st.markdown(f"""
            <div style="border:1px solid #ccc; border-radius:10px; padding:10px; margin-bottom:10px">
                <b>📖 Title:</b> {row['Title']}<br>
                <b>✍️ Author:</b> {row['Author']}<br>
                <b>🏷 Genre:</b> {row['Genre']} | <b>📅 Year:</b> {row['Year']}<br>
                <b>Status:</b> <span style='color:{"green" if row["Status"]=="Available" else "red"}'>{row["Status"]}</span>
            </div>
            """, unsafe_allow_html=True)

# Search Tab
with tab3:
    st.subheader("Search Library")
    search_option = st.radio("Search by", ["Title", "Author"], horizontal=True)
    query = st.text_input("Search...")
    if query:
        filtered = st.session_state.library_data[
            st.session_state.library_data[search_option].str.contains(query, case=False, na=False)
        ]
        if not filtered.empty:
            st.dataframe(filtered)
        else:
            st.warning(f"No match found for {search_option}: {query}")

# Check In / Out Tab
with tab4:
    st.subheader("Check Out or Return Book")
    with st.form("status_form"):
        book_title = st.text_input("Enter Book Title")
        action = st.radio("Action", ["Check Out", "Return"], horizontal=True)
        submit_status = st.form_submit_button("Update Status")

    if submit_status:
        index = st.session_state.library_data[
            st.session_state.library_data["Title"].str.contains(book_title, case=False, na=False)
        ].index

        if not index.empty:
            current = st.session_state.library_data.loc[index[0], "Status"]
            if action == "Check Out" and current == "Available":
                st.session_state.library_data.at[index[0], "Status"] = "Checked Out"
                st.success("✅ Book Checked Out")
            elif action == "Return" and current == "Checked Out":
                st.session_state.library_data.at[index[0], "Status"] = "Available"
                st.success("✅ Book Returned")
            else:
                st.error(f"⚠️ Cannot perform action. Current status: {current}")
        else:
            st.error("❗ Book not found.")
