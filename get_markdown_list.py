from os import listdir

def get_markdown_list(vault_path = None):
  if (vault_path is None):
    print('Vault Path Must Provided')
    return

  all_directories = listdir(vault_path)

  # filter out none markdown files
  markdownList = list(filter(
    lambda dir: len(dir.split('.')) > 1 and dir.split('.')[1] == 'md',
    all_directories
  ))
  
  markdown_path_list =  map(lambda name: f'{vault_path}/{name}', markdownList)

  return markdown_path_list
  

if __name__ == '__main__':
  get_markdown_list()