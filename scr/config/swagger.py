template ={
"swagger": "2.0",
"info":{
    "title":"BOOKMARKS API",
    "description":"API for tracking how many times a link is visited App by henry Onyeka",
    "contacts":{
        "name": "API Support",
        "email":"hmike54@gmail.com",
    
    "url":"https://www.linkedin.com/in/henry-onyeka-michael-0a0079a9"
       
    },
    "TermsofService":"make enquiries",
    "version":"1.2"
},
"basePath":"/api/vi", #base Path for blueprint registeration call
"schemes":[
    "http",
    "https"
],
"securityDefinitions":{
    "bearer":{
        "type":"apiKey",
        "name":"Authorization",
        "in":"header",
        "description":"JWT AUTHORIZATION using the bearer token. Example : \"Authorization: Bearer {token}\""
    }
},
}
swagger_config = {
    "headers":[

    ],
    "specs":[
        {
            "endpoint":'apispec',
            "route":'/apispec.json',
            "rule_filter": lambda rule:True,
            "model_filter":lambda tag: True
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui":True,
    "specs_route":"/"
}