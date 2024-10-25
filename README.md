# ISNA Article Scraper API

## Description
A backend service that scrapes the latest articles from the Culture and Art section of the ISNA website, stores the data in a PostgreSQL database, and provides CRUD operations via Django REST Framework.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Installation
1. Clone the repository: `git clone <repo-url>`
2. Navigate to the directory: `cd your-project-name`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up your PostgreSQL database and update settings in `settings.py`.

## Usage
1. Run the migrations: `python manage.py migrate`
2. Create a superuser: `python manage.py createsuperuser`
3. Run the application: `python manage.py runserver`
4. Trigger scraping: `python manage.py scrape_isna`

## API Endpoints
- **GET** `/api/articles/`: List all articles.
- **GET** `/api/articles/<id>/`: Retrieve a specific article.
- **POST** `/api/articles/`: Add a new article.
- **PUT** `/api/articles/<id>/`: Update an existing article.
- **DELETE** `/api/articles/<id>/`: Delete an article.

## Contributing
Feel free to submit a pull request or open an issue for any enhancements or bugs.

## License
This project is licensed under the MIT License.
