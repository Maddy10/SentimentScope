import streamlit as st
from transformers import pipeline

# Set page configuration (MUST be the first Streamlit command)
st.set_page_config(page_title="Multilingual Sentiment Analyzer", layout="centered")

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Load the sentiment model once
sentiment_analyzer = load_model()

def map_sentiment(label):
    star_rating = int(label[0])
    if star_rating <= 2:
        return "Negative"
    elif star_rating == 3:
        return "Neutral"
    else:
        return "Positive"

def analyze_sentiment(text):
    try:
        result = sentiment_analyzer(text)
        label = result[0]["label"]
        score = result[0]["score"]
        sentiment = map_sentiment(label)
        return sentiment, label, score
    except Exception as e:
        return "Error", "N/A", str(e)

def main():
    st.title("🌍 SentimentScope")
    st.write("Enter text in any language and click the button to analyze sentiment.")

    user_input = st.text_area("📝 Enter text below:")

    if st.button("🔍 Analyze"):
        if user_input.strip():
            with st.spinner("Analyzing sentiment..."):
                sentiment, raw_label, score = analyze_sentiment(user_input)

            if sentiment == "Error":
                st.error(f"Error analyzing sentiment: {score}")
            else:
                st.success(f"**Sentiment:** {sentiment}")
                st.write(f"**Model Label:** {raw_label}")
                st.write(f"**Confidence Score:** {score:.4f}")
        else:
            st.warning("Please enter some text before clicking Analyze.")

if __name__ == "__main__":
    main()
