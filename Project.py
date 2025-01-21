# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:50:34 2024

@author: SIDRA
"""
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Create a basic Tkinter window
window = tk.Tk()
window.title("Voice Controlled Contact Manager")
window.geometry("600x400")

# Create a scrolled text widget to display interaction
text_output = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=15, font=("Arial", 12))
text_output.pack(padx=10, pady=10)

# Function to speak and display text
def speak(text):
    engine.say(text)
    engine.runAndWait()
    text_output.insert(tk.END, f"System: {text}\n")
    text_output.yview(tk.END)  # Scroll to the bottom

# Simple contact class to store information
class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

# List to store contacts
contacts = []

# Function to listen to the user's command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say your command.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen to the audio

    try:
        command = recognizer.recognize_google(audio)  # Convert audio to text
        speak("You said: " + command)  # Correctly formatted string for text-to-speech
        text_output.insert(tk.END, f"You: {command}\n")
        text_output.yview(tk.END)  # Scroll to the bottom
        return command.lower()  # Return the command in lowercase
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, I couldn't connect to the speech recognition service.")
        return None

# Function to display contacts in a new window
def display_contacts_window():
    display_window = tk.Toplevel(window)
    display_window.title("View Contacts")
    display_window.geometry("400x300")

    contact_list = tk.Listbox(display_window, width=50, height=10)
    contact_list.pack(padx=10, pady=10)

    if contacts:
        for contact in contacts:
            contact_list.insert(tk.END, f"Name: {contact.name}, Phone: {contact.phone}")
    else:
        contact_list.insert(tk.END, "No contacts available.")

# Function to add a contact manually
def add_contact_manually():
    name = simpledialog.askstring("Input", "Enter the contact's name:")
    if name:
        phone = simpledialog.askstring("Input", "Enter the contact's phone number:")
        if phone:
            new_contact = Contact(name, phone)
            contacts.append(new_contact)
            speak(f"Contact for {name} added successfully.")
            text_output.insert(tk.END, f"System: Contact for {name} added successfully.\n")
            text_output.yview(tk.END)

# Function to add a contact via voice
def add_contact(name, phone):
    new_contact = Contact(name, phone)
    contacts.append(new_contact)
    speak(f"Contact for {name} added successfully.")
    text_output.insert(tk.END, f"System: Contact for {name} added successfully.\n")
    text_output.yview(tk.END)

# Function to search contacts by name
def search_contact(query):
    found = False
    text_output.insert(tk.END, "System: Searching for contact...\n")
    text_output.yview(tk.END)  # Scroll to the bottom
    for contact in contacts:
        if query.lower() in contact.name.lower() or query in contact.phone:
            speak(f"Found: {contact.name} - {contact.phone}")
            text_output.insert(tk.END, f"System: Found: {contact.name} - {contact.phone}\n")
            found = True
    if not found:
        speak(f"No contact found for {query}")
        text_output.insert(tk.END, f"System: No contact found for {query}\n")

# Function to delete a contact by name
def delete_contact(name):
    global contacts
    contacts = [contact for contact in contacts if contact.name != name]
    speak(f"Contact for {name} deleted successfully.")
    text_output.insert(tk.END, f"System: Contact for {name} deleted successfully.\n")
    text_output.yview(tk.END)  # Scroll to the bottom

# Function to update a contact's information
def update_contact(name, new_name, new_phone):
    for contact in contacts:
        if contact.name == name:
            contact.name = new_name
            contact.phone = new_phone
            speak(f"Contact for {name} updated.")
            text_output.insert(tk.END, f"System: Contact for {name} updated.\n")
            text_output.yview(tk.END)  # Scroll to the bottom
            return
    speak(f"No contact found for {name}")
    text_output.insert(tk.END, f"System: No contact found for {name}\n")

# Function to show the menu
def show_menu():
    text_output.insert(tk.END, "**************************************************\n")
    text_output.insert(tk.END, " *** PHONE DIRECTORY MENU *** \n")
    text_output.insert(tk.END, "**************************************************\n")
    text_output.insert(tk.END, "1 - View Contacts\n")
    text_output.insert(tk.END, "2 - Search For a Contact\n")
    text_output.insert(tk.END, "3 - Add Contact\n")
    text_output.insert(tk.END, "4 - Edit Contact\n")
    text_output.insert(tk.END, "5 - Delete Contact\n")
    text_output.insert(tk.END, "6 - Sort Contacts\n")
    text_output.insert(tk.END, "0 - Exit\n")
    text_output.insert(tk.END, "Please select an option by saying the number or clicking.\n")
    text_output.yview(tk.END)  # Scroll to the bottom

# Function to handle the main interaction in a separate thread
def handle_commands():
    while True:
        show_menu()
        command = listen()

        if command:
            if "view contacts" in command or "1" in command:
                display_contacts_window()
            elif "search" in command or "2" in command:
                speak("Please say the name or phone number of the contact you want to search.")
                query = listen()
                if query:
                    search_contact(query)
            elif "add contact" in command or "3" in command:
                speak("Please say the name of the contact.")
                name = listen()
                speak("Please say the phone number of the contact.")
                phone = listen()
                if name and phone:
                    add_contact(name, phone)
            elif "edit" in command or "4" in command:
                speak("Please say the name of the contact you want to edit.")
                name = listen()
                if name:
                    speak("Please say the new name for the contact.")
                    new_name = listen()
                    speak("Please say the new phone number for the contact.")
                    new_phone = listen()
                    if new_name and new_phone:
                        update_contact(name, new_name, new_phone)
            elif "delete" in command or "5" in command:
                speak("Please say the name of the contact you want to delete.")
                name = listen()
                if name:
                    delete_contact(name)
            elif "sort contacts" in command or "6" in command:
                contacts.sort(key=lambda x: x.name.lower())
                speak("Contacts sorted by name.")
                text_output.insert(tk.END, "System: Contacts sorted by name.\n")
                text_output.yview(tk.END)  # Scroll to the bottom
            elif "exit" in command or "0" in command:
                speak("Exiting the program.")
                text_output.insert(tk.END, "System: Exiting the program.\n")
                break
            else:
                speak("Sorry, I didn't understand that command.")
                text_output.insert(tk.END, "System: Sorry, I didn't understand that command.\n")
        else:
            speak("Please try again.")
            text_output.insert(tk.END, "System: Please try again.\n")

# Functions to handle manual buttons for menu options

def on_view_contacts():
    display_contacts_window()

def on_search_contact():
    query = simpledialog.askstring("Input", "Enter the name or phone number of the contact to search:")
    if query:
        search_contact(query)

def on_add_contact():
    add_contact_manually()

def on_edit_contact():
    name = simpledialog.askstring("Input", "Enter the contact name to edit:")
    if name:
        speak("Please say the new name and phone number for the contact.")
        new_name = simpledialog.askstring("Input", "Enter the new contact name:")
        new_phone = simpledialog.askstring("Input", "Enter the new phone number:")
        if new_name and new_phone:
            update_contact(name, new_name, new_phone)

def on_delete_contact():
    name = simpledialog.askstring("Input", "Enter the contact name to delete:")
    if name:
        delete_contact(name)

def on_exit():
    window.quit()

# Adding buttons for manual control
btn_view_contacts = tk.Button(window, text="View Contacts", command=on_view_contacts)
btn_view_contacts.pack(padx=10, pady=5, side=tk.LEFT)

btn_search_contact = tk.Button(window, text="Search Contact", command=on_search_contact)
btn_search_contact.pack(padx=10, pady=5, side=tk.LEFT)

btn_add_contact = tk.Button(window, text="Add Contact", command=on_add_contact)
btn_add_contact.pack(padx=10, pady=5, side=tk.LEFT)

btn_edit_contact = tk.Button(window, text="Edit Contact", command=on_edit_contact)
btn_edit_contact.pack(padx=10, pady=5, side=tk.LEFT)

btn_delete_contact = tk.Button(window, text="Delete Contact", command=on_delete_contact)
btn_delete_contact.pack(padx=10, pady=5, side=tk.LEFT)

btn_exit = tk.Button(window, text="Exit", command=on_exit)
btn_exit.pack(padx=10, pady=5, side=tk.LEFT)

# Start the command handler in a separate thread to avoid blocking the main Tkinter loop
command_thread = threading.Thread(target=handle_commands, daemon=True)
command_thread.start()

# Start the Tkinter main loop
window.mainloop()

