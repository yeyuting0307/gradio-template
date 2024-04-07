#%%
from typing import Iterator, List, Dict
import fitz # PyMuPDF
import logging

class PdfParser:
    def __init__(self, include_images: bool = False) -> None:
        super().__init__()
        self.include_images = include_images

    def lazy_parse(self, file_path):
        try:
            pdf = self.read_pdf(file_path)
            
            for idx, page in enumerate(pdf):
                text_content = self.page_text(page)
                if self.include_images:
                    img_contents = self.page_images(pdf, page)
                    metadata = {"source": file_path, "index": idx, 'type': 'pdf', 'images': img_contents}
                else:
                    metadata = {"source": file_path, "index": idx, 'type': 'pdf'}
                if text_content == "" and metadata.get('images') is not None:
                    logging.warning("OCR processing")
                    from .ocr import detect_document
                    for img_contents in metadata.get('images'):
                        img = img_contents.get('image')
                        ocr_res = detect_document(img_bytes= img)
                        ocr_text = ocr_res.full_text_annotation.text
                        text_content += ocr_text
                yield text_content, metadata
        except Exception as e:
            print(e)
            yield "" , {}
        finally:
            print("PDF finished parsed")

    def read_pdf(self, file_path: str) -> List[Dict]:
        doc = fitz.open(file_path)
        return doc
    
    def page_text(self, page: fitz.Page) -> str:
        return page.get_text()
    
    def page_images(self, doc: fitz.Document ,page: fitz.Page) -> List[Dict]:
        img_list = page.get_images()
        img_info_list = []
        for img_index in img_list:
            for i in [0]: # TODO: [0, 1] for complete images but need adjust 1
                try:
                    img_info = doc.extract_image(img_index[i])
                    img_info_list.append(img_info)
                except Exception as e:
                    print(f"page_images > extract_image > img_index[{i}] Error",e)
           
        return img_info_list

# %%
