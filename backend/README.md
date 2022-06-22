## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unproccessable
- 500: Internal Server Error

### Endpoints

### GET /categories

- General:
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains an object of
    id:category_string key: value pairs.
  - Sample: `curl http://127.0.0.1:5000/categories`
  ```{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  }
  ```

#### GET /questions

- General:
  - Returns a list of question objects, category object success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`

```{
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
  "current_category": 1,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
    "answer": "Escher",
    "category": 2,
    "difficulty": 1,
    "id": 16,
    "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    }
  ],
  "status": 200,
  "success": true,
  "total_questions": 10
  }

```

#### POST /questions

- General:
  - Creates a new question using the submitted question, answer, category and diffulty. Returns the list of question object with the new created question inclusive,categories, success value, total questions to update the frontend.
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"who wrote the book bag of bones?", "answer":"Stephen Kings", "category":"2", "difficulty":"2"}'`

```{
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
  "current_category": 1,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
    "answer": "Escher",
    "category": 2,
    "difficulty": 1,
    "id": 16,
    "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    }
    {
    "answer": "Stephen Kings",
    "category": 2,
    "difficulty": 2,
    "id": 17,
    "question": "who wrote the book bag of bones?"
    }
  ],
  "status": 200,
  "success": true,
  "total_questions": 10
  }

```

#### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted book, success value and http status code
- `curl -X DELETE http://127.0.0.1:5000/questions/1?page=2`

```
{
  "status": 200,
  "success": True,
  "deleted_question": 1
}
```
