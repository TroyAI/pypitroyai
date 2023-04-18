import requests
import json
import pickle
import string

from typing import Any

DEFAULT_HOST = "http://127.0.0.1:3000"
CREATE_AUTO_PATH = "/ai_models/create_auto"

TOKEN_LENGTH = 16
BASE62 = string.ascii_letters + string.digits

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 30

DESCRIPTION_MIN_LENGTH = 5
DESCRIPTION_MAX_LENGTH = 400

# ----------------------- error detection helper functions -----------------------

def token_error(token: str) -> bool:
    if len(token) != 16 or any(character not in BASE62 for character in token):
        print(f"Error: invalid token {token!r}")
        print(f"Token should be 16 characters (not {len(token)}) and every character should be in this set:")
        print(BASE62 + '\n')
        return True
    return False

def name_error(name: str) -> bool:
    if name is None:
        print("Warning: name is None\n")
        return False
    if not NAME_MIN_LENGTH <= len(name) <= NAME_MAX_LENGTH:
        print(f"Error: name {name!r} of bad length {len(name)}")
        print(f"Minimum is {NAME_MIN_LENGTH} and maximum is {NAME_MAX_LENGTH}\n")
        return True
    return False

def description_error(description: str) -> bool:
    if description is None:
        print("Warning: description is None\n")
        return False
    if not DESCRIPTION_MIN_LENGTH <= len(description) <= DESCRIPTION_MAX_LENGTH:
        print(f"Error: description {description!r} of bad length {len(description)}")
        print(f"Minimum is {DESCRIPTION_MIN_LENGTH} and maximum is {DESCRIPTION_MAX_LENGTH}\n")
        return True
    return False

def score_error(score: float) -> bool:
    if not 0 <= score <= 1:
        print("Invalid score! (nice try)")
        print(f"Score {score!r} not between 0 and 1\n")
        return True
    return False

def hostname_error(hostname: str) -> bool:
    if not hostname.startswith("http"):
        print("Error: bad hostname {hostname!r} does not start with 'http'")
        print(f"Did you mean: {'https://' + hostname!r}\n")
        return True
    if hostname.endswith("/"):
        print("Error: bad hostname {hostname!r} ends with '/'")
        print(f"Did you mean: {hostname.removeprefix('/')!r}\n")
        return True
    return False

# ----------------------- real function -----------------------

def upload_model(model: Any, /, *, token: str, name: str=None, 
                description: str=None, score: float=None, hostname: str=None) -> None:
    if hostname is None:
        print("Warning: No hostname provided!")
        print(f"Defaulting to {DEFAULT_HOST!r} -- explicitly specify this host to silence this warning.\n")
        hostname = DEFAULT_HOST
    
    errors = [
        token_error(token),
        name_error(name),
        description_error(description),
        score_error(score),
        hostname_error(hostname),
    ]
    
    if any(errors):
        print("Aborting")
        return
    
    upload_files = dict(
        upload_file=pickle.dumps(model),
        json=json.dumps(
            dict(
                ai_model=dict(
                    name=name,
                    description=description,
                    score=score,
                ),
                token=token,
            )
        ),
    )
    
    request = requests.post(hostname + CREATE_AUTO_PATH, files=upload_files)
    response = request.content.decode('utf-8')
    
    if response.startswith("ERR"):
        print(f"Error: Server failed to save your model!")
    if request.status_code != 200:
        print(f"Error: Server responded with code {reponse.status_code}")
    print(f"Response: {response!r}, code: {request.status_code}")