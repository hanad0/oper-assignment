# Engineering Assessment

Starter project to use for the engineering assessment exercise

## Requirements
- Docker
- docker compose

## Getting started
Build the docker container and run the container for the first time
```docker compose up```

Rebuild the container after adding any new packages
``` docker compose up --build```

The run command script creates a super-user with username & password picked from `.env` file

## Start a Bash shell inside the container
```docker exec -it quiz-backend bash```

## Initial data
Run this command from inside the container
```python manage.py load_initial_data```

## Swagger and OpenAPI
Swagger and OpenAPI schema are hosted on http://localhost:8000/swagger/ and http://localhost:8000/schema/ respectively

## Django Admin
Django Admin is hosted on http://localhost:8000/admin/

## MailDev
MailDev is hosted on http://localhost:1080/

## Tests
Run this command from inside the container
```python manage.py test```

## Authentication
SessionAuthentication is used so browser-based clients can use it.

Initial Quiz Creator creds:
- username: creator
- password: Oper1234

Initial Quiz Participant creds:
- username: participant
- password: Oper1234


## API

- Quiz Creator can create quizzes, list quizzes (with filtering, searching, ordering and pagination), retrieve quiz details (question and answers), delete and update quizzes
- Quiz Creator can perform CRUD for questions and answers
- Quiz Creator can list participants
- Quiz Creator can send invite mails to participants for a specific quiz
- Quiz Creator can list all quiz attempts for a single quiz and view details for a specific quiz attempt


- Quiz Participant can accept a quiz invite
- Quiz Participant can view a list of quizzes to which he has been invited and the status for each of them
- Quiz Participant can view a list of questions and answers for each quiz
- Quiz Participant can submit his answers in an attempt to pass a quiz