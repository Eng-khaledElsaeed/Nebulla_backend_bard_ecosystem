

import spacy

def generate_title(text):
  """
  This function generates a concise title (2-3 words) from a text snippet.

  Args:
      text: The text snippet to analyze (str).

  Returns:
      A title string with 2-3 words (str).
  """

  # Preprocess the text (optional)
  text = text.lower()  # Convert to lowercase
  text = text.strip()  # Remove leading/trailing whitespaces

  # Extract keywords
  words = text.split()  # Split into individual words
  keywords = [word for word in words if word not in ["i", "to", "a", "an", "the"]]  # Remove common words

  # Combine keywords or use a fallback
  if len(keywords) >= 2:
    title = " ".join(keywords[:2])[:15]  # Join first two words, limit to 15 chars
  else:
    title = keywords[0] if keywords else "Untitled"  # Use single keyword or fallback

  return title