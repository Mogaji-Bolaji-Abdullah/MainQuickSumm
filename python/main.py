import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """"In a peaceful forest, there lived a wise old tortoise named Timmy. Timmy was known for his slow, deliberate movements and his thoughtful approach to life. He often watched the other animals rush around, always in a hurry, and he wondered what it would be like to move so quickly.

One day, the forest animals decided to have a race to see who was the fastest. All the animals gathered at the starting line, buzzing with excitement. There were rabbits, deer, foxes, and even a squirrel, all eager to show off their speed. Timmy the tortoise watched from a distance, his curiosity piqued.

"Why don't you join us, Timmy?" a rabbit named Ruby asked, hopping over to him. "It'll be fun!"

Timmy chuckled. "I'm not fast like you, Ruby. I'd only slow everyone down."

"Nonsense!" Ruby replied. "The race is about more than just speed. It's about having fun and doing your best."

Encouraged by Ruby's words, Timmy agreed to participate. The other animals were surprised but cheered him on as he took his place at the starting line. When the race began, all the animals dashed off, leaving Timmy far behind. But Timmy didn't mind. He moved at his own pace, enjoying the sights and sounds of the forest."""

# def summarizer(rawdocs):
stopwords = list(STOP_WORDS)
# print(stopwords)
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
# print(doc)
tokens = [token.text for token in doc]
# print(tokens)
word_freq = {}
for word in doc:
  if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
    if word.text not in word_freq.keys():
      word_freq[word.text] = 1
    else:
      word_freq[word.text] += 1

# print(word_freq)

# {'a':1, 'b':2,}
max_freq = max(word_freq.values())
# print(max_freq)

for word in word_freq.keys():
  word_freq[word] = word_freq[word]/max_freq

# print(word_freq)

sent_tokens = [sent for sent in doc.sents]
# print(sent_tokens)

sent_scores = {}
for sent in sent_tokens:
  for word in sent:
    if word.text in word_freq.keys():
      if sent not in sent_scores.keys():
        sent_scores[sent] = word_freq[word.text]
      else:
        sent_scores[sent] += word_freq[word.text]
# print(sent_scores)

select_len = int(len(sent_tokens) * 0.3)
# print(select_len)
summary = nlargest(select_len, sent_scores, key=sent_scores.get)
# print(summary)

final_summary = [word.text for word in summary]
summary = ' '.join(final_summary)
print(text)
print(summary)
print("Lenght of original text ",len(text.split(' ')))
print("Lenght of summary text ",len(summary.split(' ')))
# return summary, doc, len(rawdocs.split(' ')), len(summary.split(''))
  