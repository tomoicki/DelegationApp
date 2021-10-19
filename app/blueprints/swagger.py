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
                        "201": {
                            "description": "OK",
                            "schema": {
                                "$ref": "#/components/schemas/User"
                            },
                        },
                    }
                }
            },
            "/delegations": {
                "get": {
                    "tags": ["User"],
                    "summary": "Returns list of user delegations.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "WuupcYvsqnLNoFGtvp64TW"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "OK",
                            "schema": {
                                "$ref": "#/components/schemas/User"
                            },
                        },
                    }
                }
            },
            "/add_delegation": {
                "post": {
                    "tags": ["Delegation"],
                    "summary": "Adds new delegation.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "WuupcYvsqnLNoFGtvp64TW"
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
                            "description": "OK",
                            "schema": {
                                "$ref": "#/components/schemas/Delegation"
                            },
                        },
                    }
                }
            },
            "/modify_delegation": {
                "get": {
                    "tags": ["Delegation"],
                    "summary": "Shows delegation details.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "WuupcYvsqnLNoFGtvp64TW"
                        },
                        {
                            "name": "id",
                            "in": "header",
                            "description": "ID of delegation.",
                            "type": "string",
                            "example": "MCZq7ugPkVNireoYPdHxBV"
                        }
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "201": {
                            "description": "OK",
                            "schema": {
                                "$ref": "#/components/schemas/User"
                            },
                        },
                    }
                },
                "put": {
                    "tags": ["Delegation"],
                    "summary": "Adds new delegation.",
                    "parameters": [
                        {
                            "name": "token",
                            "in": "header",
                            "description": "Token of logged user.",
                            "type": "string",
                            "example": "WuupcYvsqnLNoFGtvp64TW"
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
                                    "id": 'MCZq7ugPkVNireoYPdHxBV',
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
                            "description": "OK",
                            "schema": {
                                "$ref": "#/components/schemas/Delegation"
                            },
                        },
                    }
                }
            },

        },
        "components": {
            "schemas": {
                "User": {
                    "properties": {
                        "id": {"type": "string", "format": 'primary key'},
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
                        "id": {"type": "string", "format": 'primary key'},
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
                        "worker_id": {"type": "string", "format": "foreign key"},
                        "maker_id": {"type": "string", "format": "foreign key"},
                        "approved_by_id": {"type": "string", "format": "foreign key"},
                        "country_id": {"type": "string", "format": "foreign key"}
                    }
                },
                "AdvancePayment": {
                    "properties": {
                        "id": {"type": "string", "format": 'primary key'},
                        "amount": {"type": "float"},
                        "delegation_id": {"type": "string", "format": "foreign key"},
                        "currency_id": {"type": "string", "format": "foreign key"},
                    }
                },
                "Currency": {
                    "properties": {
                        "id": {"type": "string", "format": 'primary key'},
                        "name": {"type": "string"},
                    }
                },
                "Expense": {
                    "properties": {
                        "id": {"type": "string", "format": 'primary key'},
                        "type": {"type": "ExpenseType", "format": "string"},
                        "amount": {"type": "float"},
                        "description": {"type": "string"},
                        "delegation_id": {"type": "string", "format": 'foreign key'},
                        "currency_id": {"type": "string", "format": 'foreign key'},
                    }
                },
                "Country": {
                    "properties": {
                        "id": {"type": "string", "format": 'primary key'},
                        "name": {"type": "string"},
                        "currency_id": {"type": "string", "format": "foreign key"},
                    }
                },
                "Settlement": {
                    "properties": {
                        "id": {"type": "string", "format": 'primary key'},
                        "date": {"type": "string"},
                        "delegation_id": {"type": "string", "format": "foreign key"},
                        "approver_id": {"type": "string", "format": "foreign key"},
                    }
                },
                "Meal": {
                    "properties": {
                        "id": {"type": "string", "format": 'primary key'},
                        "type": {"type": "MealType", "format": "string"},
                        "delegation_id": {"type": "string", "format": "foreign key"},
                    }
                },
            }
        }
    }
    return details


swagger_ui_blueprint = get_swaggerui_blueprint(base_url='/swagger',
                                               api_url='/swagger_details')
