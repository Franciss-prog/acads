# My Portfolio Website

This is a simple website to show who I am and what I do. It includes my projects, a bit about me, and ways to contact me. It's built with basic web technologies: **HTML**, **CSS (Tailwind CSS)**, and **JavaScript**.

## Website Overview

- **Home Page**: A main page with an interactive terminal header and links to other pages.
- **About Page**: Information about me, including my hobbies and the programming languages I use.
- **Portfolio Page**: A list of projects I have worked on, with links to their code and live versions.
- **Contact Page**: Links to my social media profiles so you can contact or follow me.

---

## Files in This Project

### 1. `index.html` (Home Page)
This page is where you start. It shows:
- A **navbar** for easy navigation.
- A **terminal-style header** for a cool effect.
- Links to my **projects** and **contact** information.

### 2. `about.html` (About Page)
This page tells you:
- Who I am.
- What I enjoy doing (like coding, cycling, and playing games).
- The **tech stack** (programming languages and tools) I work with, with links to learn more about each one.

### 3. `portfolio.html` (Portfolio Page)
This page shows:
- A list of my **projects** with details about each one.
- Links to see the code or live version of each project.

### 4. `contact.html` (Contact Page)
Here, you can find:
- Links to my **social media** profiles like **GitHub**, **LinkedIn**, **Instagram**, and **Facebook**.

### 5. `global.css`
This file adds styles to the website. It:
- Uses **Tailwind CSS** for easy styling.
- Makes the website look nice and modern.
- Hides the scrollbar to keep the page clean.

### 6. `script.js`
This file makes the website interactive. It:
- Shows the current page in the navbar.
- Toggles the menu on smaller screens (for mobile devices).
- Opens a **modal** with more details when you click on a project.

---

## How to Use the Website

1. Open the website by clicking on any of the **HTML** files (e.g., `index.html`, `about.html`, `portfolio.html`, `contact.html`) in your browser.
2. You can click the links in the navbar to move between pages (Home, About, Portfolio, and Contact).
3. On smaller screens (like phones), the navbar will turn into a button you can click to open the menu.

---

## How to Add a New Project

To add a new project to your portfolio:

1. Open `script.js`.
2. Find the **projects** array in the file.
3. Add a new project by copying and pasting an existing one and changing the details:
   - `name`: The name of your project.
   - `description`: A short description of the project.
   - `sourceCode`: A link to the code (e.g., GitHub).
   - `livePreview`: A link to the live project (if available).
   - `image`: A link to an image for the project.

Example:
```javascript
{
  name: "New Project",
  description: "A short description of the project.",
  sourceCode: "https://github.com/username/newproject",
  livePreview: "https://newproject.example.com",
  image: "https://example.com/project-image.jpg"
}
