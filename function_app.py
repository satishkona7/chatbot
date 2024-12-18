import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Improved chatbot response function
def get_chatbot_response(user_input: str) -> dict:
    """Returns a structured chatbot response."""
    responses = {
        "hello": {"message": "Hi there! How can I assist you today?", "type": "greeting"},
        "how are you?": {"message": "I'm just a bot, but I'm doing fine, thank you!", "type": "response"},
        "bye": {"message": "Goodbye! Have a great day.", "type": "farewell"},
        "default": {"message": "Sorry, I didn't understand that. Can you ask something else?", "type": "error"}
    }

    # Normalize input and fetch appropriate response
    user_input = user_input.strip().lower()
    response = responses.get(user_input, responses["default"])

    return response

@app.route(route="chatbot")
def chatbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Chatbot function processed a request.')

    # Get user input from the query string or request body
    user_input = req.params.get('message')

    if not user_input:
        try:
            req_body = req.get_json()
            user_input = req_body.get('message')
        except ValueError:
            logging.error('Invalid JSON payload received.')
            return func.HttpResponse(
                json.dumps({"error": "Invalid input. Please send a valid JSON payload."}),
                status_code=400,
                mimetype="application/json"
            )
    
    # Validate user input
    if not user_input or len(user_input.strip()) == 0:
        logging.warning('Received empty user input.')
        return func.HttpResponse(
            json.dumps({"error": "Please provide a message in the query string or request body."}),
            status_code=400,
            mimetype="application/json"
        )

    # Get chatbot response
    response = get_chatbot_response(user_input)

    # Log the response (for debugging purposes)
    logging.info(f"Response sent: {response['message']}")

    # Return chatbot response as JSON
    return func.HttpResponse(
        json.dumps(response),
        status_code=200,
        mimetype="application/json"
    )
