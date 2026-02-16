import os
import re

file_path = r'd:\restaurant\restaurant\frontend\app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace \" with "
content = content.replace('\\"', '"')

# Replace unicode escapes like \u003e with their literal characters
# We use a regex to find \uXXXX and replace them
def decode_match(match):
    try:
        return match.group(0).encode('utf-8').decode('unicode-escape')
    except:
        return match.group(0)

content = re.sub(r'\\u[0-9a-fA-F]{4}', decode_match, content)

# Fix the specific logic error at line 403 (in case it wasn't fixed)
content = content.replace('["timing"| get_current_meal_time()', '["timing"] = get_current_meal_time()')
content = content.replace('["timing"]| get_current_meal_time()', '["timing"] = get_current_meal_time()')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File cleaned of unicode escapes and logic errors.")
