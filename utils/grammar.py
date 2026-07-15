import re

# ==========================================================
# Korean Particles (조사)
# ==========================================================

PARTICLES = [

    "에서는",
    "에게서는",
    "으로부터",
    "에게까지",
    "에게서",
    "으로는",
    "으로도",
    "으로",
    "까지",
    "부터",
    "처럼",
    "보다",
    "하고",
    "이며",
    "이나",
    "이나요",
    "에서",
    "에게",

    "은",
    "는",
    "이",
    "가",
    "을",
    "를",
    "에",
    "와",
    "과",
    "도",
    "만",
    "의",
    "로"
]

# ==========================================================
# Verb / Adjective Endings
# Longest first
# ==========================================================

VERB_ENDINGS = [

    "었습니다",
    "았습니다",
    "였습니다",

    "겠습니까",
    "겠습니다",
    "겠어요",

    "습니다",
    "ㅂ니다",

    "합니다",
    "했습니다",
    "하였다",

    "했다",
    "한다",

    "해요",

    "으세요",
    "세요",

    "으려고",
    "려고",

    "으면서",
    "면서",

    "으니까",
    "니까",

    "지만",

    "으면",
    "면",

    "으며",
    "며",

    "아서",
    "어서",
    "여서",

    "아서도",
    "어서도",

    "아요",
    "어요",

    "고",

    "는",
    "은",
    "ㄴ",

    "던",
    "았던",
    "었던"
]

# ==========================================================
# 하다 Verb Rules
# ==========================================================

HADA_RULES = {

    "했습니다": "하다",
    "합니다": "하다",
    "하였다": "하다",
    "했다": "하다",
    "한다": "하다",
    "해요": "하다"

}

# ==========================================================
# 이다 Rules
# ==========================================================

IDA_RULES = {

    "입니다": "이다"

}

# ==========================================================
# Text Cleaning
# ==========================================================

def clean_text(text):

    text = re.sub(
        r"[^\uAC00-\uD7A3\s]",
        " ",
        text
    )

    words = text.split()

    return words


# ==========================================================
# Remove Particle
# ==========================================================

def remove_particle(word):

    for particle in sorted(
        PARTICLES,
        key=len,
        reverse=True
    ):

        if word.endswith(particle):

            return word[:-len(particle)]

    return word
    # ==========================================================
# Normalize Verb / Adjective
# ==========================================================

def normalize_verb(word):

    # -----------------------------
    # 하다 verbs
    # -----------------------------

    for ending, lemma in HADA_RULES.items():

        if word.endswith(ending):

            stem = word[:-len(ending)]

            return stem + lemma

    # -----------------------------
    # 이다
    # -----------------------------

    for ending, lemma in IDA_RULES.items():

        if word.endswith(ending):

            stem = word[:-len(ending)]

            return stem + lemma

    # -----------------------------
    # General Endings
    # -----------------------------

    for ending in sorted(
        VERB_ENDINGS,
        key=len,
        reverse=True
    ):

        if word.endswith(ending):

            stem = word[:-len(ending)]

            if len(stem) == 0:

                return word

            return stem + "다"

    return word


# ==========================================================
# Root Extractor
# ==========================================================

def extract_root(word):

    original = word.strip()

    if original == "":

        return ""

    # Remove particle first
    root = remove_particle(original)

    # Normalize verb / adjective
    root = normalize_verb(root)

    return root


# ==========================================================
# Guess Word Type
# ==========================================================

def guess_pos(original, root):

    if root.endswith("하다"):
        return "Verb"

    if root.endswith("이다"):
        return "Verb"

    if root.endswith("다"):
        return "Verb/Adjective"

    return "Noun"
# ==========================================================
# Extract Words
# ==========================================================

def extract_words(text):

    words = clean_text(text)

    result = []

    seen = set()

    for original in words:

        if original.strip() == "":
            continue

        root = extract_root(original)

        pos = guess_pos(original, root)

        # Avoid duplicate root words
        if root in seen:
            continue

        seen.add(root)

        result.append(
            {
                "original": original,
                "root": root,
                "pos": pos
            }
        )

    return result


# ==========================================================
# Debug Mode
# ==========================================================

if __name__ == "__main__":

    sample = """
    저는 학교에서 한국어를 공부했습니다.
    친구를 만나고 밥을 먹었습니다.
    보면 재미있어요.
    작은 집이 있습니다.
    """

    words = extract_words(sample)

    for item in words:

        print(
            f"{item['original']}  -->  {item['root']} ({item['pos']})"
        )