import streamlit as st 
from transformers import pipeline

st.set_page_config(page_title="Sentiment Analyzer")
st.title("Sentiment Analyzer")
st.write("A Text Sentiment Analyzer")

user_input = st.text_area("Enter your text to analyze its sentiment:")

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

classifier = load_model()

if st.button("Analyze"):
    if user_input.strip():
        result =  classifier(user_input)[0]
        label= result["label"]
        confidence = round(result["score"] * 10, 2)
        match label:
            case "POSITIVE":
                st.success(f"Positive - {confidence}% confidence")
            case "NEGATIVE":
                st.error(f"Negative - {confidence}% confidence")
            case "NEUTRAL":
                st.info(f"Neutral - {confidence}% confidence")
            case _:
                st.warning(f"Unknow sentiment")
    else:
        st.warning("Input is invalid!")


        
