import streamlit as st
import pickle
import pandas as pd
from transformers import RobertaTokenizer, RobertaModel
import torch
import plotly.graph_objects as go

# Load the pre-trained CodeBERT model and tokenizer
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
codebert_model = RobertaModel.from_pretrained('microsoft/codebert-base')

# Load the trained model weights
with open('trained_model.pkl', 'rb') as f:
    model_weights = pickle.load(f)

# Define the model architecture to match the one used in Colab
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(768,)),  # Input layer based on CodeBERT output size
    tf.keras.layers.Dense(128, activation='elu'),  # Hidden layer
    tf.keras.layers.Dropout(0.5),  # Dropout layer
    tf.keras.layers.Dense(256, activation='elu'),  # Hidden layer
    tf.keras.layers.Dropout(0.5),  # Dropout layer
    tf.keras.layers.Dense(512, activation='elu'),  # Hidden layer
    tf.keras.layers.Dropout(0.5),  # Dropout layer
    tf.keras.layers.Dense(256, activation='elu'),  # Hidden layer
    tf.keras.layers.Dropout(0.5),  # Dropout layer
    tf.keras.layers.Dense(128, activation='elu'),  # Hidden layer
    tf.keras.layers.Dropout(0.5),  # Dropout layer
    tf.keras.layers.Dense(1, activation='sigmoid')  # Output layer
])

# Load the model weights
model.set_weights(model_weights)

# Function to embed the code using CodeBERT
def embed_code(code_snippet):
    inputs = tokenizer(code_snippet, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = codebert_model(**inputs)  # Use CodeBERT model here
    return outputs.last_hidden_state.mean(dim=1).numpy().flatten()  # Perform mean pooling

# Function to check if the uploaded file contains valid Java code
def is_valid_java_code(code):
    java_keywords = ['class', 'public', 'static', 'void', 'int', 'String']
    return any(keyword in code for keyword in java_keywords)


def create_circular_chart(percentage, label, color):
    fig = go.Figure(go.Pie(
        values=[percentage, 100 - percentage],
        labels=[label, ''],
        hole=0.6,
        sort=False,
        direction='clockwise',
        marker=dict(colors=[color, '#E5E5E5']),
        textinfo='none'
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=200,  # Size of the circular chart
        annotations=[dict(text=f'{label}', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    return fig


st.title("AI vs Human Code Classification")


uploaded_file = st.file_uploader("Upload a Java file", type="java")

if uploaded_file is not None:

    code = uploaded_file.read().decode('utf-8')


    if not is_valid_java_code(code):
        st.markdown(
            """
            <div style="
                padding: 15px;
                background-color: #f44336;
                border-radius: 5px;
                border: 1px solid #ff5555;
                color: white;
                font-size: 18px;
                text-align: center;">
                <strong>Warning:</strong> The uploaded file does not contain valid Java code. 
                Please upload a valid Java file.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:

        st.subheader("Uploaded Java Code:")
        st.code(code, language='java')


        code_embedding = embed_code(code)


        code_embedding = code_embedding.reshape(1, -1)

        # Use the model to predict the probability of AI-generated code
        prediction = model.predict(code_embedding)

        # Convert the prediction to percentage
        ai_percentage = prediction[0][0] * 100
        human_percentage = 100 - ai_percentage

        # Classification Confidence
        if human_percentage > ai_percentage:
            label = "human"
            color = '#6DD400'  # Green for human-written
            confidence_text = "We are highly confident this code is written by a human"
            confidence_color = 'green'
        else:
            label = "AI"
            color = '#FF6347'  # Red for AI-generated
            confidence_text = "We are highly confident this code is generated by AI"
            confidence_color = 'orange'

        st.markdown(f"<h4 style='text-align:center; color:{confidence_color};'>{confidence_text}</h4>", unsafe_allow_html=True)


        fig = create_circular_chart(human_percentage if human_percentage > ai_percentage else ai_percentage, label, color)

        # Display the circular chart
        st.plotly_chart(fig, use_container_width=True)

        # Show probability breakdown
        st.subheader("Probability Breakdown")
        st.write(f"**{human_percentage:.2f}%** Probability Human-generated | **{ai_percentage:.2f}%** Probability AI-generated")

        # Progress bar to show AI vs Human confidence
        st.progress(human_percentage / 100 if human_percentage > ai_percentage else ai_percentage / 100)