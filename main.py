#import the required libraries
import time
import threading

def countdown(t):
  
  #takes an int t and counts down from t to 0, printing each number from it
  
  while t:
    mins, secs = divmod(t, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    print(timer, end="\r")
    time.sleep(1)
    t -= 1
  print('Countdown complete!')

def display_message(message):

  time.sleep(5)  # Wait for 5 seconds before displaying the message
  print(message)

# Get input from the user for the countdown duration
duration = int(input("Enter the countdown duration in seconds: "))

# Start the countdown
countdown_thread = threading.Thread(target=countdown, args=(duration,))
countdown_thread.start()

# Get input from the user for the message to be displayed
message = input("Enter a message to be displayed after the countdown: ")

# Start a separate thread to display the message
message_thread = threading.Thread(target=display_message, args=(message,))
message_thread.start()

# Wait for both threads to finish
countdown_thread.join()
message_thread.join()
