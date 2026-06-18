import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load variables from the .env file
load_dotenv()

# Page setup for the Streamlit web browser
st.set_page_config(page_title="Prompt-Based GenAI App", page_icon="🚀", layout="wide")

# Verify token is found safely within the web workflow
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    st.error("🛑 HF_TOKEN not found! Please check your `.env` file configurations.")
    st.stop()

# Initialize Hugging Face Serverless client
client = InferenceClient(api_key=hf_token)
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# --- Core AI Functions ---

def generate_summary(text, tone, max_sentences):
    system_instruction = (
        "You are an expert research assistant. Your task is to provide a highly accurate, "
        "objective, and concise summary of the provided text."
    )
    user_prompt = f"""
    Please summarize the text delimited by triple backticks below.
    Constraints:
    - The summary must be written in a {tone} tone.
    - It must not exceed {max_sentences} sentences.
    - Rely ONLY on the clear facts directly mentioned in the context. Do not assume or extrapolate.

    Text to summarize:
    ```
    {text}
    ```
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )
    return response.choices[0].message.content

def answer_question(context, question):
    system_instruction = (
        "You are a factual QA assistant. You answer questions based strictly on the provided context."
    )
    user_prompt = f"""
    Answer the question based strictly on the context provided below. 
    If the answer cannot be found in the context, respond exactly with: "I am sorry, but the provided text does not contain enough information to answer your question."

    Context:
    ```
    {context}
    ```
    Question: {question}
    Answer:
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_tokens=200
    )
    return response.choices[0].message.content

def evaluate_output(source_text, model_output):
    judge_prompt = f"""
    You are an AI Quality Assurance Auditor. Evaluate the following Generated Output against the Source Text.

    Source Text:
    ```
    {source_text}
    ```
    Generated Output:
    ```
    {model_output}
    ```
    Provide a score from 1-5 for each metric, followed by a 1-sentence reason:
    1. Relevance (Does it capture the main points without extra fluff?)
    2. Coherence (Is it logically structured and easy to read?)
    3. Hallucination Check (Are there any facts in the output NOT found in the source text? Answer Yes/No)
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0.1,
        max_tokens=400
    )
    return response.choices[0].message.content


# --- Web Page Interface UI Layout ---

st.title("🤖 Prompt-Based Generative AI Application")
st.markdown("Powered by Python, Streamlit, and Serverless Llama 3 API")
st.divider()

# Default dataset option
default_text = """Apollo 11 was the American spaceflight that first landed humans on the Moon. Commander Neil Armstrong and Lunar Module Pilot Buzz Aldrin landed the Apollo Lunar Module Eagle on July 20, 1969, at 20:17 UTC. Armstrong became the first person to step onto the lunar surface six hours and 39 minutes later on July 21 at 02:56 UTC. Michael Collins piloted the command module Columbia alone in lunar orbit while they were on the Moon's surface."""

# Sidebar option to select/paste source context text
st.sidebar.header("Input Context Config")
source_context = st.sidebar.text_area("Global Source Text Context", value=default_text, height=250)

# Create layout tabs
tab1, tab2, tab3 = st.tabs(["📝 Text Summarization", "❓ Factual QA & Guardrails", "🎯 LLM-As-A-Judge Metric Evaluation"])

# TAB 1: SUMMARIZATION
with tab1:
    st.header("Text Summarization Model Interface")
    col1, col2 = st.columns(2)
    
    with col1:
        tone_choice = st.selectbox("Summary Tone Styling", ["informative", "professional", "casual", "academic"])
        sentence_slider = st.slider("Maximum Sentences Constraint", min_value=1, max_value=5, value=2)
        run_sum_btn = st.button("Generate Context Summary", type="primary")
        
    with col2:
        st.subheader("Output Result")
        if run_sum_btn:
            with st.spinner("Processing generation via cloud..."):
                summary_res = generate_summary(source_context, tone_choice, sentence_slider)
                st.session_state["saved_summary"] = summary_res  # Store for evaluation tab
                st.info(summary_res)
        else:
            st.write("Click 'Generate Context Summary' to view results.")

# TAB 2: QUESTION ANSWERING & GUARDRAILS
with tab2:
    st.header("Factual Grounded Question Answering")
    st.markdown("> *Try testing questions directly matching the article or out-of-bounds questions to inspect hallucination guardrails.*")
    
    user_query = st.text_input("Enter Question:", placeholder="e.g., Who piloted the command module Columbia?")
    run_qa_btn = st.button("Query LLM Engine")
    
    if run_qa_btn and user_query:
        with st.spinner("Answering query..."):
            qa_res = answer_question(source_context, user_query)
            st.success(f"**Answer:** {qa_res}")

# TAB 3: AUTOMATED EVALUATION METRICS
with tab3:
    st.header("LLM-As-A-Judge Evaluation Suite")
    st.markdown("This section automates qualitative scoring checks across key target metrics.")
    
    current_summary = st.session_state.get("saved_summary", "")
    
    if not current_summary:
        st.warning("⚠️ Please execute a generation task within the 'Text Summarization' tab first to evaluate structural outputs.")
    else:
        st.write("**Evaluating Summary:**", current_summary)
        run_eval_btn = st.button("Execute Auditor Pipeline")
        
        if run_eval_btn:
            with st.spinner("Auditing prompt alignment metrics..."):
                eval_report = evaluate_output(source_context, current_summary)
                st.code(eval_report, language="markdown")