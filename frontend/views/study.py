import streamlit as st
from frontend.api_client import chat_with_ai, summarize_text, save_quiz_score, extract_text_from_pdf, create_note, get_folders
import random
import time

@st.dialog("📝 Add to Notes")
def add_to_notes_dialog(initial_text):
    folders = get_folders()
    
    # Initialize session state for this dialog if not present
    if "note_folder_selection" not in st.session_state:
        st.session_state.note_folder_selection = None
    
    st.write("### Save to Folder")
    
    # Folder Selection Logic
    selected_folder = st.selectbox(
        "Select Existing Folder", 
        ["Select a folder..."] + folders, 
        index=0
    )
    
    new_folder_name = st.text_input(
        "Or Create New Folder", 
        placeholder="Type new folder name...",
        disabled=(selected_folder != "Select a folder...")
    )
    
    # Determine final folder
    final_folder = "General"
    if selected_folder != "Select a folder...":
        final_folder = selected_folder
    elif new_folder_name.strip():
        final_folder = new_folder_name.strip()
            
    st.divider()
    
    note_title = st.text_input("Heading", value="Note from Study Session")
    note_content = st.text_area("Note Content", value=initial_text, height=300)
    
    if st.button("Save Note"):
        if not note_title.strip():
            st.error("Please enter a heading.")
        elif final_folder == "General" and selected_folder == "Select a folder..." and not new_folder_name.strip():
             # Allow saving to General if nothing selected, but maybe warn? 
             # Actually requirement says "New folder + note creation when user inputs folder name"
             # and "Adding notes to existing folder when one is selected"
             # If neither, default to General is safe fallback or we can force selection.
             # Let's default to General for safety but explicit is better.
             pass

        if create_note(note_title, note_content, final_folder):
            st.success(f"Note saved to '{final_folder}' successfully!")
            time.sleep(1) # Give user time to see success message
            st.rerun()
        else:
            st.error("Failed to save note.")

def study_page():
    st.title("🧠 Study Room")
    
    # Use Tabs instead of Sidebar Radio
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📄 Summarizer", "🧩 Quiz"])
    
    # --- Chat Tab ---
    with tab1:
        st.header("AI Tutor")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                # Add "Add to Notes" button for assistant messages
                if msg["role"] == "assistant":
                    if st.button("📝 Add to Notes", key=f"note_btn_{i}"):
                        add_to_notes_dialog(msg["content"])

        if prompt := st.chat_input("Ask me anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.spinner("Thinking..."):
                response = chat_with_ai(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

    # --- Summarizer Tab ---
    with tab2:
        st.header("Document Summarizer")
        
        # Option to choose input method
        input_method = st.radio("Choose Input Method", ["Paste Text", "Upload PDF"], horizontal=True)
        
        text_to_summarize = ""
        
        if input_method == "Paste Text":
            text_to_summarize = st.text_area("Paste text here", height=200)
        else:
            uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
            if uploaded_file is not None:
                with st.spinner("Extracting text from PDF..."):
                    text_to_summarize = extract_text_from_pdf(uploaded_file.read())
                    if text_to_summarize.startswith("Error"):
                        st.error(text_to_summarize)
                        text_to_summarize = ""
                    else:
                        st.success("PDF loaded successfully!")
                        with st.expander("View Extracted Text"):
                            st.write(text_to_summarize[:1000] + "..." if len(text_to_summarize) > 1000 else text_to_summarize)

        if st.button("Summarize"):
            if text_to_summarize:
                with st.spinner("Summarizing..."):
                    summary = summarize_text(text_to_summarize)
                    st.session_state.last_summary = summary # Store for persistence
                    st.subheader("Summary")
                    st.write(summary)
                    if st.button("📝 Add Summary to Notes"):
                        add_to_notes_dialog(summary)
            else:
                st.warning("Please provide some text or upload a valid PDF.")
        
        # Show last summary if available (to keep it after interactions)
        elif "last_summary" in st.session_state:
             st.subheader("Summary")
             st.write(st.session_state.last_summary)
             if st.button("📝 Add Summary to Notes", key="summary_note_btn"):
                 add_to_notes_dialog(st.session_state.last_summary)

    # --- Quiz Tab ---
    with tab3:
        st.header("Quiz Arena")
        
        if "quiz_data" not in st.session_state:
            st.session_state.quiz_data = None
        if "user_answers" not in st.session_state:
            st.session_state.user_answers = {}
        if "quiz_start_time" not in st.session_state:
            st.session_state.quiz_start_time = None

        # 1. Quiz Setup (Only if not active)
        if not st.session_state.get("quiz_active"):
            from frontend.api_client import check_has_topics, generate_quiz
            
            has_topics = check_has_topics()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Start New Quiz")
                quiz_mode = st.radio("Quiz Mode", ["Random (From History)", "Specific Topic"])
                
                topic_input = ""
                if quiz_mode == "Specific Topic":
                    topic_input = st.text_input("Enter Topic")
                
                # Disable Random if no topics
                start_disabled = False
                if quiz_mode == "Random (From History)" and not has_topics:
                    st.warning("⚠️ No chat/summary history found. Please use the Chat or Summarizer first to enable Random Quiz.")
                    start_disabled = True
                
                if st.button("Start Quiz", disabled=start_disabled):
                    with st.spinner("Generating Quiz..."):
                        if quiz_mode == "Random (From History)":
                            data = generate_quiz(from_history=True)
                        else:
                            if topic_input:
                                data = generate_quiz(topic=topic_input)
                            else:
                                st.warning("Please enter a topic.")
                                data = None
                        
                        if data:
                            st.session_state.quiz_data = data
                            st.session_state.quiz_active = True
                            st.session_state.current_question = 0
                            st.session_state.user_answers = {}
                            import time
                            st.session_state.quiz_start_time = time.time()
                            st.rerun()
                        elif not start_disabled and topic_input:
                             st.error("Failed to generate quiz. Please try again.")

            with col2:
                st.info("Test your knowledge! Random quizzes are based on your recent studies.")

        # 2. Active Quiz Interface
        elif st.session_state.get("quiz_active") and st.session_state.quiz_data:
            q_data = st.session_state.quiz_data
            questions = q_data.get("questions", [])
            total_q = len(questions)
            current_idx = st.session_state.current_question
            
            # Timer
            import time
            elapsed = int(time.time() - st.session_state.quiz_start_time)
            st.metric("⏱️ Time Elapsed", f"{elapsed}s")
            
            # Progress
            st.progress((current_idx + 1) / total_q, text=f"Question {current_idx + 1} of {total_q}")
            
            # Question Display
            if current_idx < total_q:
                q = questions[current_idx]
                st.subheader(f"Q: {q['question']}")
                
                # Options
                options = q['options']
                # Restore previous answer if any
                default_idx = None
                if current_idx in st.session_state.user_answers:
                    prev_ans = st.session_state.user_answers[current_idx]
                    if prev_ans in options:
                        default_idx = options.index(prev_ans)

                selected_option = st.radio("Choose an answer:", options, index=default_idx, key=f"q_{current_idx}")
                
                # Navigation
                c1, c2 = st.columns([1, 1])
                with c1:
                    if st.button("Next Question" if current_idx < total_q - 1 else "Finish Quiz"):
                        st.session_state.user_answers[current_idx] = selected_option
                        if current_idx < total_q - 1:
                            st.session_state.current_question += 1
                            st.rerun()
                        else:
                            # End Quiz
                            st.session_state.quiz_finished = True
                            st.session_state.quiz_active = False
                            st.rerun()
                with c2:
                     if st.button("End Quiz Now"):
                        st.session_state.user_answers[current_idx] = selected_option
                        st.session_state.quiz_finished = True
                        st.session_state.quiz_active = False
                        st.rerun()

        # 3. Quiz Results
        if st.session_state.get("quiz_finished"):
            st.header("🎉 Quiz Results")
            
            q_data = st.session_state.quiz_data
            questions = q_data.get("questions", [])
            user_answers = st.session_state.user_answers
            
            score = 0
            results = []
            
            for i, q in enumerate(questions):
                user_ans = user_answers.get(i, "No Answer")
                correct_ans = q['answer']
                is_correct = user_ans == correct_ans
                if is_correct:
                    score += 1
                
                results.append({
                    "Question": q['question'],
                    "Your Answer": user_ans,
                    "Correct Answer": correct_ans,
                    "Result": "✅" if is_correct else "❌"
                })
            
            # Save Score
            if not st.session_state.get("score_saved"):
                save_quiz_score(q_data['topic'], score, len(questions))
                st.session_state.score_saved = True
            
            st.subheader(f"Final Score: {score} / {len(questions)}")
            
            # Display Detailed Results
            st.table(results)
            
            if st.button("Start New Quiz"):
                st.session_state.quiz_active = False
                st.session_state.quiz_finished = False
                st.session_state.score_saved = False
                st.session_state.quiz_data = None
                st.rerun()
