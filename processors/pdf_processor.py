import fitz  # PyMuPDF

def process_pdf(file_path):
    """
    Process a PDF file to extract text and images.
    Returns a dictionary with 'text' and 'images' (list of image bytes).
    """
    doc = fitz.open(file_path)
    extracted_text = ""
    images = []
    
    for page in doc:
        extracted_text += page.get_text("text") + "\n"
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)
            
    return {"text": extracted_text, "images": images}
