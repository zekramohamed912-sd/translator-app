import json
import pickle
import re
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load model
model = load_model("model/translation_model.keras")

# Load tokenizers
with open("model/en_tokenizer.pkl", "rb") as f:
    en_tokenizer = pickle.load(f)

with open("model/fr_tokenizer.pkl", "rb") as f:
    fr_tokenizer = pickle.load(f)

# Load config
with open("model/config.json", "r") as f:
    config = json.load(f)

MAX_EN_LEN = config["MAX_EN_LEN"]
MAX_FR_LEN = config["MAX_FR_LEN"]
start_id = config["start_id"]
end_id = config["end_id"]

# Build index-to-word dictionary
fr_index_word = {i: w for w, i in fr_tokenizer.word_index.items()}
fr_index_word[0] = "<pad>"

def clean_english(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z?.!,']+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def encode_sentence(sentence):
    sentence = clean_english(sentence)
    seq = en_tokenizer.texts_to_sequences([sentence])
    return pad_sequences(seq, maxlen=MAX_EN_LEN, padding="post")

def greedy_translate(sentence):
    encoder_input = encode_sentence(sentence)
    decoder_input = [start_id]

    for _ in range(MAX_FR_LEN - 1):
        decoder_pad = pad_sequences([decoder_input], maxlen=MAX_FR_LEN - 1, padding="post")
        predictions = model.predict([encoder_input, decoder_pad], verbose=0)

        next_token = int(np.argmax(predictions[0, len(decoder_input) - 1]))

        if next_token == end_id or next_token == 0:
            break

        decoder_input.append(next_token)

    words = []
    for token in decoder_input[1:]:
        word = fr_index_word.get(token, "")
        if word == "<end>":
            break
        words.append(word)

    return " ".join(words)

if __name__ == "__main__":
    test_sentence = "she likes apples ."
    result = greedy_translate(test_sentence)
    print("Input:", test_sentence)
    print("Translation:", result)