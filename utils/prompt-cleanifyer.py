import sys
import re
import os

def replace_headers(markdown_text):
    # replace headings, marked with heading [br]---- with ## heading
    markdown_text = re.sub(r'^\s*([^-\n].*?)\s*\n\s*-+\s*$', r'## \1: ', markdown_text, flags=re.MULTILINE)
    # Delete all line breaks
    markdown_text = re.sub(r'\n', '', markdown_text)
    return markdown_text

def main(input_file):
    output_file = os.path.splitext(input_file)[0] + "_cleanified" + os.path.splitext(input_file)[1]

    with open(input_file, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    updated_markdown = replace_headers(markdown_text)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_markdown)

    print("File successfully updated, new file created:", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usabe: this-skript.py prompt-markdown.md")
        sys.exit(1)

    input_file = sys.argv[1]

    main(input_file)
