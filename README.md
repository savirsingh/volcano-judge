![image](https://github.com/user-attachments/assets/d64cabb2-2bfc-400b-862b-11faebce55a8)

# Volcano Judge
### A minimalistic &amp; user-friendly competitive programming online judge.

Volcano Judge is an easy-to-use online judge and contest hosting system. You can see a live demo at https://volcanojudge.pythonanywhere.com.

Note that I built this judge as a learning project and it is not necessarily secure or efficient. However, it can be used by school clubs or small organizations looking for a simple solution to host fun programming competitions or events.

## Features
* Support for Python and C++:
  * Python is sandboxed and available by default for all problems.
  * C++ is not sandboxed/secure. It is available by default for contests and **Volcano Judge can compile & run C++ programs**, however, enabling C++ will make the system vulnerable to attacks (note that the C++ code will be isolated from the main directory when running, and safety measures have been enabled to reduce the risk of vulnerabilities).
  * Authors can add custom time limits to all problems, and Volcano Judge will kill processes after the limit is exceeded.
* Easy-to-understand grading:
  * Simple & instantaneous feedback when users submit their code.
  * Enable custom checking & feedback on problems (e.g. a character limit on submissions for code golf style problems).
  * View all feedback codes at https://volcanojudge.pythonanywhere.com/about
* Minimalistic Design:
  * Volcano Judge features a simple **Bootstrap-powered** design.
* Email Verification:
  * Built-in email verification for all users, via the admin's Gmail business account.
* Simple Comment System:
  * Users can comment on all problem objects and can vote on comments authored by other users.
* Announcement/News System:
  * Staff can publish important updates, such as contest announcements. These will be visible on the user dashboard.
* Support for HTML &amp; Latex Problem Statements:
  * When writing problem statements, approved authors may use HTML and Latex for math, tables, images, etc.
* Simple & Extensible Rating System:
  * More details here: https://volcanojudge.pythonanywhere.com/about
* Syntax Highlighting & Autocompletion for Both Python &amp; C++:
  * Volcano Judge integrates the Ace Editor for syntax highlighting & autocompletion.
  * The code editor serves as a working browser-based IDE, with the problem statement visible to the user as they write their code.

## Screenshots
### Simple & Appealing Dashboard Interface
![image](https://github.com/user-attachments/assets/a1b5e4c5-b102-4a6c-a5a7-cb2591317c6d)

### Informative Contest Pages
![image](https://github.com/user-attachments/assets/e473c741-03ab-49b2-9857-e96016f939ed)

### Problem Statement Visible While Writing Code, &amp; Syntax Highlighting + Autocompletion
![image](https://github.com/user-attachments/assets/73314ca2-a8c2-426c-a553-c29a0fc5eca4)

### Enable Dark Mode for Late-Night Competitive Programming Sessions
![image](https://github.com/user-attachments/assets/5a08515f-6855-4849-9f28-9f0462886aba)

### User Rankings by Total Points
![image](https://github.com/user-attachments/assets/642e6bdc-f452-4687-93fb-31ea63a1d2d1)

### Interact With Others in the Comments
![image](https://github.com/user-attachments/assets/057a88d6-4592-4401-841d-5c6dda945c6c)

### Rich Problem Statements With Support for Latex &amp; HTML
![image](https://github.com/user-attachments/assets/f4d61b84-65d2-4ae0-af84-7094a6ce34e1)

### Easy-to-use Admin Interface for Uploading Problems, Publishing Announcements, and Hosting Contests
![image](https://github.com/user-attachments/assets/3ba774d4-43a0-456f-aef0-9740ffe54b51)

## Usage
Volcano Judge features support for grading solutions in Python 3 and C++. These languages should be installed on the machine being used as the server and the grader will make use of version installed.

### Installation
After cloning this repository, run
```
python server.py
```
Now, visit http://127.0.0.1:5000. Your clone of Volcano Judge will be running there.

## Contact
Direct any questions you have about Volcano Judge to savirsinghwork@gmail.com.
