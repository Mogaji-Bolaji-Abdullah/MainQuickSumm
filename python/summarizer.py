import google.generativeai as genai
import sys

# Configure the API key
genai.configure(api_key='AIzaSyDd8V2D0lV2HECOD8tnV7Ct6LTmM6S1_G0')

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')  # Updated to a more capable model

try:
    from fpdf import FPDF
    from docx import Document
    import pyperclip
except ImportError as e:
    print(f"Error: {e}. Please install the required libraries.")
    sys.exit(1)

def get_summary(text, summary_length):
    max_tokens_map = {
        'short': 50,
        'medium': 150,
        'long': 300
    }
    
    max_tokens = max_tokens_map.get(summary_length, 150)
    
    try:
        response = model.generate_content(
            f"Summarize the following text in approximately {max_tokens} words:\n\n{text}"
        )
        summary = response.text.strip()
        return summary
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def count_words(text):
    return len(text.split())

def save_as_txt(filename, text):
    try:
        with open(filename, 'w', encoding='utf-8') as file:  # Added encoding
            file.write(text)
        print(f"Summary saved as {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

def save_as_pdf(filename, text):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(filename)
        print(f"Summary saved as {filename}")
    except Exception as e:
        print(f"Error saving PDF: {e}")

def save_as_doc(filename, text):
    try:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(filename)
        print(f"Summary saved as {filename}")
    except Exception as e:
        print(f"Error saving DOC: {e}")

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        print("Summary copied to clipboard.")
    except pyperclip.PyperclipException as e:
        print(f"Error copying to clipboard: {e}")

def main():
    # Prompt user for input text
    input_text = input("Enter the text you want to summarize: ").strip()

    # Prompt user for summary length
    valid_lengths = ['short', 'medium', 'long']
    summary_length = input("Enter summary length (short, medium, long): ").strip().lower()
    while summary_length not in valid_lengths:
        summary_length = input("Invalid input. Please enter summary length (short, medium, long): ").strip().lower()

    # Get summary
    summary = get_summary(input_text, summary_length)

    # Print original text word count and summary
    if summary:
        original_word_count = count_words(input_text)
        summary_word_count = count_words(summary)
        print(f"Original text word count: {original_word_count}")
        print(f"Summarized text word count: {summary_word_count}")
        print("Summary:", summary)
        
        # Ask user for the output format
        output_format = input("Enter the format for download (txt, pdf, doc) or 'clipboard' to copy to clipboard: ").strip().lower()
        
        if output_format in ['txt', 'pdf', 'doc']:
            filename = f"summary.{output_format}"
            if output_format == 'txt':
                save_as_txt(filename, summary)
            elif output_format == 'pdf':
                save_as_pdf(filename, summary)
            elif output_format == 'doc':
                save_as_doc(filename, summary)
        
        elif output_format == 'clipboard':
            copy_to_clipboard(summary)
        
        else:
            print("Invalid format selected.")
    else:
        print("Could not retrieve summary.")

if __name__ == "__main__":
    main()