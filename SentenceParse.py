MAX_SIZE = 200 #Max sentence length

def _Parse(sentence: str):
    result = []
    word = ""
    
    for i in range(0, len(sentence)):
        # End of sentence?
        if (sentence[i] == "." or sentence[i] == "!" or sentence[i] == "?") and i == len(sentence)-1:
            result.append(word)
            break
        
        if i == len(sentence)-1:
            if len(word) > 0:
                result.append(word)
            break
        
        if (sentence[i] == "." or sentence[i] == "!" or sentence[i] == "?") and sentence[i+1].isspace():
            result.append(word)
            break        
        
        # Letter is not whitespace?
        if not sentence[i].isspace(): 
            word += sentence[i]
            
        # End of word?
        if sentence[i+1].isspace():
            if len(word) > 0:
                result.append(word)
                word = ""
        
            
    return result;

def _ParseWords(sentence: str):
    result = []
    temp = []
    
    words = _Parse(sentence)
    
    for i in range (0, len(words)):
        temp.append(words[i])
        if len(temp) >= MAX_SIZE:
            result.append(temp.copy())
            temp = []
        
    if len(temp) <= MAX_SIZE:
        result.append(temp.copy())
        
    return result

def _ParseSentence(paragraph: str):
    results = []
    sentence = ""
    
    for i in range(0, len(paragraph)):
        sentence += paragraph[i]
        
        if i == len(paragraph)-1:
            if len(sentence) > 0:
                results.append(sentence)
            break
        
        if i+1 == len(paragraph)-1 and (paragraph[i] == "." or paragraph[i] == "!" or paragraph[i] == "?"):
            if len(sentence) > 0:
                results.append(sentence)
            break
        
        if (paragraph[i] == "." or paragraph[i] == "!" or paragraph[i] == "?") and paragraph[i+1].isspace():
            if len(sentence) > 0:
                results.append(sentence)
                sentence = ""
            
        
    return results
            
def ParseParagraph(paragraph: str):    
    results = _ParseSentence(paragraph)
    word_arrays = []
    
    for sentence in results:
        for blob in _ParseWords(sentence):
            word_arrays.append(blob)
            
    return word_arrays

#print(ParseParagraph(input()))

print(len(ParseParagraph("""You’ve probably heard of Lorem Ipsum before – it’s the most-used dummy text excerpt out there. People use it because it has a fairly normal distribution of letters and words (making it look like normal English), but it’s also Latin, which means your average reader won’t get distracted by trying to read it. It’s perfect for showcasing design work as it should look when fleshed out with text, because it allows viewers to focus on the design work itself, instead of the text. It’s also a great way to showcase the functionality of programs like word processors, font types, and more.

We’ve taken Lorem Ipsum to the next level with our HTML-Ipsum tool. As you can see, this Lorem Ipsum is tailor-made for websites and other online projects that are based in HTML. Most web design projects use Lorem Ipsum excerpts to begin with, but you always have to spend an annoying extra minute or two formatting it properly for the web.

Maybe you have a custom-styled ordered list you want to show off, or maybe you just want a long chunk of Lorem Ipsum that’s already wrapped in paragraph tags. No matter the need, we’ve put together a number of Lorem Ipsum samples ready to go with HTML tags and formatting in place. All you have to do is click the heading of any section on this page, and that HTML-Ipsum block is copied to your clipboard and ready to be loaded into a website redesign template, brand new design mockup, or any other digital project you might need dummy text for.

No matter the project, please remember to replace your fancy HTML-Ipsum with real content before you go live - this is especially important if you're planning to implement a content-based marketing strategy for your new creation! Lorem Ipsum text is all well and good to demonstrate a design or project, but if you set a website loose on the Internet without replacing dummy text with relevant, high quality content, you’ll run into all sorts of potential Search Engine Optimization issues like thin content, duplicate content, and more.

HTML-Ipsum is maintained by WebFX. For more information about us, please visit WebFX Reviews. To learn more about the industries we drive Internet marketing performormance for and our revenue driving services: SEO, PPC, social media, web design, local SEO and online advertising services.""")))