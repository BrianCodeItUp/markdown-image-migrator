
from pathlib import Path
import os
from auth import authenticate 
from get_markdown_list import get_markdown_list
from process_markdown_image import process_markdown_image

def main (vault_path, attachment_folder_name):
  markdown_list = get_markdown_list(vault_path)
  attachment_path = f"{vault_path}/{attachment_folder_name}"
  # authentication
  imgur_client = authenticate()
  for md_path in markdown_list:  
    with open(md_path) as md:
      content = md.readlines()
      image_path_list = process_markdown_image(content, attachment_path)
      
      for image in image_path_list:
        img_path = image["img_path"]
        
        # upload images
        new_image = imgur_client.upload_from_path(img_path, None, False)
        image_name = os.path.basename(img_path)
        print(f"{image_name} is uploaded Successfully! 😀😀😀, You can find image here: 🔥{new_image['link']}🔥")

        # swap image url
        line_index = image["line_index"]
        link = new_image["link"]
        new_image_markdown = f'![imgur]({link})'
        content[line_index] = new_image_markdown
        
      # create new folder
      new_note_folder = os.getcwd() + "/new notes"
      if os.path.isdir(new_note_folder) == False:
        os.mkdir(new_note_folder)
        print('New notes folder created successfully')

      # write new notes to new folder
      filename = os.path.basename(md_path)
      new_note_path = f'{new_note_folder}/{filename}'
      with open(new_note_path, 'w') as notes_folder:
        new_content = "".join(content)
        notes_folder.write(new_content)
        print(f'New note {filename} created...')
      
      print(f'Great! All images migrated to Imgur. \n Check out your new note at {new_note_folder}')

if __name__ == '__main__':
  vault_path = Path.home().joinpath('.development', 'code_test', 'markdown_img_migration_test')  
  attachment_folder_name = 'attachments'
  main(vault_path, attachment_folder_name)

  
