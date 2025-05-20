import requests

def download_file(url: str, local_path: str):
    try:        
        response = requests.get(url)
        with open(local_path, "wb") as file:
            file.write(response.content)
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
    
    return True
    