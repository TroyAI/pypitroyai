import requests
import json
import pickle
import string

from typing import Any

from error_helpers import (
    token_error,
    name_error,
    description_error,
    score_error,
    hostname_error,
)

def upload_model(model: Any, *, token: str, name: str=None, 
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