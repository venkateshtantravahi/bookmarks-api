template = {
    "swagger": "2.0",
    "info": {
        "title": "Bookmarks API",
        "description": "API for bookmarks",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "Venkatesh Tantravahi",
            "email": "venkateshtantravahi99@gmail.com",
            "url": "www.twitter.com/deve",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0",
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"',
        }
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",  # change this endpoint based on UI
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",  # to load static files
    "swagger_ui": True,
    "specs_route": "/",
}
