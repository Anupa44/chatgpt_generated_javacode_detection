# ChatGPT-Generated Java Code Detection

This project aims to classify Java code as AI-generated(ChatGpt) or human-written. It uses two models — a deep learning-based model and a traditional machine learning model. A custom dataset created by me from Java code on LeetCode and AtCoder has been used for training.

The tool includes a simple UI where users can upload a Java file and receive a percentage breakdown of AI-written vs. human-written code.

## Features
- **Two Classification Models**: Deep learning and machine learning models for code classification.
- **Custom Java Dataset**: Created using LeetCode and AtCoder, specifically for Java-based code.
- **UI for Code Classification**: Upload Java files and get a detailed percentage of AI vs. human-written code.

## Prerequisites
- Python 3.8 or higher
- Jupyter Notebook
- Required packages (see `requirements.txt`)

To install the required packages, run:
```bash
pip install -r requirements.txt
