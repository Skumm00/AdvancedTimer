# Import the required libraries
import time
import threading
import logging
import json
import os

# Configure logging
logging.basicConfig(filename='countdown_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class CountdownTimer:
    def __init__(self, duration, name=""):
        self.duration = duration
        self.remaining_time = duration
        self.paused = False
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.name = name

    def countdown(self):
        logging.info(f'Starting countdown for {self.name} ({self.duration} seconds).')
        while self.remaining_time > 0:
            if self.paused:
                time.sleep(1)
                continue

            mins, secs = divmod(self.remaining_time, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(f"{self.name}: {timer}", end="\r")
            time.sleep(1)
            with self.lock:
                self.remaining_time -= 1

        print(f"{self.name}: Countdown complete!")
        logging.info(f'Countdown complete for {self.name}.')
        self.event.set()

    def pause(self):
        with self.lock:
            self.paused = True

    def resume(self):
        with self.lock:
            self.paused = False

    def adjust_time(self, new_duration):
        with self.lock:
            self.remaining_time = new_duration
            self.duration = new_duration

    def is_complete(self):
        return self.remaining_time == 0

    def get_status(self):
        return {
            'name': self.name,
            'remaining_time': self.remaining_time,
            'paused': self.paused
        }

def display_message(message, event):
    event.wait()
    print(message)
    logging.info(f'Message displayed: {message}')

def get_valid_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_valid_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

def save_configurations(config):
    try:
        with open('countdown_config.json', 'w') as file:
            json.dump(config, file, indent=4)
        print("Configurations saved.")
    except IOError as e:
        print(f"Failed to save configurations: {e}")
        logging.error(f"Failed to save configurations: {e}")

def load_configurations():
    try:
        with open('countdown_config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Error reading configuration file: {e}")
        logging.error(f"Error reading configuration file: {e}")
        return []

def delete_configuration():
    try:
        os.remove('countdown_config.json')
        print("Configuration file deleted.")
    except IOError as e:
        print(f"Failed to delete configuration file: {e}")
        logging.error(f"Failed to delete configuration file: {e}")

def list_configurations(configurations):
    if not configurations:
        print("No configurations found.")
    else:
        for idx, cfg in enumerate(configurations, start=1):
            print(f"Config {idx}: Duration: {cfg.get('duration')} seconds, Message: {cfg.get('message')}")

def check_status(timers):
    for timer in timers:
        status = timer.get_status()
        status_str = f"Name: {status['name']}, Remaining Time: {status['remaining_time']} seconds, Paused: {status['paused']}"
        print(status_str)

def display_remaining_time(timers):
    for timer in timers:
        mins, secs = divmod(timer.remaining_time, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)
        print(f"{timer.name}: {timer_str}")

def save_preferences(preferences):
    try:
        with open('user_preferences.json', 'w') as file:
            json.dump(preferences, file, indent=4)
        print("User preferences saved.")
    except IOError as e:
        print(f"Failed to save user preferences: {e}")
        logging.error(f"Failed to save user preferences: {e}")

def load_preferences():
    try:
        with open('user_preferences.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Error reading preferences file: {e}")
        logging.error(f"Error reading preferences file: {e}")
        return {}

def main():
    countdown_threads = []
    message_threads = []
    timers = []

    preferences = load_preferences()

    while True:
        try:
            action = input("Choose an action - [1] Set countdowns, [2] List configurations, [3] Delete configurations, [4] Check status, [5] Display remaining time, [6] Save preferences, [7] Exit: ").strip()
            if action == '1':
                num_countdowns = get_valid_integer("How many countdowns would you like to set? ")
                configurations = load_configurations()

                for i in range(num_countdowns):
                    print(f"\nCountdown {i + 1}:")
                    duration = get_valid_integer("Enter the countdown duration in seconds: ")
                    name = get_valid_string("Enter a name for this countdown: ")

                    timer = CountdownTimer(duration, name)
                    timers.append(timer)

                    countdown_thread = threading.Thread(target=timer.countdown)
                    countdown_threads.append(countdown_thread)
                    countdown_thread.start()

                    message = get_valid_string("Enter a message to be displayed after the countdown: ")

                    message_thread = threading.Thread(target=display_message, args=(message, timer.event))
                    message_threads.append(message_thread)
                    message_thread.start()

                    while True:
                        action = input("Would you like to pause, resume, adjust, or continue? (pause/resume/adjust/continue): ").strip().lower()
                        if action == 'pause':
                            timer.pause()
                            print("Countdown paused.")
                        elif action == 'resume':
                            timer.resume()
                            print("Countdown resumed.")
                        elif action == 'adjust':
                            new_duration = get_valid_integer("Enter the new countdown duration in seconds: ")
                            timer.adjust_time(new_duration)
                            print("Countdown adjusted.")
                        elif action == 'continue':
                            break
                        else:
                            print("Invalid input. Please type 'pause', 'resume', 'adjust', or 'continue'.")

                    countdown_thread.join()
                    message_thread.join()

                    if input("Would you like to save the current configuration? (yes/no): ").strip().lower() == 'yes':
                        configurations.append({'name': name, 'duration': duration, 'message': message})
                        save_configurations(configurations)

                    while True:
                        again = input("Would you like to set another countdown? (yes/no): ").strip().lower()
                        if again in ['yes', 'no']:
                            break
                        print("Invalid input. Please type 'yes' or 'no'.")

                    if again == 'no':
                        print("Thank you for using the countdown program!")
                        logging.info('Program terminated by user.')
                        return

            elif action == '2':
                configurations = load_configurations()
                list_configurations(configurations)

            elif action == '3':
                if input("Are you sure you want to delete the configuration file? This action cannot be undone. (yes/no): ").strip().lower() == 'yes':
                    delete_configuration()

            elif action == '4':
                check_status(timers)

            elif action == '5':
                display_remaining_time(timers)

            elif action == '6':
                preferred_format = get_valid_string("Enter your preferred time format (e.g., HH:MM:SS or MM:SS): ")
                preferences['time_format'] = preferred_format
                save_preferences(preferences)
                print("Preferences saved.")

            elif action == '7':
                print("Exiting program. Thank you!")
                logging.info('Program exited by user.')
                return

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
