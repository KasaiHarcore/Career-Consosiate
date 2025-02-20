# Career-Consosiate
### AI-Powered Resume Screening for Human Resources

Career-Consosiate is web-like AI-driven application designed to assist human resource professionals in screening resumes efficiently.

# Installation & Setup
Follow the steps below to install and run the application:
### 1. Prerequisites
- **Tesseract** OCR (for optical character recognition"
  - Download: [Tesseract](https://github.com/tesseract-ocr/tesseract)
- **Poppler** (for processing PDF files
  - Download: [Poppler for Windoes](https://github.com/oschwartz10612/poppler-windows)

After installation, place the installed files in the `./app/utils` directory.

### 2. Install Required Dependencies
Run the following command to install all necessary Python packages:
```
pip install -r requirements.txt
```

### 3. Database Setup
Navigate to the `app` folder and initialize the database:
```
python manage.py makemigrations
python manage.py migrate
```

4. Run the Application
Start the development server using:
```
python manage.py runserver
```
The application will be available at http://127.0.0.1:8000/
