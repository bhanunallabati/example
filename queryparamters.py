import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Retrieve query parameters from the request
    name = req.params.get('name')
    age = req.params.get('age')
    
    # Check if the required parameters are provided
    if not name or not age:
        return func.HttpResponse(
            "Please provide both 'name' and 'age' query parameters.",
            status_code=400
        )
    
    # Return a message with the parameters
    return func.HttpResponse(
        f"Hello {name}, you are {age} years old.",
        status_code=200
    )
