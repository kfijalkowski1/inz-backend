from datetime import datetime

from code.database.declarations.users_roles import Roles
from code.database.declarations.worker import Department

mock_db = {
  "estate": [
      {
          "id": 1,
          "name": "Test Estate",
          "description": "Test Estate Description"
      },
      {
          "id": 2,
          "name": "Test Estate 2",
          "description": "Test Estate Description 2"
      }
  ],
  "users": [
      {
          "id": 1,
          "name": "Kevin",
          "surname": "Scott",
          "username": "kevin",
          "hashed_password": "hashed_password"
      },
      {
          "id": 2,
          "name": "Dwight",
          "surname": "Schrute",
          "username": "dwight",
          "hashed_password": "hashed_password"
      },
      {
          "id": 3,
          "name": "Jim",
          "username": "jim",
          "hashed_password": "hashed_password"
      },
      {
          "id": 4,
          "name": "Admin",
          "username": "admin",
          "hashed_password": "hashed_password"
      },
      {
          "id": 5,
          "name": "Worker",
          "username": "worker_1",
          "hashed_password": "hashed_password"
      },
      {
          "id": 6,
          "name": "Worker",
          "username": "worker_2",
          "hashed_password": "hashed_password"
      },
      {
          "id": 7,
          "name": "Michael",
          "surname": "Scott",
          "username": "worker_3",
          "hashed_password": "hashed_password"
      }
  ],
    "users_roles": [
        {
            "id": 1,
            "user_id": 1,
            "role": Roles.USER,
            "estate_id": 1
        },
        {
            "id": 2,
            "user_id": 2,
            "role": Roles.USER,
            "estate_id": 1
        },
        {
            "id": 3,
            "user_id": 3,
            "role": Roles.USER,
            "estate_id": 2
        },
        {
            "id": 4,
            "user_id": 4,
            "role": Roles.ADMIN,
            "estate_id": 1
        },
        {
            "id": 5,
            "user_id": 5,
            "role": Roles.WORKER,
            "estate_id": 1
        },
        {
            "id": 6,
            "user_id": 6,
            "role": Roles.WORKER,
            "estate_id": 2
        },
        {
            "id": 7,
            "user_id": 7,
            "role": Roles.WORKER,
            "estate_id": 1
        }
    ],
    "worker": [
        {
            "id": 3,
            "user_id": 7,
            "type": Department.OTHER,
            "is_manager": True
        },
        {
            "id": 1,
            "user_id": 5,
            "type": Department.CLEANING,
            "manager_id": "7",
        },
        {
            "id": 2,
            "user_id": 6,
            "type": Department.CLEANING
        }
    ],
  "posts": [
          {
              "id": 1,
              "title": "Test Post",
              "description": "Test Post Description",
              "author_id": 1,
              "created_at": datetime.now()
          },
          {
              "id": 2,
              "title": "Test Post 2",
              "description": "Test Post Description 2",
              "author_id": 2,
              "created_at": datetime.now()
          },
        {
            "id": 3,
            "title": "Test Post 3",
            "description": "Test Post Description 3",
            "author_id": 3,
            "created_at": datetime.now()
        }
  ],
    "requests": [
        {
            "id": 1,
            "author_id": 1,
            "title": "Test Request",
            "description": "Test Request Description",
            "start_time": datetime.now()
        },
        {
            "id": 2,
            "author_id": 2,
            "title": "Test Request 2",
            "description": "Test Request Description 2",
            "start_time": datetime.now()
        },
        {
            "id": 3,
            "author_id": 3,
            "title": "Test Request 3",
            "description": "Test Request Description 3",
            "start_time": datetime.now()
        }
    ],
    "request_comments": [
        {
            "id": 1,
            "content": "Test Comment",
            "author_id": 1,
            "created_at": datetime.now(),
            "request_id": 1
        },
        {
            "id": 2,
            "content": "Test Comment Admin",
            "author_id": 4,
            "created_at": datetime.now(),
            "request_id": 2
        },
        {
            "id": 3,
            "content": "Test Comment Worker",
            "author_id": 5,
            "created_at": datetime.now(),
            "request_id": 3
        }
    ]

}