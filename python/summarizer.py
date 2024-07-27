import requests
import openai
import pyperclip
from fpdf import FPDF
from docx import Document
import fitz  # PyMuPDF for PDF handling

openai.api_key = 'sk-proj-3EE2GIh130QiPPkz2CE9T3BlbkFJSNxXMQuVqqt6NWOjRHku'

def get_summary(text, summary_length):
    max_tokens_map = {
        'short': 50,
        'medium': 150,
        'large': 300
    }
    
    max_tokens = max_tokens_map.get(summary_length, 150)  # Default to 'medium' if invalid input
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}\n\nSummary:"}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Please check your quota and billing details.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def count_words(text):
    return len(text.split())

def save_as_txt(filename, text):
    with open(filename, 'w') as file:
        file.write(text)

def save_as_pdf(filename, text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

def save_as_doc(filename, text):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def copy_to_clipboard(text):
    pyperclip.copy(text)

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"An error occurred while extracting text from PDF: {e}")
        return None

# Prompt user for input method
input_method = input("Do you want to paste text or upload a file? (paste/upload): ").strip().lower()

if input_method == 'paste':
    input_text = input("Enter the text you want to summarize: ")
elif input_method == 'upload':
    file_type = input("Enter the file type (txt or pdf): ").strip().lower()
    file_path = input("Enter the file path: ")
    
    if file_type == 'txt':
        try:
            with open(file_path, 'r') as file:
                input_text = file.read()
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            input_text = ""
    elif file_type == 'pdf':
        input_text = extract_text_from_pdf(file_path)
        if input_text is None:
            input_text = ""
    else:
        print("Unsupported file type.")
        input_text = ""
else:
    print("Invalid input method.")
    input_text = ""

if input_text:
    # Prompt user for summary length
    summary_length = input("Enter summary length (short, medium, large): ").strip().lower()

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
            print(f"Summary saved as {filename}")
        
        elif output_format == 'clipboard':
            copy_to_clipboard(summary)
            print("Summary copied to clipboard.")
        
        else:
            print("Invalid format selected.")
    else:
        print("Could not retrieve summary due to rate limit.")
else:
    print("No text available for summarization.")
