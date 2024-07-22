# Data Importer System

## Overview

The Data Importer System is designed to dynamically import and manage data from CSV files and manual data entry into a PostgreSQL database using Django. It allows users to preview data, define column types, and store the data in dynamically created tables.

## Features

- Import data from CSV files.
- Manual data entry with column definition.
- Dynamic table creation based on imported data.
- Display of table columns and data.

## System Architecture

The system is built using Django with PostgreSQL as the database backend. The key components are:

1. **Models**: 
   - `ImportedData`: Stores metadata about imported data.
   
2. **Views**:
   - `index`: Main page for data import and manual entry.
   - `data_list`: Displays the columns and data of the dynamic table.
   - `data_create`: Allows creating new data entries.
   - `view_data`: Lists the imported data.

3. **Templates**:
   - `index.html`: Main page template.
   - `data_list.html`: Template for displaying table columns and data.
   - `data_form.html`: Template for creating and editing data.

## API Endpoints

1. **Main Page**: 
   - **URL**: `/`
   - **Method**: GET
   - **Description**: Displays the main page for data import and manual entry.

2. **Data List**: 
   - **URL**: `/data/list/`
   - **Method**: GET
   - **Description**: Displays the columns and data of the dynamic table.

3. **Data Create**: 
   - **URL**: `/data/create/`
   - **Method**: POST
   - **Description**: Allows creating new data entries.

4. **View Data**: 
   - **URL**: `/view_data/`
   - **Method**: GET
   - **Description**: Lists the imported data.

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup the database**:
   - Ensure PostgreSQL is installed and running.
   - Create a database and update the `DATABASES` setting in `settings.py`.

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Open your browser and go to `http://127.0.0.1:8000/`

## Notes

- This project was developed within a tight schedule of 2 days.
- Future enhancements include better error handling, advanced data validation, and extended functionalities for data manipulation.
