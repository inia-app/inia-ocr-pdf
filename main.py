from flask import Flask, request, jsonify
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from io import BytesIO

class OCR:
    @staticmethod
    def extract_text(pdf):
        model = ocr_predictor(pretrained=True)
        # PDF
        doc = DocumentFile.from_pdf(BytesIO(pdf))
        # Analyze
        result = model(doc)

        # Extrair o texto do resultado
        extracted_text = ""
        for page in result.pages:
            for block in page.blocks:
                for line in block.lines:
                    extracted_text += " ".join([word.value for word in line.words]) + "\n"

        # Agora a variável extracted_text contém todo o texto extraído do PDF
        return extracted_text

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'hello world'

@app.route('/upload/', methods=['POST'])
def upload_file():
    try:
        # Verificar se o arquivo está presente na requisição
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        # Ler o arquivo PDF da requisição
        file = request.files['file']
        pdf_data = file.read()
        
        # Extrair o texto do PDF
        text = OCR.extract_text(pdf_data)
        text_decode = text.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')

        return jsonify({"text": text_decode}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
