import pyperclip
from datetime import datetime
from dictionary import PHRASES

codes = input("Enter code(s) separated by '-': ").strip().split("-")

lines = []
for code in codes:
    code = code.strip()
    if code in PHRASES:
        lines.append(f"• {PHRASES[code]}")
    else:
        lines.append(f"• [Unknown code: {code}]")

output = "\n".join(lines)
pyperclip.copy(output)

filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Copy is done. Saved to {filename}")
input("Press Enter to close.")
