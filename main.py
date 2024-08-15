#import the required random libraries
import random

def generate_word(word_list):
    return random.choice(word_list)

def get_guess():
    while True:
        guess = input("Enter your guess: ").lower()
        if len(guess) == 1 and guess.isalpha():
            return guess
        else:
            print("Please enter only one letter.")

def check_guess(guess, word):
    if guess in word:
        return f"Good guess! {guess} is in the word."
    else:
        return f"Sorry, {guess} is not in the word."

def is_palindrome(word):
    return word == word[::-1]

def provide_hint(word, guesses):
    hint = ""
    for letter in word:
        if letter in guesses:
            hint += letter
        else:
            hint += "_"
    return f"Hint: {hint}"

def play_game(difficulty, word_list):
    word = generate_word(word_list)
    word_set = set(word)
    guesses = []
    max_guesses = {'easy': 7, 'medium': 5, 'hard': 3}[difficulty]
    print(f"\nDifficulty: {difficulty.capitalize()}")
    print(f"The word is {len(word)} letters long.")
    print("Hint: It's a palindrome!")

    while len(guesses) < max_guesses:
        guess = get_guess()
        if guess in guesses:
            print("You already guessed that letter. Try again.")
        else:
            guesses.append(guess)
            print(check_guess(guess, word))

            guessed_letters = set(guesses)
            if guessed_letters == word_set:
                print(f"Congratulations! You guessed the word: {word}.")
                return True

            guessed_letters_str = "".join(sorted(guesses))
            if is_palindrome(guessed_letters_str):
                print("You've guessed a palindrome!")

            if difficulty == 'hard' and len(guesses) == max_guesses - 2:
                print("Warning: You're close to running out of guesses!")
            if difficulty == 'medium' and len(guesses) == max_guesses - 3:
                print("Hint: You're getting closer!")

            # Provide a hint if guesses are getting low
            if len(guesses) >= max_guesses - 3:
                print(provide_hint(word, guesses))

    print(f"Sorry, you ran out of guesses! The word was {word}")
    return False


if __name__ == "__main__":
    main()
