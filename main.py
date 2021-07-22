
from pathlib import Path
import os
import sys
from auth import authenticate 
from get_markdown_list import get_markdown_list
from process_markdown_image import process_markdown_image
from terminal_color import print_header, print_green, print_fail, print_blue, print_warning
from  write_new_content import write_new_content
import imgurpython


def print_updated_files(updated_files):
  for fiename in updated_files:
      print_blue(f'{fiename} have been updated')

def main (vault_path, attachment_folder_name):
  markdown_list = get_markdown_list(vault_path)
  attachment_path = f"{vault_path}/{attachment_folder_name}"
  # authentication
  imgur_client = authenticate()
  updated_files = []
  for md_path in markdown_list:  
    with open(md_path, 'r') as md:
      md_name = os.path.basename(md_path)
      print_header(f'processing markdown: {md_name} ...')
      content = md.readlines()
      image_path_list = process_markdown_image(content, attachment_path)
      
      for image in image_path_list:
        
        img_path = image["img_path"]
        
        print_blue(f'uploading image to Imgur of image path: {img_path}')
        # upload images
        try:
          new_image = imgur_client.upload_from_path(img_path, None, False)
          image_name = os.path.basename(img_path)
          print_green(f"{image_name} is uploaded Successfully! 😀😀😀, You can find image here: 🔥{new_image['link']}🔥")

          # swap image url
          line_index = image["line_index"]
          link = new_image["link"]
          new_image_markdown = f'![imgur]({link})'
          content[line_index] = new_image_markdown
        except imgurpython.helpers.error.ImgurClientRateLimitError:
          print_fail(f"Imgur Rate limit error: {sys.exc_info()[0]}")
          print_warning("This error occur due to Imgur have limit on the amount of images  you can upload within 1 hour. \n You can try again later 😀 ")
          # write new content to the note
          write_new_content(md_path, md_name, content)
          updated_files.append(md_name)
          print_updated_files(updated_files)
          raise
        except:
          print_fail(f"Unexpected error: {sys.exc_info()[0]}")
          # write new content to the note
          write_new_content(md_path, md_name, content)
          updated_files.append(md_name)
          print_updated_files(updated_files)
          raise
    
      # write new content to the note
      is_the_markdown_processed = len(image_path_list) > 0
      if is_the_markdown_processed == False:
        print_header(f"{md_name} doesn't contain any image")
      if is_the_markdown_processed:
        write_new_content(md_path, md_name, content)
        updated_files.append(md_name)

  print_updated_files(updated_files)
  print_green(f'Done! All images migrated to Imgur.')

if __name__ == '__main__':
  # vault_path = Path.home().joinpath('.development', 'code_test', 'markdown_img_migration_test')
  vault_path = Path.home().joinpath('Documents', 'valut')  
  attachment_folder_name = 'attachments'
  main(vault_path, attachment_folder_name)

  
