#import the required libraries~!

import time
import threading
import logging

# Configure logging
logging.basicConfig(filename='countdown_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def countdown(t, event):
    """Counts down from t to 0, printing each number and logging the progress."""
    logging.info(f'Starting countdown for {t} seconds.')
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print('Countdown complete!')
    logging.info('Countdown complete.')
    event.set()  # Signal that the countdown is complete

def display_message(message, event):
    """Waits until the countdown is complete and then displays the message."""
    event.wait()
    print(message)
    logging.info(f'Message displayed: {message}')

def get_valid_integer(prompt):
    """Prompts the user for an integer and validates the input."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def main():
    while True:
        try:
            num_countdowns = get_valid_integer("How many countdowns would you like to set? ")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    for i in range(num_countdowns):
        print(f"\nCountdown {i + 1}:")
        duration = get_valid_integer("Enter the countdown duration in seconds: ")

        # Create an event object to signal the end of the countdown
        countdown_complete_event = threading.Event()

        # Start the countdown
        countdown_thread = threading.Thread(target=countdown, args=(duration, countdown_complete_event))
        countdown_thread.start()

        # Get input from the user for the message to be displayed
        message = input("Enter a message to be displayed after the countdown: ")

        # Start a separate thread to display the message
        message_thread = threading.Thread(target=display_message, args=(message, countdown_complete_event))
        message_thread.start()

        # Wait for both threads to finish
        countdown_thread.join()
        message_thread.join()

        # Prompt to run another countdown or exit
        while True:
            again = input("Would you like to set another countdown? (yes/no): ").strip().lower()
            if again in ['yes', 'no']:
                break
            print("Invalid input. Please type 'yes' or 'no'.")

        if again == 'no':
            print("Thank you for using the countdown program!")
            logging.info('Program terminated by user.')
            break

if __name__ == "__main__":
    main()
