from terminal_color import print_green

def write_new_content(note_path, note_name, content):
  with open(note_path, 'w') as md:
    new_content = "".join(content)
    md.write(new_content)
    print_green(f'Writing new image links to: {note_name}')
    return note_name
