Food Database
A Flask-based web application that imports, stores, and displays nutritional data from the OpenFoodFacts API, with advanced NLP-generated insights for each product.

Skills & Technologies
Languages: Python, SQL
Frameworks & Tools: PostgreSQL, Docker, Hugging Face Transformers

Project Structure
├── app.py                     
├── importer.py                
├── nlp_insights.py   
├── schema.sql                 
├── docker-compose.yml         
├── requirements.txt           
├── templates/                 
│   └── index.html
├── .env.example              
└── .gitignore               

Setup Instructions
1. Clone the Repository
git clone https://github.com/yourusername/Food-Database.git
cd Food-Database

2. Environment Variables
Copy the example .env file:
cp .env.example .env
Edit .env and fill in your credentials:
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=food_db
DB_HOST=db
DB_PORT=5432
API_KEY=your_api_key_here  # Optional, if using NLP API
Note: Never push .env to GitHub. Keep it local for security.

3. Start PostgreSQL with Docker
docker-compose up -d
This will start a PostgreSQL container on port 5432.
Verify the container is running in Docker Desktop or via:
docker ps

4. Create Database Schema
replace all text in caps as needed
psql -h HOST -U USER -d DATABASE -f schema.sql

5. Install Python Dependencies
pip install -r requirements.txt

6. Import Food Data
python importer.py
Fetches data from OpenFoodFacts for specified categories and countries.
Populates your PostgreSQL database with nutritional information and NLP-generated insights.

7. Run the Web Application
python app.py
Open a browser at http://127.0.0.1:5000 to access the web interface.
Use filters to search by category, country, or nutritional values.
