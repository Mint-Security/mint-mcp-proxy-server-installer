import zipfile

def decrypt_zip(zip_path: str, save_to: str ,key: str):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(path=save_to, pwd=key.encode('utf-8'))
    except Exception as e:
        print(f"Error decrypting zip file: {e}")
        raise e
