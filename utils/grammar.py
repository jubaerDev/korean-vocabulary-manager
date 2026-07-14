import re

# Korean particles (조사)
PARTICLES = [
    "에서는",
    "에게서",
    "으로는",
    "으로",
    "에서",
    "에게",
    "까지",
    "부터",
    "처럼",
    "보다",
    "하고",
    "이며",
    "이나",
    "이나요",
    "으로도",
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

# Common verb endings
VERB_ENDINGS = [
    "었습니다",
    "았습니다",
    "였습니다",
    "ㅂ니다",
    "습니다",
    "입니다",
    "합니다",
    "합니다.",
    "했다",
    "했다.",
    "한다",
    "한다.",
    "했다가",
    "해요",
    "아요",
    "어요",
    "네요",
    "군요",
    "겠다",
    "겠어요",
    "겠습니 다",
    "고",
    "며",
    "면",
    "니까",
    "세요"
]


def clean_text(text):
    """
    Remove punctuation and split words.
    """

    text = re.sub(r"[^\uAC00-\uD7A3\s]", " ", text)

    words = text.split()

    return words


def remove_particle(word):

    for particle in sorted(PARTICLES, key=len, reverse=True):

        if word.endswith(particle):

            return word[:-len(particle)]

    return word


def normalize_verb(word):

    # 공부했습니다 -> 공부하다
    if word.endswith("했습니다"):
        return word[:-4] + "하다"

    if word.endswith("합니다"):
        return word[:-3] + "하다"

    if word.endswith("했다"):
        return word[:-2] + "하다"

    if word.endswith("해요"):
        return word[:-2] + "하다"

    if word.endswith("입니다"):
        return word[:-3]

    for ending in sorted(VERB_ENDINGS, key=len, reverse=True):

        if word.endswith(ending):

            word = word[:-len(ending)]

            break

    return word


def extract_root(word):

    word = word.strip()

    word = remove_particle(word)

    word = normalize_verb(word)

    return word


def extract_words(text):

    words = clean_text(text)

    result = []

    seen = set()

    for word in words:

        root = extract_root(word)

        if root and root not in seen:

            result.append({
                "original": word,
                "root": root
            })

            seen.add(root)

    return result