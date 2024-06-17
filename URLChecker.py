"""
Title: URL Image Alt Text Checker
Created by: João S
2024

The URL Image Alt Text Checker application helps users analyze the accessibility of a webpage by checking if images have descriptive alt (Alternative) text.
The concept behind the application is to raise awareness and promote web accessibility by helping developers identify and address missing alt text 
for images, ultimately improving the user experience for visually impaired individuals and thus promote best pratice guidelines.
"""
from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import webbrowser  # Import for opening webpages

# GUI.
# This is the GUI setup for the whole app. It calls tkinter lib to do it. It adds the title and the size.
window = Tk()
window.title("URL Image Alt Text Checker - Final Project - Standford Code In Place 2024 by Joao S.") # App Tittle
window.geometry("880x570") # Regulates the main window size.
window.configure(bg = "alice blue")  # Set background color. Light gray background #F0F0F0 

# This will check the retrieved information for "src" and "alt" 
def check_images(url):
  if not url.startswith("http"): # Checks if "https://" is present in the URL text input given by the user. If not, it will be added to the URL input.
    url = "https://" + url
    
  # Image counter. 
  # Counts total images found on the given URL. It will show Total images, total images with Alt text and total images without Alt text.
  total_images = 0
  images_with_alt = 0
  images_without_alt = 0
  
  # The requests library will retrieve the URL information and BeautifulSoup library will search the HTML code and check for image alt text.
  try:
    response = requests.get(url)    
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    report_text = ""

    for image in images:
      alt_text = image.get('alt', None)
      text = f"IMAGE: {image['src']}\n"
      total_images += 1
      if alt_text:
        text += f"ALT TEXT: {alt_text}"
        images_with_alt += 1
      else:
        # text += "ALT TEXT: None"
        images_without_alt += 1
      report_text += text + "\n\n"
    
    results.delete(0.0, END)  # This clears the text box. From the inicial text position (0.0) to the end of the text box (END).
    results.insert(END, report_text)
    
    # This will display the image count information in a text box.
    image_counts_text.delete(0.0, END) # This clears the text box. From the inicial text position (0.0) to the end of the text box (END).
    summary_text = f"Summary:\n"
    summary_text += f"  - Total Images Found: {total_images}\n"
    summary_text += f"  - Images with Alt Text: {images_with_alt}\n"
    summary_text += f"  - Images without Alt Text: {images_without_alt}\n"
    image_counts_text.insert(END, summary_text)
  
  # Displays error messages about missing or incorrect URL text.
  except requests.exceptions.RequestException as e:
    messagebox.showerror("Error", f"Invalid URL or connection error: {e}. Please check if the URL is correct and try again.")
  except Exception as e:
    messagebox.showerror("Error", f"Error fetching URL: {e}")

def save_report(): # Saves the report to a specific file format. Right now, users can save as .txt, .html, .md and .xml.
  report_text = results.get(1.0, END) # It will get the text from the result box. Tkinter will save the text starting from the beginning (1.0) to the end (END).
  if report_text: # Check if there is any text to save.
    filename = filedialog.asksaveasfilename(
        defaultextension = ".txt",
        filetypes=[
            ("Text files", "*.txt"),
            ("HTML files", "*.html"),
            ("Markdown files", "*.md"),
            ("XML files", "*.xml"),
            ("All files", "*.*")
        ]
    )
    if filename:
      try:
        # Get the chosen extension for the filename.
        extension = filename.split(".")[-1]
        with open(filename, 'w') as file: # Modify the content based on extension (e.g., wrapping in XML tags for .xml). "w" also gives writting permissions.
          if extension.lower() == "xml": # Adds basic XML structure when creating the save file.
            file.write("<report>\n")
            file.write(report_text)
            file.write("</report>\n")
          else:
            file.write(report_text)
        messagebox.showinfo("Success", f"Report saved successfully as {extension}!")
      except Exception as e:
        messagebox.showerror("Error", f"Error saving report: {e}")
  else:
    messagebox.showinfo("Save Report", "There's no report to save yet. Please check images first.")

def show_help(): # It displays a dialog / message box by accessing the Menu (Help section) with "Help" information.
  help_text = (
      "This program is a tool that helps users check the alt text descriptions of images on webpages.\n"
      "\n"
      "Simple to use:\n"
      "1 - Enter an URL (no need to add https://), click 'Check for Alt Text' button and the results with image source and alt text (if present) will be displayed.\n"
      "2 - Use the 'Save Report' option under the File menu to save the results.\n"
      "3 - The report can be saved under several formats (txt, html, md and xml).\n"
  )
  messagebox.showinfo("Help", help_text)

def show_disclaimer(): # It displays a message box by accessing the app Menu (About section) with the "Disclaimer".
  disclaimer_text = (
      "Disclaimer: This program is provided 'as is' and without any warranty.\n"
      "The authors disclaim all responsibility for any damages arising from its use.\n"
      "\n"
      "This program is licensed under the Creative Commons Attribution (CC BY) license.\n"
      "\n"
      "You are free to share and adapt the work, but you must attribute the work to the authors.\n"
      "\n"
      "For more information, visit: https://creativecommons.org/"
  )
  messagebox.showinfo("Disclaimer", disclaimer_text)

def show_about_the_project(): # It displays a message box by accessing the Menu (About section) with the "About the project" information.
  about_the_project_text = (
      "This application was created as a final project for the Standford Code In Place 2024.\n"
      "\n"
      "URL Image Alt Text Checker\n"
      "Created by Joao S\n"
      "2024\n"
      "\n"
      "For more information, visit: https://codeinplace.stanford.edu/\n"
      "\n"
      "Thank you for using the URL Image Alt Text Checker!\n"
      "\n"
      "Feel free to customize this content to fit your specific application and project details."
  )
  messagebox.showinfo("About the Project", about_the_project_text)

def show_alt_text_info(): # It displays a message box by accessing the Menu (About section) with the "What is Alt Text?" information.
  alt_text_info_text = (
      "What is Alt Text?\n"
      "\n"
      "Alternative text (alt text) is a description of an image that conveys its meaning and context in a webpage.\n"
      "\n"
      "Alt text is crucial for web accessibility, enabling visually impaired users who rely on screen readers to understand the content and context of images on a webpage.\n"
      "\n"
      "Screen readers make it possible for people who are blind or low-vision to interact with digital documents, forms, and web pages.\n"
      "\n"
      "Alt text also helps search engine crawlers (bots that search and index webpage content) and users understand images that do not load correctly.\n" 
      "If an image fails to load on a document or web page, then the alt text will be displayed in its place.\n"
      "This makes effective alt text very useful if users have a poor internet connection.\n"
      "\n"
      "Alt text can include the name, colors, shape, setting, tone, and emotion of an image.\n"
  )
  messagebox.showinfo("Best Practices", alt_text_info_text)

def show_best_practices(): # It displays a message box by accessing the Menu (About section) with the "About the project" information.
  best_practices_text = (
      "Good alt text is concise, descriptive, and provides the same functional information that the image conveys to sighted users. It's an essential part of making web content accessible to everyone.\n"
      "\n"
      "Some common alt text mistakes:\n"
      "\n"
      "- Omitting alt text: Not providing any alt text is a significant oversight, as it leaves visually impaired users without any context for the image.\n"
      "\n"
      "- Vague descriptions: Alt text like “dog” is too general and doesn’t offer enough detail about the image’s content.\n"
      "\n"
      "- Overly complex language: Using jargon or complex terms can make the alt text difficult to understand.\n"
      "\n"
      "- Ignoring the context: Alt text should relate the image to the surrounding content, not just describe it in isolation.\n"
      "\n"
      "- Repeating the caption: If the image has a caption, the alt text should not simply repeat it.\n"
      "\n"
      "- Missing out on function: If an image is also a button or link, the alt text should describe its function, not just its appearance.\n"
      "\n"
      "- Not updating alt text: Alt text should be reviewed and updated to ensure it remains relevant and accurate.\n"
  )
  messagebox.showinfo("Best Practices", best_practices_text)

# Calls the webbrowser library to open webpages
def open_webpage(url): # Opens the provided URL (https link) found in the Resources menu, using the user's prefered web browser independent of what OS is being used.
    webbrowser.open(url)

# THE MENU BAR. 
# This creates the Menu. So far it includes: File tab -> Save Report and Exit, Resources tab -> What is Alt Text, Best Practices and Resource Links (currently with 3 links), Help tab -> Help, About the Project and Disclaimer.
menu_bar = Menu(window)
window.config(menu=menu_bar)

# FILE MENU
file_menu = Menu(menu_bar, tearoff=0) # Creates the File Menu tab. It contains 2 categories, Save Report and Exit.
file_menu.add_command(label="Save Report", command=save_report) # Creates the "Save Report" Menu. It will show options to save the report to a file.
file_menu.add_separator() # Adds a space (line) dividing the labels.
file_menu.add_command(label="Exit", command=window.destroy)  # Creates the "Exit" command. It will close the application.
menu_bar.add_cascade(label="File", menu=file_menu)

# RESOURCES MENU
resources_menu = Menu(menu_bar, tearoff=0) # Creates the Resources Menu tab. It contains 3 categories: What is Alt Text, Best Practices and Resources Links with 3 links with information regarding best practices and other information.
resources_menu.add_command(label="What is Alt Text?", command=show_alt_text_info) # Creates the "What is Alt Text?" Menu and content.
resources_menu.add_command(label="Best Practices", command=show_best_practices) # Creates the "Best Practices" Menu and content.
resources_submenu = Menu(menu_bar, tearoff=0) # Adds a space (line) dividing the labels.
resources_submenu.add_command(label="WC3 Web Accessibility Initiative", command=lambda: open_webpage("https://www.w3.org/WAI/")) # Resource Link.
resources_submenu.add_command(label="Standford Code in Place", command=lambda: open_webpage("https://codeinplace.stanford.edu/")) # Resource Link.
resources_submenu.add_command(label="Teach Access", command=lambda: open_webpage("https://teachaccess.org/")) # Resource Link
resources_menu.add_cascade(label='Resource Links', menu=resources_submenu, underline=0) # Creates the submenu under Resource Links
menu_bar.add_cascade(label="Resources", menu=resources_menu)

# HELP MENU
help_menu = Menu(menu_bar, tearoff=0) # Creates the Help Menu tab. It contains 3 categories, Help, About the Project and Disclaimer.
help_menu.add_command(label="Help", command=show_help) # Creates the "Help" Menu and message content.
help_menu.add_command(label="About the Project", command=show_about_the_project) # Creates the "About the Project" Menu and message content.
help_menu.add_command(label="Disclaimer", command=show_disclaimer) # Creates the "Disclaimer" Menu and message content.
menu_bar.add_cascade(label="Help", menu=help_menu)

# URL Input
url_label = Label(window, text="Enter URL either by typing the URL address or copy paste it here:", bg = "alice blue")
url_label.pack()

# PLACEHOLDER FOR THE URL TEXT BOX (entry)
def on_entry_click(event): # This will be used when the URL Input text box (entry) is clicked.
    if url_entry.get() == "https://":
       url_entry.delete(0, "end") # This clears the text box. From the inicial text position (0) to the end of the text box (END).
       #url_entry.insert(0, "") # Insert blank for user input.
       url_entry.config(fg = "black")

def on_focusout(event):
    if url_entry.get() == "":
        url_entry.insert(0, "https://")
        url_entry.config(fg = "grey")

# URL TEXT BOX
url_entry = Entry(window, width=60, relief = "solid") # Creates the URL text Box. The user will provide the URL, either by typing of copy-paste.
url_entry.insert(0, "https://") # Displays the text "https://" as a placeholder in the Input text box.
url_entry.bind("<FocusIn>", on_entry_click)
url_entry.bind("<FocusOut>", on_focusout)
url_entry.config(fg = "grey")
url_entry.pack()

# URL TEXT BOX SUBMIT BUTTON
check_button = Button(window, text="Check for Alt Text", command = lambda: check_images(url_entry.get())) # Creates the submit button for the chosen URL (the input from the URL Text Box).
check_button.pack()

# RESULTS TEXT AND BOX
results_label = Label(window, text="Here are the Results:", bg = "alice blue") 
results_label.pack(pady=10)

results = Text(window, bg = "light cyan", width=100, height=19, relief = "solid") # Creates the Text box that will display the output given by the URL Input. 
results.pack()

# IMAGE COUNTER TEXT BOX
# Creates the label and text box that will display the image count. It will display the total images found in the URL, the total images that contain Alt text and the total images without Alt text.
image_counts_label = Label(window, text="Image Count:", bg = "alice blue")
image_counts_label.pack(pady=10)

image_counts_text = Text(window, height=5, width=40, relief = "solid")  # Creates the text box for the image counter.
image_counts_text.pack()

window.mainloop() # A small note to me: The mainloop method is what keeps the root window visible (tkinter). If I remove the line, the app stops running.