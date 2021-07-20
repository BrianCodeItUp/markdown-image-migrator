import re
import sys

COMMON_IMAGE_REGEX = "\([a-zA-Z0-9%\-\/\.]*\.(png|jpg|jpeg)\)"
OBSIDIAN_PASTED_IMAGE_REGEX = "Pasted image \d{14}\.(?:png|jpg|jpeg)"

def get_img_name(line):
  common_img_match = re.search(COMMON_IMAGE_REGEX, line)
  if common_img_match:
    # notion export file due to encoding, the white space will become %20
    x = re.sub("%20", " ", common_img_match.group())
    # remove parentheses
    image_path  =  x[1: len(x) -1]
    return image_path

  obsidian_img_match = re.search(OBSIDIAN_PASTED_IMAGE_REGEX, line)
  if obsidian_img_match:
    return obsidian_img_match.group()

  return None
  
  
def process_markdown_image(content, attachment_path):
  image_path_list = []
  for line_index, line in enumerate(content):
    image_name = get_img_name(line)
  
    if image_name:
      image_path = {
        "line_index":  line_index,
        "img_path": f"{attachment_path}/{image_name}",
      } 
      image_path_list.append(image_path)
  
  return image_path_list

if __name__ == "__main__":
  markdown_path = sys.argv[1]
  attachment_path = f"{sys.argv[1]}/{sys.argv[2]}"
  result = process_markdown_image(markdown_path, attachment_path)
  print(result)
