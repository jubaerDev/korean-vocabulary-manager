import re
from collections import Counter
import pandas as pd

def extract_korean_words(text):

    words = re.findall(r"[가-힣]+", text)

    counter = Counter(words)

    unique_words = sorted(counter.keys())

    data = []

    for word in unique_words:
        data.append({
            "Word": word,
            "Frequency": counter[word]
        })

    df = pd.DataFrame(data)

    return words, df