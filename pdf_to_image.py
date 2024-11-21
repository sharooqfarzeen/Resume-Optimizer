import pymupdf  # PyMuPDF
from PIL import Image
import io

def pdf_to_image(pdf_file, max_pages=5):
    """
    Converts pages of a PDF file into PNG images.

    Args:
        pdf_file (UploadedFile): The PDF file uploaded using st.file_uploader.
        max_pages (int): Maximum number of pages to convert.

    Returns:
        list: A list of PIL Image objects representing PNG images of the pages.
    """
    images = []
    
    # Open the PDF document using PyMuPDF
    pdf_document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")
    
    # Determine the number of pages to process
    total_pages = pdf_document.page_count
    pages_to_process = min(max_pages or total_pages, total_pages)
    
    for page_num in range(pages_to_process):
        # Select the page
        page = pdf_document[page_num]
        
        # Render the page as a pixmap
        pixmap = page.get_pixmap()
        
        # Convert the pixmap to a PIL Image
        image = Image.open(io.BytesIO(pixmap.tobytes("png")))
        images.append(image)
    
    # Close the PDF document
    pdf_document.close()
    
    return images