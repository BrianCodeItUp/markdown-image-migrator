class bcolors:
    Header = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def apply_style(style):
  def color_string(line):
    return f'{style}{line}{bcolors.ENDC}'
  return color_string

header = apply_style(bcolors.Header)
blue = apply_style(bcolors.OKBLUE)
green = apply_style(bcolors.OKGREEN)
warning = apply_style(bcolors.WARNING)
fail = apply_style(bcolors.FAIL)

def apply_print_format(format_func):
  def print_with_format(line):
    print(format_func(line))
  return print_with_format

print_header = apply_print_format(header)
print_blue = apply_print_format(blue)
print_green = apply_print_format(green)
print_warning = apply_print_format(warning)
print_fail = apply_print_format(fail)

