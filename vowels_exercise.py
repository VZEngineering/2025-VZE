""" This is an exercise produced by Grok 3 on 2/20/25 for me to solve"""


def count_vowels(s):
    s = s.lower()
    vowels = "aeiou"
    return sum(1 for char in s if char in vowels)


while True:
    word = input("\nEnter a word (type 'quit' to exit): ")
    if word.lower() == "quit":
        break
    print("Number of vowels in the word:", count_vowels(word))
