# sort_languages.py
import re

def sort_languages(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract the dictionary content
    dict_content = re.search(r'LANGUAGES = {(.+?)}', content, re.DOTALL).group(1)

    # Convert the dictionary string to a dictionary
    languages_dict = eval(f'{{{dict_content}}}')

    # Sort the dictionary by values (language names)
    sorted_languages = dict(sorted(languages_dict.items(), key=lambda item: item[1]))

    # Replace the original dictionary with the sorted one
    sorted_content = re.sub(r'LANGUAGES = {(.+?)}', f'LANGUAGES = {sorted_languages}', content, flags=re.DOTALL)

    # Write the sorted content back to the file
    with open(file_path, 'w') as file:
        file.write(sorted_content)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sort_languages.py path/to/languages.py")
    else:
        sort_languages(sys.argv[1])
