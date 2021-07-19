from auth import authenticate
from pathlib import Path
import os

#TODO: This is the test, will be removed when implement markdown image process.
image_path = os.getcwd() + "/Aggregation of Records.png"

def upload_image(client):
  image = client.upload_from_path(image_path, None, False)
  print("Done")
  return image

if __name__ == '__main__':
  client = authenticate()
  image = upload_image(client)
  print("Image is uploaded! 😀😀😀")
  print(f"You can find image here: 🔥{image['link']}🔥")