import re

def generate_ai_summary(text):
    """
    Placeholder AI engine for StudySphere.
    Extracts the first 1-2 sentences from the provided notes text.
    Ready to be easily integrated with Google Gemini or OpenAI API.
    """
    if not text:
        return ""
    
    clean_text = text.strip()
    
    # Heuristic for splitting sentences
    # Matches a punctuation (.!?), followed by whitespace
    sentence_split_regex = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_split_regex.split(clean_text)
    
    # If the regex doesn't match easily, fallback to simple period split
    if len(sentences) == 1:
        # Fallback split
        sentences = [s.strip() for s in clean_text.split('.') if s.strip()]
        # Add period back
        sentences = [s + "." for s in sentences]
        
    if not sentences:
        return "No text to summarize."
        
    # Take the first 1 or 2 sentences
    summary_sentences = sentences[:2]
    summary_text = " ".join(summary_sentences)
    
    # Ensure it ends with punctuation if it doesn't already
    if not summary_text.endswith(('.', '!', '?')):
        summary_text += '.'
        
    return f"{summary_text}"
