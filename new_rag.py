import os
import pdfplumber
import PyPDF2
import cohere

co = cohere.Client("p8zlCuXpKhFnIHaXOKZnwaOBPrCOsnSUoytpb4qd")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text

pdf_folder = r"C:\Users\khush\OneDrive\Desktop\rag_files"

documents = []
for filename in os.listdir(pdf_folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, filename)
        text = extract_text_from_pdf(pdf_path)
        documents.append({"title": filename, "text": text})

message = "When was icloud launched"

response = co.chat_stream(message=message, documents=documents)


# Display the response
citations = []
cited_documents = []

for event in response:
    if event.event_type == "text-generation":
        print(event.text, end="")
    elif event.event_type == "citation-generation":
        citations.extend(event.citations)
    elif event.event_type == "stream-end":
      cited_documents = event.response.documents

if citations:
    print("\n\nCITATIONS:")
    for citation in citations:
        print(citation)

    print("\nDOCUMENTS:")
    for document in cited_documents:
        print(document)
