"""top docstring"""

def getstringsentiment(app, sent_api_data, textstring):
    """get sentiment data of a string"""
    import requests
    request_headers = {
        "X-Mashape-Key": sent_api_data["X-Mashape-Key"],
        "Content-Type": sent_api_data["Content-Type"],
        "Accept": sent_api_data["Accept"]
    }
    request_data = {
        "language": sent_api_data["language"],
        "text": textstring
    }
    request = requests.post("https://japerk-text-processing.p.mashape.com/sentiment/",
                            headers=request_headers, data=request_data)
    return request.json()
