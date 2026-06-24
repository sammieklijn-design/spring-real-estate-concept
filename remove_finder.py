import re

content = open('index.html', encoding='utf-8').read()

# Remove the finder section
pattern = r'<section class="section finder-sec">.*?</div></section>'
new_content = re.sub(pattern, '', content, flags=re.DOTALL)

if new_content != content:
    open('index.html', 'w', encoding='utf-8', newline='').write(new_content)
    print('Removed finder-sec from index.html')
else:
    print('Pattern not found!')
    # Show first 200 chars around finder-sec
    idx = content.find('finder-sec')
    print('Context:', repr(content[idx-20:idx+100]))
