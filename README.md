<p align="center">
  <a href="https://oaoS-Dev/Standford-Code_In_Place-Final-Project-2024">
    <img src="https://github.com/JoaoS-Dev/Standford-Code_In_Place-Final-Project-2024/assets/172130901/5f77553f-3f48-4e28-aa5f-c81f1b65540a" alt="Logo displaying the Name of the application, URL Image Alt Text Checker, the student name and an image of Karel the robot" >
  </a>
  <div align="center">
  <h3>
    <a href="codeinplace.standford.edu">
      Code In Place
    </a>
    <span> | </span>
    <a href="https://www.w3.org/WAI/">
      Userful Resources
    </a>
  </h3>
</div>
</P>

![coverfp](https://github.com/JoaoS-Dev/Standford-Code_In_Place-Final-Project-2024/assets/172130901/e9092088-2d12-45aa-ba3b-424955459147)

# Code in Place Final Project 2024

**Stanford University** **"Code in Place"** Run by Prof. Mehran Sahami and Prof. Chris Piech.
### Final Project Description

**URL Image Alt Text Checker**<br/>
This program helps check for the existence of alt text in images on a website.<br/>

The **URL Image Alt Text Checker** application helps users analyze the accessibility of a webpage by checking if images have descriptive alt text.
The concept behind the application is to raise awareness and promote web accessibility by helping developers identify and address missing alt text 
for images, ultimately improving the user experience for visually impaired individuals and thus promote best pratice guidelines. The idea came after 
participating in a webinar event named "Panel: Accessibility in Tech & Education", promoted by Code in Place.

For more information, please visit the <a href="https://www.w3.org/WAI/"> WC3 Web Accessibility Initiative</a> for strategies, standards and resources to make the Web accessible 
to people with disabilities

 
# Programming Language and Environment used:<br/> 
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](#features)

 - **Python:** This project is written in Python, the programming language being taught at Code in Place. It is a versatile and beginner-friendly programming language. **Python version** 3.10.2<br/>
 - **VSCode:** Code in Place uses its own IDE but I chose to use Visual Studio Code (VS Code) due to the fact that I needed external libraries that were not available in the 
Code in Place IDE.<br/>

This IDE is a popular open-source code editor (from Microsoft). It is easy to install, import libraries and can connect to github making it easy to operate.

**Modules/Libraries used:**

- **requests:** Used to fetch the HTML content of the webpage from the provided URL. It facilitates making HTTP requests in Python.
- **BeautifulSoup:** Used to parse the fetched HTML content from request. It simplifies navigating and extracting information from the HTML structure.
- **tkinter:** Used for creating the graphical user interface (GUI) such as the text box for URL input, results display and image count (text widget) and error messages (messagebox).
- **webbrowser:** It provides an interface for users to view Web-based content. It will displays web-based documents or web pages.

# **How it works:**

 - Takes an user URL input either by typing or using copy-paste.
 - Checks if the URL starts with "https://" and adds it, if not present.
 - Fetches the HTML content of the webpage using the provided user URL input and parses the HTML to find all image tags (<img>).
 - For each image, it extracts the source URL (src attribute) and checks if it has an alt text attribute (alt).
 - Generates a report text containing information for each image:
     * Image source URL
     * Alt text (if available)
 - It also keeps track of the total number of images found, images with alt text, images without alt text and displays it in the GUI.

### Instructions to use this program in the correct manner:
  1. Enter a URL (no need to add https://), click 'Check for Alt Images', and the results with image source and alt text (if present) will be displayed.<br/>
  
  ![final1](https://github.com/JoaoS-Dev/Standford-Code_In_Place-Final-Project-2024/assets/172130901/545c7bf4-436a-4b62-b2a3-c1b3ff5ad8df)<br/>
  #
  
  2. Use the 'Save Report' option under the File menu to save the results.<br/>
  
  ![final2](https://github.com/JoaoS-Dev/Standford-Code_In_Place-Final-Project-2024/assets/172130901/9dc3532c-3ff9-4a89-8c17-713fcc4e0481)<br/>
  #
  
  3. The report can be saved under several formats (txt, html, md and xml).<br/>
  ![fp3](https://github.com/JoaoS-Dev/Standford-Code_In_Place-Final-Project-2024/assets/172130901/4cce938f-aae2-473e-bdc9-5e96ae5e14ee)<br/>
  #
  
  Here we can see a full print of the URL Image Alt Text Checker main screen.<br/>
  
  ![final5](https://github.com/JoaoS-Dev/Standford-Code_In_Place-Final-Project-2024/assets/172130901/74823ffd-df1b-44be-afe6-605d9c1936e5)

**Version:** 0.1

## About Standford's Code in Place
The Stanford Code in Place is free an online course offered by Stanford University, designed to teach the fundamentals of computer programming using Python. 
The course is based on Stanford's introductory programming course, CS106A.

The course is delivered through a combination of pre-recorded lectures, live sessions, and assignments. It includes a significant hands-on component 
where students work on coding exercises, projects and weekly live zoom meetings with teachers, called Section Leaders.

The course fosters a sense of community among participants through discussion forums, study groups, and collaborative projects. This helps create an 
engaging and supportive learning environment. It aims to democratize access to high-quality computer science education.

Overall, Stanford Code in Place is an initiative to make computer science education more accessible and to build a global community of learners.<br/>

For more information, please visit: <a href="https://codeinplace.standford.edu">Code in Place</a><br/>

![finalProject 000a6207](https://github.com/JoaoS-Dev/Standford-Code_In_Place-Final-Project-2024/assets/172130901/e2d61940-80f9-4aec-96c1-aa2620ef7684)<br/>
Credits: Artist's Name: <a href="https://www.deviantart.com/xbooshbabyx">xbooshbabyx</a> 
Image Link and Name: <a href="https://www.deviantart.com/xbooshbabyx/art/Imagination-124194321">Imagination</a>
