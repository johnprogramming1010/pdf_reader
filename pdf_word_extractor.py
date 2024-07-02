import PyPDF2
import re

def extract_words_with_page_number(pdf_path, output_file, skip_pages=None, target_word=None):
    word_list = []
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            if skip_pages and page_num + 1 in skip_pages:
                continue  # Skip the specified pages
            
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Extract words using regular expression, ignoring punctuation and numbers
            words = re.findall(r'\b[a-zA-Z]+\b', text)
            
            # Append each word along with its page number
            for word in words:
                word_list.append((word, page_num + 1))  # Adding 1 to page_num since it starts from 0
                
    # Sort the word list alphabetically
    word_list.sort(key=lambda x: x[0])
    
    # Write the sorted words and their page numbers to the output file
    with open(output_file, 'w') as output:
        for word, page_num in word_list:
            output.write(f"Word: {word}, Page: {page_num}\n")
    
    if target_word:
        # Find the page number containing the target word
        target_page = next((page_num for word, page_num in word_list if word == target_word), None)
        if target_page is not None:
            print(f"Target word '{target_word}' found on page {target_page}.")
        else:
            print(f"Target word '{target_word}' not found.")

# Example usage
pdf_path = 'example.pdf'  # Change this to your PDF file path
output_file = 'output.txt'  # Change this to the desired output text file path
skip_pages = [5, 6, 7]  # Pages to skip
target_word = "Figure"  # Target word to find
extract_words_with_page_number(pdf_path, output_file, skip_pages, target_word)

print("Extraction complete. Sorted words and their page numbers have been saved to", output_file)
