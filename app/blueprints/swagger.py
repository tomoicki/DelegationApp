from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

swagger_details = Blueprint('swagger_details', __name__)


@swagger_details.route('/swagger_details')
def swagger_details_provider():
    details = {
        "openapi": "3.0.0",
        "info": {
            "version": "1.0.0",
            "title": "DelegationApp API"},
        "servers": [
            {
                "url": "/"
            }
        ],
        "paths": {
            "/register": {
                "post": {
                    "tags": ["User"],
                    "summary": "Creates new user.",
                    "requestBody": {
                        "description": "Takes new user details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
                                },
                                "example": {
                                    'first_name': 'First',
                                    'last_name': 'User',
                                    "email": "maker@gmail.com",
                                    "password": "right",
                                    'retype_password': 'right',
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "401": {
                            "description": "Passwords do not match.",
                        },
                        "409": {
                            "description": "User with provided email already registered.",
                        },
                    }
                }
            },
            "/login": {
                "post": {
                    "tags": ["User"],
                    "summary": "Returns users token",
                    "requestBody": {
                        "description": "takes user email and password",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
                                },
                                "example": {
                                    "email": "maker@gmail.com",
                                    "password": "right"
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "Ok",
                        },
                        "400": {
                            "description": "Bad request.",
                        },
                        "401": {
                            "description": "Bad password.",
                        },
                        "403": {
                            "description": "Cannot find user with provided email.",
                        },
                    }
                },
            },
            "/user": {
                "get": {
                    "tags": ["User"],
                    "summary": "Returns user details..",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "ieZJQPebstKXutENPiQNmh"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        }
                    }
                },
                "put": {
                    "tags": ["User"],
                    "summary": "Modifies existing user.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        }
                    ],
                    "requestBody": {
                        "description": "Changes existing user.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
                                },
                                "example": {
                                    "first_name": "changed name",
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK.",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                    }
                },
            },
            "/settlements": {
                "get": {
                    "tags": ["Settlement"],
                    "summary": "Shows settlements for user.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                    }
                },
                "post": {
                    "tags": ["Settlement"],
                    "summary": "Adds new settlement.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "e5k9ih78cEDjpqV5YQdxmf"
                        },
                    ],
                    "requestBody": {
                        "description": "Takes settlement details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Settlement"
                                },
                                "example": {
                                    "title": "some title",
                                    "delegate_id": 2,
                                    "country_id": 11,
                                    "approver_id": 3,
                                    "arrival_date": "2020-01-20",
                                    "departure_time": "10:10:10",
                                    "arrival_time": "20:10:10",
                                    "departure_date": "2020-01-15",
                                    "reason": "some reason",
                                    "remarks": "some remarks",
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to create this settlement.",
                        },
                        "404": {
                            "description": "Fail.",
                        },
                        "404.2": {
                            "description": 'Cannot find user with provided approver_id.',
                        },
                    }
                },
            },
            "/settlements/{settlement_id}": {
                "get": {
                    "tags": ["Settlement"],
                    "summary": "Shows settlement details.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement to show.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this settlement.",
                        },
                        "404": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                },
                "put": {
                    "tags": ["Settlement"],
                    "summary": "Modifies existing settlement.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement to modify.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Changes existing settlement.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Settlement"
                                },
                                "example": {
                                    "arrival_time": "20:10:10",
                                    "departure_time": "10:10:10",
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to modify this settlement.",
                        },
                        "404": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                },
                "delete": {
                    "tags": ["Settlement"],
                    "summary": "Deletes settlement.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "LFvxPVWyetuPyKo8ZrLm5F"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement to delete.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to delete this settlement.",
                        },
                        "404": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                }
            },
            "/settlements/{settlement_id}/advance_payments": {
                "get": {
                    "tags": ["Advance payment"],
                    "summary": "Shows advance payments for settlement.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement - parent of advance payments.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this advance payment list.",
                        },
                        "404": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                },
                "post": {
                    "tags": ["Advance payment"],
                    "summary": "Adds new advance payment.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "e5k9ih78cEDjpqV5YQdxmf"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement - parent of advance payment to add.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Takes advance payment details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AdvancePayment"
                                },
                                "example": [
                                    {
                                        "amount": 66,
                                        "currency_id": 11,
                                    },
                                    {
                                        "amount": 0,
                                        "currency_id": 1,
                                    }
                                ]
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to create this delegation.",
                        },
                        "404": {
                            "description": "Fail.",
                        },
                        "404.2": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                },
            },
            "/advance_payments/{advance_payment_id}": {
                "get": {
                    "tags": ["Advance payment"],
                    "summary": "Shows advance payment details.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "advance_payment_id",
                            "in": "path",
                            "description": "ID of the advance payment to show.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to delete this advance payment.",
                        },
                        "404": {
                            "description": "Cannot find advance payment with provided ID.",
                        },
                    }
                },
                "put": {
                    "tags": ["Advance payment"],
                    "summary": "Modifies existing advance payment.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "advance_payment_id",
                            "in": "path",
                            "description": "ID of the advance payment to modify.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Changes existing advance payment.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AdvancePayment"
                                },
                                "example": {
                                    "amount": 0,
                                    "currency_id": 1,
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to delete this advance payment.",
                        },
                        "404": {
                            "description": "Cannot find advance payment with provided ID.",
                        },
                    }
                },
                "delete": {
                    "tags": ["Advance payment"],
                    "summary": "Deletes advance payment.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "LFvxPVWyetuPyKo8ZrLm5F"
                        },
                        {
                            "name": "advance_payment_id",
                            "in": "path",
                            "description": "ID of the advance payment to delete.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to delete this advance payment.",
                        },
                        "404": {
                            "description": "Cannot find advance payment with provided ID.",
                        },
                    }
                }
            },
            "/settlements/{settlement_id}/meals": {
                "get": {
                    "tags": ["Meal"],
                    "summary": "Shows meals for settlement.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement - parent of meals.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "403": {
                            "description": "You dont have the rights to see this meals.",
                        },
                        "404": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                },
                "post": {
                    "tags": ["Meal"],
                    "summary": "Adds new meal.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "e5k9ih78cEDjpqV5YQdxmf"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement - parent of the meal to add.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Takes meal details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Meal"
                                },
                                "example": [
                                    {
                                        "type": "lunch"
                                    },
                                    {
                                        "type": "supper"
                                    },
                                ]
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "403": {
                            "description": "You dont have the rights to add this meal.",
                        },
                        "404": {
                            "description": "Fail.",
                        },
                        "404.2": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                },
            },
            "/meals/{meal_id}": {
                "get": {
                    "tags": ["Meal"],
                    "summary": "Shows meal details.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "meal_id",
                            "in": "path",
                            "description": "ID of the meal to show.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this meal.",
                        },
                        "404": {
                            "description": "Cannot find meal with provided ID.",
                        },
                    }
                },
                "put": {
                    "tags": ["Meal"],
                    "summary": "Modifies existing meal.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "meal_id",
                            "in": "path",
                            "description": "ID of the meal to modify.",
                            "type": "int"
                        },
                    ],
                    "requestBody": {
                        "description": "Changes existing meal.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Meal"
                                },
                                "example": {
                                    "type": "supper",
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to modify this meal.",
                        },
                        "404": {
                            "description": "Cannot find meal with provided ID.",
                        },
                    }
                },
                "delete": {
                    "tags": ["Meal"],
                    "summary": "Deletes meal.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "LFvxPVWyetuPyKo8ZrLm5F"
                        },
                        {
                            "name": "meal_id",
                            "in": "path",
                            "description": "ID of the meal to delete.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to delete this meal.",
                        },
                        "404": {
                            "description": "Cannot find meal with provided ID.",
                        },
                    }
                }
            },
            "/settlements/{settlement_id}/expenses": {
                "get": {
                    "tags": ["Expense"],
                    "summary": "Shows expenses for settlement.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement - parent of expenses.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this expenses.",
                        },
                        "404": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                    }
                },
                "post": {
                    "tags": ["Expense"],
                    "summary": "Adds new expense.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "e5k9ih78cEDjpqV5YQdxmf"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement - parent of the expense to add.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Takes expense details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Expense"
                                },
                                "example": [
                                    {
                                        "currency_id": 6,
                                        "type": 'accommodation',
                                        'amount': 12.21
                                    },
                                    {
                                        "currency_id": 1,
                                        "type": 'drive',
                                        'amount': 1
                                    }
                                ]
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to add this expenses.",
                        },
                        "404": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                        "404.2": {
                            "description": "Fail.",
                        },
                    }
                },
            },
            "/expenses/{expense_id}": {
                "get": {
                    "tags": ["Expense"],
                    "summary": "Shows expense details.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "expense_id",
                            "in": "path",
                            "description": "ID of the expense to show.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this expense.",
                        },
                        "404": {
                            "description": "Cannot find expense with provided ID.",
                        },
                    }
                },
                "put": {
                    "tags": ["Expense"],
                    "summary": "Modifies existing expense.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "expense_id",
                            "in": "path",
                            "description": "ID of the expense to modify.",
                            "type": "int"
                        },
                    ],
                    "requestBody": {
                        "description": "Changes existing expense.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Expense"
                                },
                                "example": {
                                    "reason": "some info added",
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to modify this expense.",
                        },
                        "404": {
                            "description": "Cannot find expense with provided ID.",
                        },
                    }
                },
                "delete": {
                    "tags": ["Expense"],
                    "summary": "Deletes expense.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "LFvxPVWyetuPyKo8ZrLm5F"
                        },
                        {
                            "name": "expense_id",
                            "in": "path",
                            "description": "ID of the expense to delete.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to delete this expense.",
                        },
                        "404": {
                            "description": "Cannot find expense with provided ID.",
                        },
                    }
                }
            },
            "/expenses/{expense_id}/attachments": {
                "get": {
                    "tags": ["Attachment"],
                    "summary": "Shows attachments for expense.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "expense_id",
                            "in": "path",
                            "description": "ID of the expense - parent of attachments.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this attachments.",
                        },
                        "404": {
                            "description": "Cannot find expense with provided ID.",
                        },
                    }
                },
                "post": {
                    "tags": ["Attachment"],
                    "summary": "Adds new attachment.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "e5k9ih78cEDjpqV5YQdxmf"
                        },
                        {
                            "name": "expense_id",
                            "in": "path",
                            "description": "ID of the expense to create attachment for.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Takes attachment details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Attachment"
                                },
                                "example": [
                                    {
                                        "file": 'c://windows/sys32.exe'
                                    },
                                    {
                                        "file": '...'
                                    }
                                ]
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to create this attachments.",
                        },
                        "404": {
                            "description": "Cannot find expense with provided ID.",
                        },
                        "404.2": {
                            "description": "Fail.",
                        },
                    }
                },
            },
            "/attachments/{attachment_id}": {
                "get": {
                    "tags": ["Attachment"],
                    "summary": "Shows attachment details.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "attachment_id",
                            "in": "path",
                            "description": "ID of the attachment to show.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this attachment.",
                        },
                        "404": {
                            "description": "Cannot find attachment with provided ID.",
                        },
                    }
                },
                "put": {
                    "tags": ["Attachment"],
                    "summary": "Modifies existing attachment.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "attachment_id",
                            "in": "path",
                            "description": "ID of the attachment to modify.",
                            "type": "int"
                        },
                    ],
                    "requestBody": {
                        "description": "Changes existing attachment.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Attachment"
                                },
                                "example": {
                                    "file": "new/path",
                                }
                            }
                        }
                    },
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this attachment.",
                        },
                        "404": {
                            "description": "Cannot find attachment with provided ID.",
                        },
                    }
                },
                "delete": {
                    "tags": ["Attachment"],
                    "summary": "Deletes attachment.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "LFvxPVWyetuPyKo8ZrLm5F"
                        },
                        {
                            "name": "attachment_id",
                            "in": "path",
                            "description": "ID of the attachment to delete.",
                            "type": "int"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "401": {
                            "description": "You are not logged in.",
                        },
                        "403": {
                            "description": "You dont have the rights to see this attachment.",
                        },
                        "404": {
                            "description": "Cannot find attachment with provided ID.",
                        },
                    }
                }
            },
            "/dictionary/currency": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of currencies.",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
            "/dictionary/expense_types": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of available expense types.",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
            "/dictionary/user_roles": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of available user roles.",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
            "/dictionary/meal_types": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of available meal types.",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
            "/dictionary/settlement_status_options": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of available settlement status options.",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
            "/dictionary/countries": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of countries.",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
            "/dictionary/users": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of all users with their id as key.",
                    "parameters": [
                        {
                            "name": "search",
                            "in": "query",
                            "description": "Letters to filter by.",
                            "type": "string",
                            "example": "xx"
                        },
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
            "/dictionary/managers": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows dictionary of all privileged users with their id as key.",
                    "parameters": [
                        {
                            "name": "search",
                            "in": "query",
                            "description": "Letters to filter by.",
                            "type": "string",
                            "example": "xx"
                        },
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                        },
                    }
                },
            },
        },
        "components": {
            "schemas": {
                "User": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string", "nullable": 'false'},
                        "password": {"type": "string", "nullable": 'false'},
                        "role": {"type": "Role", "format": "dictionary/user_roles", "nullable": 'false'},
                        "is_active": {"type": "boolean"},
                        "token": {"type": "string"}
                    }
                },
                "AdvancePayment": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "amount": {"type": "float", "nullable": 'false'},
                        "settlement_id": {"type": "integer", "format": "foreign key", "nullable": 'false'},
                        "currency_id": {"type": "integer", "format": "dictionary/currency", "nullable": 'false'},
                    }
                },
                "Country": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "name": {"type": "string"},
                        "currency_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Currency": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "name": {"type": "string"},
                    }
                },
                "SettlementStatus": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "status": {"type": "string"},
                        "reason": {"type": "string"},
                        "settlement_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Settlement": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "submit_date": {"type": "string"},
                        "departure_date": {"type": "string", "nullable": 'false'},
                        "departure_time": {"type": "string", "nullable": 'false'},
                        "arrival_date": {"type": "string", "nullable": 'false'},
                        "arrival_time": {"type": "string", "nullable": 'false'},
                        "reason": {"type": "string"},
                        "remarks": {"type": "string"},
                        "delegate_id": {"type": "integer", "format": "dictionary/users", "nullable": 'false'},
                        "creator_id": {"type": "integer", "format": "dictionary/users", "nullable": 'false'},
                        "approver_id": {"type": "integer", "format": "dictionary/managers", "nullable": 'false'},
                        "country_id": {"type": "integer", "format": "dictionary/countries", "nullable": 'false'}
                    }
                },
                "Meal": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "type": {"type": "MealType", "format": "dictionary/meal_types", "nullable": 'false'},
                        "settlement_id": {"type": "integer", "format": "foreign key", "nullable": 'false'},
                    }
                },
                "Expense": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "type": {"type": "ExpenseType", "format": "dictionary/expense_types", "nullable": 'false'},
                        "amount": {"type": "float", "nullable": 'false'},
                        "description": {"type": "string"},
                        "settlement_id": {"type": "integer", "format": 'foreign key', "nullable": 'false'},
                        "currency_id": {"type": "integer", "format": 'dictionary/currency', "nullable": 'false'},
                    }
                },
                "Attachment": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "file": {"type": "string", "nullable": 'false'},
                        "expense_id": {"type": "integer", "format": "foreign key", "nullable": 'false'},
                    }
                },
            }
        }
    }
    return details


swagger_ui_blueprint = get_swaggerui_blueprint(base_url='/swagger',
                                               api_url='/swagger_details')
