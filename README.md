# Shopping Website

## Overview

This project is a **shopping website** built using **Streamlit** for the frontend and **FastAPI** for the backend. It follows the **MVC architecture** (Models, Views, Controllers) and utilizes a **MySQL database** with pre-inserted items. The entire system is containerized with **Docker**, and dependencies are managed via a `requirements.txt` file. A `docker-compose.yml` file is provided for easy deployment.

## Features

- **User Registration & Authentication** – Users can sign up and log in.
- **Item Browsing** – All users can view available items.
- **Order Creation** – Logged-in users can place orders.
- **Favorite Items List** – Users can add items to their favorites.
- **AI Chat Assistant** – AI-powered assistant provides details about available items.

## Tech Stack

| Component    | Technology  |
|-------------|------------|
| **Frontend**  | Streamlit  |
| **Backend**   | FastAPI    |
| **Database**  | MySQL (with pre-inserted item data) |
| **Architecture** | MVC (Models, Views, Controllers) |
| **Containerization** | Docker & Docker Compose |

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation & Running

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/shopping-website.git
   cd shopping-website
   ```

2. Update the OpenAI API key in the configuration file:
   ```sh
   export OPENAI_API_KEY=YOUR_API_KEY_HERE
   ```

3. Build and run the containers:
   ```sh
   docker-compose up --build
   ```

4. Start the backend:
   ```sh
   python main.py
   ```

5. Start the frontend:
   ```sh
   streamlit run app.py
   ```

### Access the Website
- **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
- **MySQL Database:** Runs internally on Docker

## Environment Variables
Ensure the following environment variables are set before running the application:
```sh
MYSQL_USER=<your_mysql_user>
MYSQL_PASSWORD=<your_mysql_password>
MYSQL_DB=<your_database_name>
MYSQL_HOST=mysql
MYSQL_PORT=3306
OPENAI_API_KEY=<your_openai_api_key>
```

## Notes
- **API Key Requirement:** The OpenAI API key is not included in the config file and must be updated manually.
- **Database Persistence:** Ensure that MySQL container volumes are properly configured to avoid data loss.
- **Pre-inserted Items:** The MySQL database includes initial data to populate the store.

## Contributors
- **Your Name** – [GitHub Profile](https://github.com/david-menahem)

