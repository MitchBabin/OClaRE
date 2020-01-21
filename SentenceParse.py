#####################
#      Imports      #
#####################
import re


MAX_SIZE = 20 #Max sentence length


def _ParseWords(sentence: str) -> list:
    """Private function not for use outside of the library.
Converts sentences into list of words."""

    result = []
    word = ""
    
    for i in range(0, len(sentence)):

        # End of sentence? Append the word and break
        if (sentence[i] == "." or sentence[i] == "!" or sentence[i] == "?") and i == len(sentence)-1:
            result.append(word)
            break

        # Letter is an alphabetic charater? Add it to the word
        if sentence[i].isalpha() or sentence[i] == '\'' or sentence[i] == '-': 
            word += sentence[i]

        # End of the line? Append the word to list, and break
        if i == len(sentence)-1:
            if len(word) > 0:
                result.append(word)
            break
            
        # End of word?
        if sentence[i+1].isspace():
            if len(word) > 0:
                result.append(word)
                word = ""
        
            
    return result;


def _ParseBlobs(sentence: str) -> list:
    """Private function not for use outside of calls within library.
Converts a sentence into a list of its component blobs of MAX_SIZE"""

    result = []
    temp = []

    # Get a list of words in the sentence without limitation on size of blob
    words = _ParseWords(sentence)

    
    for i in range (0, len(words)):
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
        if i == len(paragraph)-1:
            if len(sentence) > 0:
                results.append(sentence)
            break

        # Is end of line? Add sentence if not empty
        if (paragraph[i] == "." or paragraph[i] == "!" or paragraph[i] == "?"):
            if len(sentence) > 0:
                results.append(sentence)
                sentence = ""
            
        
    return results



def _ParseMath(sentence: str) -> str:
    """Private function unintended for use outside library.
Converts all math symbols and formulas into [MATH] placeholders."""
    
    regex = "(\(( (\d*)|\d*)( ( |-|\+|\/|\*|x|X|e|E|\*\*|\^)|-|\+|\/|\*|x|X|e|E|\*\*|^)( (\d*)|\d*)( \)|\)))|(\d+( ( |-|\+|\/|\*|x|X|\*\*|^)|-|\+|\/|\*|x|X|e|E|\*\*|\^)( (\d*)|\d*))|(\d+.\d+)"
    newSentence = re.sub(regex,'[MATH]',sentence)
    return newSentence


def ParseParagraph(paragraph: str) -> list:
    """Converts a paragraph into a list of lists containing a blob's worth of words. The length of a blob is defined by SetMaxSize(size: int)"""
    results = _ParseSentence(paragraph)
    word_arrays = []
    
    for sentence in results:
        blobs = _ParseMath(sentence)
        for blob in blobs:
            word_arrays.append(blob)
            
    return word_arrays

def SetMaxSize(size:int) -> None:
    """Set the maximum size a sentence can be before becoming a blob"""
    MAX_SIZE = size
