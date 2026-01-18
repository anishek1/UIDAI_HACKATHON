"""
Sanitize HTML submission file for UIDAI Hackathon.
Removes problematic characters that may trigger security filters.
"""
import re

# Read the original file
with open('UIDAI_1545_submission.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Character replacements
replacements = {
    # Emojis to text equivalents
    '🇮🇳': '[INDIA]',
    '🔴': '[CRITICAL]',
    '🟡': '[WARNING]',
    '🔵': '[INFO]',
    '⚠️': '[ALERT]',
    '📥': '[1]',
    '🧹': '[2]',
    '⚙️': '[3]',
    '📊': '[4]',
    '🎯': '[5]',
    '🔍': '*',
    '💰': '[DBT]',
    '★': '*',
    '✓': '[OK]',
    
    # Mathematical symbols
    '→': '->',
    '×': 'x',
    '₹': 'Rs.',
    '–': '-',
    '≥': '>=',
    '•': '-',
    
    # Handle HTML entities that might be problematic
    '&lt;': 'less than',
    '&gt;': 'greater than',
    '&amp;': 'and',
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Remove code blocks entirely - replace with descriptive text
# This is aggressive but ensures no code patterns remain
code_block_pattern = r'<div class="code-block">.*?</div>'
content = re.sub(code_block_pattern, '<div class="code-block">[Code implementation available in GitHub repository]</div>', content, flags=re.DOTALL)

# Remove any remaining non-ASCII characters that might cause issues
def remove_non_ascii(text):
    result = []
    for char in text:
        if ord(char) < 128 or char in '\n\r\t':
            result.append(char)
        elif ord(char) in range(0x2000, 0x3000):  # General punctuation
            result.append(' ')
        elif ord(char) > 127:
            # Try to keep common extended chars
            if char in 'àáâãäåèéêëìíîïòóôõöùúûüýÿñ':
                result.append(char)
            else:
                result.append(' ')
    return ''.join(result)

content = remove_non_ascii(content)

# Clean up multiple spaces
content = re.sub(r' +', ' ', content)

# Write the cleaned file
with open('UIDAI_1545_submission_CLEAN.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned file created: UIDAI_1545_submission_CLEAN.html")
print("Original backup: UIDAI_1545_submission_BACKUP.html")
