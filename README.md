# Kobe Halal Food Guide 🇯🇵

## 📖 About the Project
This project was developed as part of the **Fundamentals of Computer Programming Python (2025-2026)** course at **Kobe Institute of Computing (KIC)**.

📄 **[Class Presentation](presentation/presentation.pdf)**

### The Problem
Finding reliable **Halal food** in Japan can be difficult for Muslim residents and tourists. Information is often scattered or outdated.

### The Solution
This web application solves this real-world problem by providing a trusted guide for Halal restaurants and grocery stores in Kobe. The goal is to apply Python programming skills to build a useful tool that serves the community.

---

## 🌐 Live Demo
You can try the live version of the application here:
👉 **[Kobe Halal Food Guide (Live)](https://halal.project.com.ly)**

### 🔐 Admin Access
You can explore the **Admin Dashboard** features (Read-Only Mode).
* Navigate to the login page.
* **Credentials are provided on the screen.**
* Simply **click the "Demo Access" box** to auto-fill the username and password.

---

## 🛠️ Technologies & Libraries
This project is built using **Python** and **Django**. It uses several libraries to ensure a modern design and powerful features:

* **Django:** The main web framework.
* **Django Unfold:** For a beautiful and modern Admin Dashboard.
* **BeautifulSoup4 & Requests:** For web scraping real data.
* **Faker:** To generate dummy data for testing.
* **Pillow:** For handling image uploads.
* **Tailwind CSS:** Used via CDN for styling the public interface.
* **FontAwesome:** For icons.

---

## 🚀 How to Run the Project

Follow these steps to set up the project on your local machine (Mac/Linux):

### 1. Create a Virtual Environment
First, create an isolated environment to keep the project clean.

```bash
python -m venv .venv
```

### 2. Activate the Environment

You need to activate the environment before installing dependencies.

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows (CMD / PowerShell):**

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required libraries:

```bash
pip install -r requirements.txt
```

### 4. Setup the Database

Create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an Admin User (Superuser)

To access the dashboard, create an admin account:

```bash
python manage.py createsuperuser
```

### 6. Run the Server

Start the project:

```bash
python manage.py runserver
```

Now, open your browser and go to: `http://127.0.0.1:8000`

---

## ⚙️ Management Commands (Optional)

This project includes custom commands to help manage data easily. You can run these from the terminal.

### 1. Scrape Real Data

Fetches real restaurant data (Names, Photos, Locations, Coordinates) from the web to populate your database.

```bash
python manage.py scrape_halal
```

### 2. Seed Fake Data

If you want to test the design with random dummy data (names, random food images).

```bash
python manage.py seed_data
```

### 3. Clear Database

Deletes all restaurants, cities, and categories, and **cleans up the media folder** to remove unused images.

```bash
python manage.py clear_data
```

---

## 👨‍💻 Developer Info

**Name:** Firas Aldweni

**Course:** M1 Innovator - JICA ABE Initiative

**Email:** [contact@firas.ly](mailto:contact@firas.ly)

---

*Built with ❤️ for the Muslim community in Kobe.*