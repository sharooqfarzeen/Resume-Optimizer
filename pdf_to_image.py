import fitz  # PyMuPDF
from PIL import Image
import io

def pdf_to_image(file_object, max_pages=5, dpi=150):
    # Open the PDF file using PyMuPDF with a file-like object
    pdf_document = fitz.open(stream=file_object.read(), filetype="pdf")
    images = []
    
    # Loop through each page up to the maximum specified
    for page_number in range(min(max_pages, pdf_document.page_count)):
        page = pdf_document.load_page(page_number)   # Load page
        pix = page.get_pixmap(dpi=dpi)               # Render page to image with specified DPI
        
        # Convert the Pixmap to a PIL image
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
        
    pdf_document.close()
    return images