import re
import sys
import os
from terminal_color import print_header, print_blue

COMMON_IMAGE_REGEX = "\([a-zA-Z0-9%\-\/\.]*\.(png|jpg|jpeg)\)"

def process_obsidian_img_link(line, attachment_folder_name):
  is_attachment = re.search('!\[\[', line)
  is_img = re.search("\.(png|jpeg|jpg)\]\]", line)
  if (is_attachment and is_img):
    print_header(f'Found Obsidian Image link, Original Markdown:')
    print_blue(line)
    # remvoe ![[]]
    image_name = line.split("[[")[1].split("]]")[0]
    if image_name.split('/')[0] == attachment_folder_name:
        # remove attachments folder name
        return image_name[len(attachment_folder_name)+1:]
    else:
        return image_name
  return None
    

def get_img_name(line, attachment_folder_name):
  common_img_match = re.search(COMMON_IMAGE_REGEX, line)
  if common_img_match:
    print_header(f'Found Common Img Link:')
    print_blue(line)
    # notion export file due to encoding, the white space will become %20
    x = re.sub("%20", " ", common_img_match.group())
    # remove parentheses
    image_name  =  x[1: len(x) -1]
    if image_name.split('/')[0] == attachment_folder_name:
        # remove attachments folder name
        return image_name[len(attachment_folder_name)+1:]
    else:
        return image_name

  image_name = process_obsidian_img_link(line, attachment_folder_name)
  return image_name if image_name else None
  
  
def process_markdown_image(content, attachment_path):
  image_path_list = []
  for line_index, line in enumerate(content):
    attachment_folder_name = os.path.basename(attachment_path)
    image_name = get_img_name(line, attachment_folder_name)
    if image_name:
      print_blue(f'image name: {image_name}')
      image_path = {
        "line_index":  line_index,
        "img_path": f"{attachment_path}/{image_name}",
      }
      print_blue(f'image path: {image_path["img_path"]}') 
      image_path_list.append(image_path)
  
  return image_path_list

if __name__ == "__main__":
  markdown_path = sys.argv[1]
  attachment_path = f"{sys.argv[1]}/{sys.argv[2]}"
  result = process_markdown_image(markdown_path, attachment_path)
  print(result)
