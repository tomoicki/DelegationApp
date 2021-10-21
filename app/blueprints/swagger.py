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
                }
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
                        }
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
                                    "title": "some_title"
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
                                    "id": '1',
                                    "title": "new_title",
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
                            "name": "delegation id",
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
                        "403": {
                            "description": "You dont have the rights to delete this delegation.",
                        },
                        "404": {
                            "description": "Cannot find delegation with provided ID.",
                        },
                    }
                }
            },
            "/countries": {
                "get": {
                    "tags": ["Countries"],
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
                "Delegation": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "status": {"type": "DelegationStatus", "format": "string"},
                        "title": {"type": "string"},
                        "submit_date": {"type": "string"},
                        "departure_date": {"type": "string"},
                        "departure_time": {"type": "Role", "format": "string"},
                        "arrival_date": {"type": "boolean"},
                        "arrival_time": {"type": "string"},
                        "reason": {"type": "string"},
                        "remarks": {"type": "string"},
                        "diet": {"type": "float"},
                        "worker_id": {"type": "integer", "format": "foreign key"},
                        "maker_id": {"type": "integer", "format": "foreign key"},
                        "approved_by_id": {"type": "integer", "format": "foreign key"},
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
                "Currency": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "name": {"type": "string"},
                    }
                },
                "Expense": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "type": {"type": "ExpenseType", "format": "string"},
                        "amount": {"type": "float"},
                        "description": {"type": "string"},
                        "delegation_id": {"type": "integer", "format": 'foreign key'},
                        "currency_id": {"type": "integer", "format": 'foreign key'},
                    }
                },
                "Country": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "name": {"type": "string"},
                        "currency_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Settlement": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "date": {"type": "string"},
                        "delegation_id": {"type": "integer", "format": "foreign key"},
                        "approver_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Meal": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "type": {"type": "MealType", "format": "string"},
                        "delegation_id": {"type": "integer", "format": "foreign key"},
                    }
                },
                "Attachment": {
                    "properties": {
                        "id": {"type": "integer", "format": 'primary key'},
                        "file": {"type": "LargeBinary"},
                        "settlement_id": {"type": "integer", "format": "foreign key"},
                    }
                },
            }
        }
    }
    return details


swagger_ui_blueprint = get_swaggerui_blueprint(base_url='/swagger',
                                               api_url='/swagger_details')
