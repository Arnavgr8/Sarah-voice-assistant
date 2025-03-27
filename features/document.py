from core.speech import speak
import PyPDF2

def pdf_reader():
    speak("Please say the name of the PDF book")
    name = takecommand().lower()
    try:
        with open(f"{name}.pdf", "rb") as book:
            pdf_reader = PyPDF2.PdfFileReader(book)
            pages = pdf_reader.numPages
            speak(f"This book contains {pages} pages")
            speak("Which page should I read?")
            pg = int(takecommand().lower())
            page = pdf_reader.getPage(pg)
            text = page.extractText()
            speak(text)
    except Exception as e:
        speak(f"Error reading PDF: {str(e)}")