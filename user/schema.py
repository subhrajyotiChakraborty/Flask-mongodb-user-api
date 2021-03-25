user_register = {
    "type": "object",
    "properties": {
      "name": {"type": "string", "minLength": 2, "maxLength": 100},
      "email": {"type": "string", "format": "email"},
      "password": {"type": "string", "minLength": 5, "maxLength": 32}
    },
    "required": ["name", "email", "password"]
}

user_login = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 5, "maxLength": 32}
    },
    "required": ["email", "password"]
}