import re

_HASHTAG_PATTERN_STRING = "\B#\w+"
HASHTAG_PATTERN = re.compile(_HASHTAG_PATTERN_STRING)


def extract_tags_from_description(description):
    return [
        x.lower() for x in
        HASHTAG_PATTERN.findall(description)
    ]
