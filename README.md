## Project Overview

This project is a Biomedical Maintenance System designed to manage and track the maintenance of biomedical equipment. It is a web-based application built using modern web technologies.

## Features

- Equipment Management: Add, update, and delete biomedical equipment records.
- Maintenance Scheduling: Schedule and track maintenance activities.
- User Management: Manage user roles and permissions.
- Reporting: Generate reports on maintenance activities and equipment status.

## Technologies Used

- Frontend: HTML, CSS, Bootstrap
- Backend: Python, Flask
- Database: SQLite (SQLAlchemy)
- Templating: Jinja2
- Version Control: Git

## Installation

1. Clone the repository:
	```bash
	git clone https://github.com/MoMaherB/Biomedical-maintenance-system-Webstack-Portfolio-Project.git
	```
2. Navigate to the project directory:
	```bash
	cd Biomedical-maintenance-systemWebstack-Portfolio-Project
	```
3. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
	```
4. You can start the server using Python:
	```bash
	python3 run.py
	```

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Register a new account or log in with existing credentials.
3. Start managing biomedical equipment and scheduling maintenance.
4. In login page enter with these credentials as admi user: email: admin@maintenance.com password: Adminpassword.
5. Login as a regular user using these credentials: email: maher1525@gmail.com password: 5573758

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## API Usage
The application also provides a RESTful API for managing biomedical equipment and maintenance activities. The base URL for the API is `http://localhost:5000/api`.

### Endpoints
- **GET /api/users**: Retrieve a list of all users.
- **GET /api/users/{id}**: Retrieve details of a specific user.
- **POST /api/register**: Register new user.
- **POST /api/login**: Login with existing user. 
- **GET /api/departments**: Retrieve a list of all departments.
- **GET /api/departments/{id}**: Retrieve details of a specific department.
- **POST /api/departments**: Add a new department.
- **DELETE /api/departments/{id}**: Delete a specific department.
- **GET /api/departments/{department_id}/devices**: Retrieve a list of all devices in a specific department.
- **POST /api/departments/{department_id}/devices**: Add a new device to a specific department.
- **GET /api/departments/{department_id}/devices/{device_id}**: Retrieve details of a specific device in a department.
- **DELETE /api/departments/{department_id}/devices/{device_id}**: Delete a specific device in a department.
- **GET /api/hospitals**: Retrieve a list of all hospitals.
- **GET /api/hospitals/{id}**: Retrieve details of a specific hospital.

### Example Requests

#### Add new user
```bash
curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d '{"username": "UserTest", "email": "test.maher@email.com", "password": "password"}'
```

#### Login with existing user
```bash
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"email": "Mohamed@maher.com, "password": "password"}'
```

#### Get all users
```bash
curl -X GET http://localhost:5000/api/users
```

#### Get specific user
```bash
curl -X GET http://localhost:5000/api/users/{id}
```

#### Get all departments
```bash
curl -X GET http://localhost:5000/api/departments
```

#### Get specific department
```bash
curl -X GET http://localhost:5000/api/departments/{id}
```

#### Add new department
```bash
curl -X POST http://localhost:5000/api/departments -H "Content-Type: application/json" -d '{"name": "Radiology"}'
```

#### Delete specific department
```bash
curl -X DELETE http://localhost:5000/api/departments/{id}
```

#### Get all devices in a department
```bash
curl -X GET http://localhost:5000/api/departments/{department_id}/devices
```

#### Add new device to a department
```bash
curl -X POST http://localhost:5000/api/departments/{department_id}/devices -H "Content-Type: application/json" -d '{"name": "MRI Machine"}'
```

#### Get specific device in a department
```bash
curl -X GET http://localhost:5000/api/departments/{department_id}/devices/{device_id}
```

#### Delete specific device in a department
```bash
curl -X DELETE http://localhost:5000/api/departments/{department_id}/devices/{device_id}
```

#### Get all hospitals
```bash
curl -X GET http://localhost:5000/api/hospitals
```

#### Get specific hospital
```bash
curl -X GET http://localhost:5000/api/hospitals/{id}
```

## Tests
```bash
python3 -m unittest -v tests/department_test.py
python3 -m unittest -v tests/device_test.py
python3 -m unittest -v tests/user_test.py
python3 -m unittest -v tests/hospitals_test.py
```

## License

This project is licensed under the ALX scholarship.
