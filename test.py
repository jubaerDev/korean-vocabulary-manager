import sys
import os

from utils.grammar import extract_words

text = "저는 학교에서 한국어를 공부했습니다."

print(extract_words(text))