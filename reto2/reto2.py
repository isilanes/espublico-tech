"""
reto2.py: script de Python para resolver el Reto 2 de esPublico.tech (https://espublico.tech/reto/2).
"""

__author__ = "Iñaki Silanes Cristóbal"
__copyright__ = "Copyright 2019, Iñaki Silanes Cristóbal"
__email__ = "isilanes@gmail.com"

# Standard libs:


# Functions:
def main():
    word = "1[h2[ol2[a]]]"
    res = translate_word(word)
    print(res)


def translate_word(word):
    """Translate a single word."""
    
    # If no [ ] in word, return word itself:
    if "[" not in word:
        return word
    
    # Read from left up to first [:
    left = ""
    multiplier = ""
    for i, letter in enumerate(word):
        if letter == "[":
            break
        
        try:
            x = int(letter)
            multiplier += letter
        except ValueError:
            left += letter
    
    # Read from right up to first ]:
    right = ""
    for j, letter in enumerate(word[::-1]):
        if letter == "]":
            break
        
        right += letter
    
    right = right[::-1]
    
    # Text in the middle, and how many times to multiply it:
    middle = word[i+1:-j-1]
    multiplier = int(multiplier)
    
    return left + multiplier*translate_word(middle) + right
    

# Main:
if __name__ == "__main__":
    main()
