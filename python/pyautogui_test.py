import pyautogui
import time

# Function to open Notepad
def open_notepad():
    pyautogui.press('win')  # Press the Windows key
    time.sleep(1)
    pyautogui.typewrite('notepad')  # Type 'notepad'
    pyautogui.press('enter')  # Press Enter
    time.sleep(2)  # Wait for Notepad to open

# Function to type text
def type_text(text):
    pyautogui.typewrite(text, interval=0.1)  # Type each character with a short delay

# Function to save the file
def save_file(filename):
    pyautogui.hotkey('ctrl', 's')  # Open the Save As dialog
    time.sleep(2)
    pyautogui.typewrite(filename)  # Type the filename
    pyautogui.press('enter')  # Press Enter to save

# Main script
if __name__ == "__main__":
    open_notepad()
    type_text("Hello! This is an automated message written by PyAutoGUI.\nHave a great day!")
    time.sleep(1)
    save_file("automated_note.txt")
    print("Automation complete!")
