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
                        "20": {
                            "description": "Ok",
                        },
                        "400": {
                            "description": "Bad request.",
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
                        "201": {
                            "description": "Success.",
                        },
                        "400": {
                            "description": "Fail."
                        },
                        "403": {
                            "description": "You dont have the rights to modify this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        }
                    }
                },

            },
            "/delegations": {
                "get": {
                    "tags": ["Delegation"],
                    "summary": "Returns list of user delegations.",
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
                        },
                    }
                },
                "post": {
                    "tags": ["Delegation"],
                    "summary": "Adds new delegation.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "e5k9ih78cEDjpqV5YQdxmf"
                        }
                    ],
                    "requestBody": {
                        "description": "Takes delegation details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Delegation"
                                },
                                "example": {
                                    "title": "some title",
                                    "country_id": 11,
                                    "approver_id": 3,
                                    "arrival_date": "2020-01-20",
                                    "delegate_id": 2,
                                    "departure_date": "2020-01-15",
                                    "reason": "some reason",
                                    "remarks": "some remarks",
                                    "advance_payments": [
                                        {
                                            "amount": 124,
                                            "currency_id": 5
                                        },
                                        {
                                            "amount": 11,
                                            "currency_id": 1
                                        }
                                    ]
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
                        "404": {
                            "description": "Fail.",
                        },
                    }
                }
            },
            "/delegations/{delegation_id}": {
                "get": {
                    "tags": ["Delegation"],
                    "summary": "Shows delegation details.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation to show.",
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
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                    }
                },
                "put": {
                    "tags": ["Delegation"],
                    "summary": "Modifies existing delegation.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation to modify.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Changes existing delegation.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Delegation"
                                },
                                "example": {
                                    "advance_payment": [
                                        {
                                            "amount": 999,
                                            "currency_id": 4,
                                            "id": 1
                                        },
                                    ],
                                    "arrival_date": "Mon, 22 Jan 2020 00:00:00 GMT",
                                    "departure_date": "Wed, 15 Jan 2020 00:00:00 GMT",
                                    "id": 1,
                                    "reason": "xxx",
                                    "title": "xxx"
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
                            "description": "You dont have the rights to modify this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        }
                    }
                },
                "delete": {
                    "tags": ["Delegation"],
                    "summary": "Deletes delegation.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "LFvxPVWyetuPyKo8ZrLm5F"
                        },
                        {
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation to delete.",
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
                            "description": "You dont have the rights to delete this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                    }
                }
            },
            "/delegations/{delegation_id}/settlements": {
                "get": {
                    "tags": ["Settlement"],
                    "summary": "Shows settlements for delegation.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "2T7y2x29rpxQJT4474RPWv"
                        },
                        {
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation to show.",
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
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
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
                        {
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation to show.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Takes settlement details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Settlement"
                                },
                                "example": {
                                    "approver_id": 6,
                                    "departure_date": "2020-01-15",
                                    "departure_time": "10:10:10",
                                    "arrival_date": "2020-01-20",
                                    "arrival_time": "20:10:10",
                                    "meals": [
                                        {
                                            'type': 'breakfast'
                                        },
                                        {
                                            "type": 'lunch'
                                        }
                                    ],
                                    "expenses": [
                                        {
                                            "type": 'transit',
                                            "amount": 111,
                                            "currency_id": 3,
                                            "description": "some description",
                                            "attachments": [
                                                {
                                                    "file": 'some path'
                                                },
                                                {
                                                    "file": 'path2'
                                                }
                                            ]
                                        },
                                        {
                                            "type": 'other',
                                            "amount": 1,
                                            "currency_id": 3,
                                            "description": "lost",
                                            "attachments": [
                                                {
                                                    "file": 'pathpath'
                                                },
                                            ]
                                        },
                                    ]
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
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Fail.",
                        },
                        "404.2": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                        "404.3": {
                            "description": 'Cannot find user with provided "approver_id".',
                        },
                    }
                },
            },
            "/delegations/{delegation_id}/settlements/{settlement_id}": {
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
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation that is a parent of settlement.",
                            "type": "int"
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
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                        "404.2": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                        "404.3": {
                            "description": "Provided settlement is not a child of provided delegation.",
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
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation that is a parent of settlement.",
                            "type": "int"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement to show.",
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
                                    "diet": 11,
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
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                        "404.2": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                        "404.3": {
                            "description": "Provided settlement is not a child of provided delegation.",
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
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation that is a parent of settlement.",
                            "type": "int"
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
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                        "404.2": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                        "404.3": {
                            "description": "Provided settlement is not a child of provided delegation.",
                        },
                    }
                }
            },
            "/delegations/{delegation_id}/settlements/{settlement_id}/expenses": {
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
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation that is a parent of settlement.",
                            "type": "int"
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
                        "403": {
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
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
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation that is a parent of settlement.",
                            "type": "int"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement to show.",
                            "type": "int"
                        }
                    ],
                    "requestBody": {
                        "description": "Takes settlement details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Expense"
                                },
                                "example": {
                                    "currency_id": 6,
                                    "type": 'accommodation',
                                    'amount': 12.21
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
                        "404": {
                            "description": "Fail.",
                        },
                    }
                },
            },
            "/delegations/{delegation_id}/settlements/{settlement_id}/expenses/{expense_id}": {
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
                            "name": "delegation_id",
                            "in": "path",
                            "description": "ID of the delegation that is a parent of settlement.",
                            "type": "int"
                        },
                        {
                            "name": "settlement_id",
                            "in": "path",
                            "description": "ID of the settlement to show.",
                            "type": "int"
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
                            "description": "You dont have the rights to see this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                        "404.2": {
                            "description": "Cannot find settlement with provided ID.",
                        },
                        "404.3": {
                            "description": "Provided settlement is not a child of provided delegation.",
                        },
                    }
                },
                # "put": {
                #     "tags": ["Expense"],
                #     "summary": "Modifies existing expense.",
                #     "parameters": [
                #         {
                #             "name": "token",
                #             "in": "header",
                #             "description": "Token of logged user.",
                #             "type": "string",
                #             "example": "2T7y2x29rpxQJT4474RPWv"
                #         },
                #         {
                #             "name": "delegation_id",
                #             "in": "path",
                #             "description": "ID of the delegation that is a parent of settlement.",
                #             "type": "int"
                #         },
                #         {
                #             "name": "settlement_id",
                #             "in": "path",
                #             "description": "ID of the settlement to show.",
                #             "type": "int"
                #         }
                #     ],
                #     "requestBody": {
                #         "description": "Changes existing settlement.",
                #         "content": {
                #             "application/json": {
                #                 "schema": {
                #                     "$ref": "#/components/schemas/Settlement"
                #                 },
                #                 "example": {
                #                     "diet": 11,
                #                 }
                #             }
                #         }
                #     },
                #     "produces": [
                #         "application/json"
                #     ],
                #     "responses": {
                #         "201": {
                #             "description": "Success.",
                #         },
                #         "400": {
                #             "description": "Fail."
                #         },
                #         "401": {
                #             "description": "You are not logged in.",
                #         },
                #         "403": {
                #             "description": "You dont have the rights to see this delegation.",
                #         },
                #         "404": {
                #             "description": "Cannot find delegation with provided ID.",
                #         },
                #         "404.2": {
                #             "description": "Cannot find settlement with provided ID.",
                #         },
                #         "404.3": {
                #             "description": "Provided settlement is not a child of provided delegation.",
                #         },
                #     }
                # },
                # "delete": {
                #     "tags": ["Expense"],
                #     "summary": "Deletes expense.",
                #     "parameters": [
                #         {
                #             "name": "token",
                #             "in": "header",
                #             "description": "Token of logged user.",
                #             "type": "string",
                #             "example": "LFvxPVWyetuPyKo8ZrLm5F"
                #         },
                #         {
                #             "name": "delegation_id",
                #             "in": "path",
                #             "description": "ID of the delegation that is a parent of settlement.",
                #             "type": "int"
                #         },
                #         {
                #             "name": "settlement_id",
                #             "in": "path",
                #             "description": "ID of the settlement to show.",
                #             "type": "int"
                #         }
                #     ],
                #     "produces": [
                #         "application/json"
                #     ],
                #     "responses": {
                #         "201": {
                #             "description": "Success.",
                #         },
                #         "400": {
                #             "description": "Fail."
                #         },
                #         "401": {
                #             "description": "You are not logged in.",
                #         },
                #         "403": {
                #             "description": "You dont have the rights to see this delegation.",
                #         },
                #         "404": {
                #             "description": "Cannot find delegation with provided ID.",
                #         },
                #         "404.2": {
                #             "description": "Cannot find settlement with provided ID.",
                #         },
                #         "404.3": {
                #             "description": "Provided settlement is not a child of provided delegation.",
                #         },
                #     }
                # }
            },
            "/dictionary/currency": {
                "get": {
                    "tags": ["Dictionary"],
                    "summary": "Shows list of currencies.",
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
                    "summary": "Shows list of countries.",
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
                        "email": {"type": "string"},
                        "password": {"type": "string"},
                        "role": {"type": "Role", "format": "string"},
                        "is_active": {"type": "boolean"},
                        "token": {"type": "string"}
                    }
                },
                "DelegationStatus": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "status": {"type": "string"},
                        "reason": {"type": "string"},
                        "delegation_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Delegation": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "status": {"type": "DelegationStatus", "format": "string"},
                        "title": {"type": "string"},
                        "submit_date": {"type": "string"},
                        "departure_date": {"type": "string"},
                        "arrival_date": {"type": "string"},
                        "reason": {"type": "string"},
                        "remarks": {"type": "string"},
                        "delegate_id": {"type": "integer", "format": "foreign key"},
                        "creator_id": {"type": "integer", "format": "foreign key"},
                        "approver_id": {"type": "integer", "format": "foreign key"},
                        "country_id": {"type": "integer", "format": "foreign key"}
                    }
                },
                "AdvancePayment": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "amount": {"type": "float"},
                        "delegation_id": {"type": "integer", "format": "foreign key"},
                        "currency_id": {"type": "integer", "format": "foreign key"},
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
                        "departure_date": {"type": "string"},
                        "departure_time": {"type": "string"},
                        "arrival_date": {"type": "string"},
                        "arrival_time": {"type": "string"},
                        "diet": {"type": "float"},
                        "delegation_id": {"type": "integer", "format": "foreign key"},
                        "approver_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Meal": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "type": {"type": "MealType", "format": "string"},
                        "settlement_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Expense": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "type": {"type": "ExpenseType", "format": "string"},
                        "amount": {"type": "float"},
                        "description": {"type": "string"},
                        "settlement_id": {"type": "integer", "format": 'foreign key'},
                        "currency_id": {"type": "integer", "format": 'foreign key'},
                    }
                },
                "Attachment": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "file": {"type": "LargeBinary"},
                        "expense_id": {"type": "integer", "format": "foreign key"},
                    }
                },
            }
        }
    }
    return details


swagger_ui_blueprint = get_swaggerui_blueprint(base_url='/swagger',
                                               api_url='/swagger_details')
