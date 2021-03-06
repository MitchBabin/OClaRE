#############################
#      SentenceParser       #
# Parses paragraphs into a  #
# list of sentences,        #
# splitting on periods,     #
# double newlines and EOF.  #
# Also converts math into   #
# [MATH] tokens             #
#############################


#####################
#      Imports      #
#####################
import re
import Kandy

MAX_SIZE = 20  # Max sentence length


def _ParseWords(sentence: str) -> list:
    """Private function not for use outside of the library.
Converts sentences into list of words."""

    result = []
    word = ""

    for i in range(0, len(sentence)):

        # End of sentence? Append the word and break
        if (sentence[i] == "." or sentence[i] == "!" or sentence[i] == "?") and i == len(sentence) - 1:
            if len(word) > 0:
                result.append(word)
            break

        # Is it a math token?
        elif _isMath(sentence, i):
            if len(word) > 0:
                result.append(word)
                word = ""
            if sentence[i] == ']':
                result.append("[MATH]")


        # Letter is an alphabetic charater? Add it to the word
        elif sentence[i].isalpha() or sentence[i] == '\'' or sentence[i] == '-':
            word += sentence[i]

        # End of the line? Append the word to list, and break
        if i == len(sentence) - 1:
            if len(word) > 0:
                result.append(word)
            break

        # End of word?
        elif sentence[i + 1].isspace():
            if len(word) > 0:
                result.append(word)
                word = ""

    return result;


def _isMath(sentence: str, index: int) -> bool:
    """Private function, not intended for use outside of library.
Checks if passed index is part of [MATH] token."""

    token = "[MATH]"
    length = len(sentence)

    if (index + 5 < length and
            (sentence[index] +
             sentence[index + 1] +
             sentence[index + 2] +
             sentence[index + 3] +
             sentence[index + 4] +
             sentence[index + 5] == token)):
        return True

    if (index - 1 >= 0 and index + 4 < length and
            (sentence[index - 1] +
             sentence[index] +
             sentence[index + 1] +
             sentence[index + 2] +
             sentence[index + 3] +
             sentence[index + 4] == token)):
        return True

    if (index - 2 >= 0 and index + 3 < length and
            (sentence[index - 2] +
             sentence[index - 1] +
             sentence[index] +
             sentence[index + 1] +
             sentence[index + 2] +
             sentence[index + 3] == token)):
        return True

    if (index - 3 >= 0 and index + 2 < length and
            (sentence[index - 3] +
             sentence[index - 2] +
             sentence[index - 1] +
             sentence[index] +
             sentence[index + 1] +
             sentence[index + 2] == token)):
        return True

    if (index - 4 >= 0 and index + 1 < length and
            (sentence[index - 4] +
             sentence[index - 3] +
             sentence[index - 2] +
             sentence[index - 1] +
             sentence[index] +
             sentence[index + 1] == token)):
        return True

    if (index - 5 >= 0 and
            (sentence[index - 5] +
             sentence[index - 4] +
             sentence[index - 3] +
             sentence[index - 2] +
             sentence[index - 1] +
             sentence[index] == token)):
        return True

    return False


def _ParseBlobs(sentence: str) -> list:
    """Private function not for use outside of calls within library.
Converts a sentence into a list of its component blobs of MAX_SIZE"""

    result = []
    temp = []

    # Get a list of words in the sentence without limitation on size of blob
    words = _ParseWords(sentence)

    for i in range(0, len(words)):
        # Append word to temp blob
        temp.append(words[i])

        # If temp blob has reached max size, add to list and reset temp
        if len(temp) >= MAX_SIZE:
            result.append(temp.copy())
            temp = []

    # If we got through the loop before reaching the MAX_SIZE blob
    # Add the blob to the list
    if len(temp) <= MAX_SIZE:
        result.append(temp.copy())

    return result


def _ParseSentence(paragraph: str) -> list:
    """Private function not for use outside of calls within library.
converts a paragraph into component sentences based on punctuation."""

    results = []
    sentence = ""

    for i in range(0, len(paragraph)):
        sentence += paragraph[i]

        # Is end of paragraph? Add sentence if not empty and end
        if i == len(paragraph) - 1:
            if len(sentence) > 0:
                sentence = sentence.strip()
                sentence = re.sub('(\\n)', '', sentence)
                results.append(sentence)
            break

        if _isEllipsis(paragraph, i):
            continue

        # Is end of line? Add sentence if not empty
        if paragraph[i] == "." or paragraph[i] == "!" or paragraph[i] == "?":
            if len(sentence) > 0:
                sentence = sentence.strip()
                sentence = re.sub('(\\n)', '', sentence)
                results.append(sentence)
                sentence = ""

    return results


def ParseParagraph(paragraph: str) -> list:
    """Converts a paragraph into a list of lists containing a blob's worth of words. The length of a blob is defined
    by SetMaxSize(size: int) """

    results = Kandy.LaunchKandy(paragraph)
    results = _ParseSentence(results)
    sentences = []

    for sentence in results:
        blobs = sentence
        sentence = []
        for blob in _ParseWords(blobs):
            if len(blob) > 0:
                sentence.append(blob)
        sentences.append(sentence)

    for i in range(0, len(sentences)):
        sentence = []
        wasMath = False
        for word in sentences[i]:
            if not wasMath and word == "[MATH]":
                sentence.append(word)
                wasMath = True
            elif not word == "[MATH]":
                sentence.append(word)
                wasMath = False
        sentences[i] = sentence

    return sentences


def SetMaxSize(size: int) -> None:
    """Set the maximum size a sentence can be before becoming a blob"""

    MAX_SIZE = size


def _isEllipsis(paragraph: str, index: int) -> bool:
    """Private function not intended for use outside the library.
Checks if the specified index is part of an ellipsis in the provided text."""

    if index - 2 >= 0 and paragraph[index - 2] + paragraph[index - 1] + paragraph[index] == "...":
        return True

    if index - 1 >= 0 and index + 1 < len(paragraph) and \
            (paragraph[index - 1] + paragraph[index] + paragraph[index + 1] == "..."):
        return True

    if index + 2 < len(paragraph) and paragraph[index] + paragraph[index + 1] + paragraph[index + 2] == "...":
        return True

    return False
