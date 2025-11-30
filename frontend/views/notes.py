import streamlit as st
from frontend.api_client import get_notes, create_note, delete_note, get_folders

def notes_page():
    st.title("📝 My Notes")
    
    # --- Sidebar for Folders ---
    folders = get_folders()
    if not folders:
        folders = ["General"]
        
    # Use session state to track selected folder
    if "selected_note_folder" not in st.session_state:
        st.session_state.selected_note_folder = "General"
        
    # Ensure selected folder still exists
    if st.session_state.selected_note_folder not in folders:
        st.session_state.selected_note_folder = folders[0]

    # Layout: Left column for folders (or top pills), Right for notes
    # Let's use pills for a cleaner look if few folders, or a sidebar section
    
    st.subheader("📁 Folders")
    selected_folder = st.pills("Select Folder", folders, selection_mode="single", default=st.session_state.selected_note_folder)
    
    if selected_folder:
        st.session_state.selected_note_folder = selected_folder
    
    current_folder = st.session_state.selected_note_folder
    
    st.divider()
    
    # --- Display Notes in Selected Folder ---
    st.subheader(f"📂 {current_folder}")
    
    all_notes = get_notes()
    # Filter notes by folder
    folder_notes = [n for n in all_notes if n.get("folder", "General") == current_folder]
    
    if not folder_notes:
        st.info(f"No notes in '{current_folder}'.")
    else:
        for note in folder_notes:
            with st.expander(f"📄 {note['title']}", expanded=False):
                st.markdown(note["content"])
                st.caption(f"Created: {note['created_at'][:10]}")
                
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("Delete", key=f"del_{note['id']}", type="primary"):
                        if delete_note(note["id"]):
                            st.success("Deleted!")
                            st.rerun()
    
    st.divider()
    
    # --- Create New Note (Optional here, since we have "Add to Notes" in Study) ---
    with st.expander("➕ Create New Note Manually"):
        new_title = st.text_input("Title")
        new_content = st.text_area("Content")
        if st.button("Save Manual Note"):
            if new_title and new_content:
                if create_note(new_title, new_content, current_folder):
                    st.success("Note saved!")
                    st.rerun()
                else:
                    st.error("Failed to save note")
