def count_words(text):
    """Return a dict mapping each word to how many times it appears."""
    text = text.lower()
    for ch in [".", ",", "!", "?", ":", ";", "'", "\"", "(", ")", "-", "\n"]:
        text = text.replace(ch, " ")
    words = text.split()

    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


sample_text = (
    "Coding every day makes you better at coding. "
    "At first coding feels hard, but every small step builds your confidence. "
    "Keep coding, keep learning, and every day will get a little easier!"
)

word_counts = count_words(sample_text)
top_words = sorted(word_counts.items(), key=lambda pair: pair[1], reverse=True)[:5]

print("Top 5 most frequent words:")
for word, count in top_words:
    print(f"  {word} -> {count}")

