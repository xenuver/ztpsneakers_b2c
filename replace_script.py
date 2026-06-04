import os
import re

template_dir = r"d:\! Coding New\ztpsneakers_b2c\ztpsneakers\templates"

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            new_content = content
            # Replace green hovers
            new_content = new_content.replace("hover:bg-green-800", "hover:bg-orange-600")
            new_content = new_content.replace("hover:bg-green-50", "hover:bg-orange-50")
            
            # Replace floatformat with intcomma
            new_content = new_content.replace('floatformat:"0"', 'intcomma')
            new_content = new_content.replace("floatformat:'0'", 'intcomma')
            new_content = new_content.replace("floatformat:0", 'intcomma')
            
            # Replace the neon green color with orange
            new_content = new_content.replace("#E8FF00", "#ef8215")
            new_content = new_content.replace("#e8ff00", "#ef8215")
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {path}")
print("Done.")
