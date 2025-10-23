# Food Database
A Flask-based web application that imports, stores, and displays nutritional data from the OpenFoodFacts API, with advanced NLP-generated insights for each product.

## Skills & Technologies
Languages: Python, SQL
Frameworks & Tools: PostgreSQL, Docker, Hugging Face Transformers

## Project Structure
├── app.py                     
├── importer.py                
├── nlp_insights.py   
├── schema.sql                 
├── docker-compose.yml         
├── requirements.txt           
├── index.html  
├── .env.example              
└── .gitignore               

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Food-Database.git
cd Food-Database
```

### 2. Environment Variables
Copy the example .env file:
```bash
cp .env.example .env
```
Edit .env and fill in your credentials:
```env
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=food_db
DB_HOST=db
DB_PORT=5432
```

### 3. Start PostgreSQL with Docker
```bash
docker-compose up -d
```
Verify the container is running in Docker Desktop or via:
```bash
docker ps
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Import Food Data
```bash
python importer.py
```
Fetches data from OpenFoodFacts for specified categories and countries.
Populates your PostgreSQL database with nutritional information and NLP-generated insights.

### 6. Run the Web Application
```bash
python app.py
```
