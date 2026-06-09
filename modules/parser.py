import docx
import fitz

def extract_text(file):

    if file.name.endswith('.docx'):

        doc=docx.Document(file)

        text='\n'.join(
        [p.text for p in doc.paragraphs]
        )

        return text

    if file.name.endswith('.pdf'):

        pdf=fitz.open(stream=file.read(), filetype='pdf')

        text=''

        for page in pdf:
            text += page.get_text()

        return text