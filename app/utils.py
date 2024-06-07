import requests
import logging
from app.config import Config  # Adjust the import path if necessary

logger = logging.getLogger(__name__)

def get_ollama_response(message, agent="default"):
    url = Config.OLLAMA_URL
    data = {
        "model": Config.OLLAMA_MODEL,
        "prompt": f"[{agent}]: {message}",
        "stream": False
    }

    logger.debug(f"Sending request to Ollama API with data: {data}")
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(f"Ollama response: {response_json}")
        return response_json.get("response")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return f"Error: HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        return f"Error: Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return f"Error: Timeout error occurred: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return f"Error: Request error occurred: {req_err}"
    except ValueError as json_err:
        logger.error(f"JSON decode error: {json_err}")
        return f"Error: JSON decode error: {json_err}"

def player_interaction_agent(user_message):
    logger.debug(f"Interacting with player message: {user_message}")
    overseer_response = get_ollama_response(user_message, agent="RPG-Master-Overseer")
    if 'Error:' in overseer_response:
        logger.error(f"Error received from overseer response: {overseer_response}")
    else:
        logger.debug(f"Overseer response received: {overseer_response}")

    story_update = get_ollama_response("Generate story update based on latest events", agent="Story Teller")
    if 'Error:' in story_update:
        logger.error(f"Error received from story update response: {story_update}")
    else:
        logger.debug(f"Story update response received: {story_update}")
    
    return overseer_response, story_update
