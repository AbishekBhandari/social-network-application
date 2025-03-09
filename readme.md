# Social Network Project

## Overview
This project is a simple social networking web application that allows users to create posts, follow other users, and like posts. The application is built using Python (Django), JavaScript, HTML, and CSS. It also includes features such as pagination, user profiles, and the ability to edit and like posts dynamically.

## Features
### 1. All Posts
- Users can view all posts from all users, with the latest posts displayed first.
- Each post includes the username, post content, timestamp, and the number of likes.

### 2. New Post
- Authenticated users can create new posts by submitting text via a textarea.
- Posts appear in reverse chronological order.

### 3. Profile Page
- Clicking on a username redirects to their profile page.
- Displays the number of followers and people the user follows.
- Shows all posts made by the user in reverse chronological order.
- Users can follow/unfollow other users (except themselves).

### 4. Following Page
- Users can see posts only from people they follow.
- Available only to authenticated users.

### 5. Pagination
- Posts are displayed 10 per page.
- "Next" and "Previous" buttons allow navigation through pages.

### 6. Edit Post
- Authenticated Users can edit their own posts by clicking an "Edit" button.
- Edits are handled dynamically using JavaScript, without page reloads.
- Security measures ensure that users cannot edit others' posts.

### 7. Like/Unlike
- Authenticated Users can like and unlike posts with a single click.
- Likes are updated asynchronously using JavaScript (via `fetch`).
- The like count updates dynamically without reloading the page.

## Installation & Setup

### Prerequisites
- Python 3.x
- Django
- JavaScript (Vanilla JS)
- SQLite (default for Django) or any other database supported by Django

### Steps to Run the Project
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/AbishekBhandari/social-network-application.git
   cd social-network-application
   ```

2. **Create a Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```sh
   python manage.py makemigrations network
   python manage.py migrate
   ```

5. **Create a Superuser (Optional):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the Server:**
   ```sh
   python manage.py runserver
   ```

7. **Access the Application:**
   Open a web browser and go to `http://127.0.0.1:8000/`.

## Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (or other Django-supported databases)
- **Authentication:** Django built-in authentication system

## Future Improvements
- Add user comments on posts.
- Implement real-time notifications using WebSockets.
- Enhance the UI with better design frameworks like Bootstrap or Tailwind CSS.

## License
This project is open-source and created as part of CS50W project

## Author
Abishek Bhandari

