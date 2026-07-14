import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.grammar import extract_words

text = "저는 학교에서 한국어를 공부했습니다."

print(extract_words(text))