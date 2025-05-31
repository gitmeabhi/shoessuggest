import streamlit as st
from prompts.shoe_prompt import shoe_prompt
from utils.llm import get_llm

# Page config
st.set_page_config(page_title="Shoe Suggestion AI", page_icon="👟", layout="wide")

# Sidebar menu for occasion selection
st.sidebar.title("👟 AI-Powered Occasion-Based Shoe Recommender")
occasions = ["Select Occasion", "Wedding", "Gym Workout", "Casual Walk", "Business Meeting", 
             "Party", "Beach Day", "Hiking", "Date Night", "Interview"]
selected_occasion = st.sidebar.selectbox("Choose an occasion:", occasions)

# Inject CSS for hoverable cards
st.markdown("""
    <style>
    .hover-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 10px;
        transition: box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    .hover-box:hover {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        background-color: #f0f8ff;
    }
    </style>
""", unsafe_allow_html=True)

# Display layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### 👞 Occasion")
    if selected_occasion != "Select Occasion":
        st.write(selected_occasion)
    else:
        st.write("Please choose an occasion from the list.")

with col2:
    st.markdown("### 👟 Suggested Shoe Details")
    
    if selected_occasion != "Select Occasion":
        with st.spinner("Getting your perfect shoe suggestions..."):
            llm = get_llm()
            prompt = shoe_prompt.format(occasion=selected_occasion)
            response = llm.invoke(prompt)
            
            def parse_response(text):
                sections = {}
                current_key = None
                for line in text.split('\n'):
                    line = line.strip()
                    if line.endswith(':'):
                        current_key = line[:-1]
                        sections[current_key] = []
                    elif current_key:
                        sections[current_key].append(line)
                for k in sections:
                    sections[k] = "\n".join(sections[k]).strip()
                return sections
            
            parsed = parse_response(response.content)

            if parsed:
                for key, val in parsed.items():
                    st.markdown(f"""
                        <div class="hover-box">
                            <strong>{key}</strong>
                            <p style="margin-top: 0.5rem;">{val.replace('\n', '<br>')}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.write(response.content)
    else:
        st.markdown("👈 Select your occasion to get started with tailored shoe recommendations!")
