from transformers import pipeline

def load_model(model_choice):
    if model_choice == "BART":
        model_name = "facebook/bart-large-cnn"
    else:
        model_name = "t5-small"

    return pipeline("summarization", model=model_name)