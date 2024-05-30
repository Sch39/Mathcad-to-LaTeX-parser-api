from flask import Flask, jsonify, request, Response
from socket import gethostname
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import shutil
import os
import uuid
from flask_cors import CORS

from src.utils.mathcad_xml_2_latex_parser import MathcadXML2LatexParser

load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # x MB max file size


API_KEY = os.getenv('CLIENT_API_KEY')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# def process_file(file_path):
#     # Dummy processing function to create a .tex file
#     base, _ = os.path.splitext(file_path)
#     tex_file_path = f"{base}.tex"
#     with open(file_path, 'r') as f:
#         content = f.read()
#     with open(tex_file_path, 'w') as f:
#         f.write(f"% Processed content\n{content}")
#     return tex_file_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'xmcd'


@app.route('/', methods = ['GET'])
def index():
  return 'Welcome to py-sch-api'

@app.route('/api/mathcad-2-latex', methods=['POST'])
def parser():
    api_key = request.headers.get('api-key')
    if api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename =='':
        return jsonify({'error': 'No file selected for uploading'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}__{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        mathcad_2_latex = MathcadXML2LatexParser(file_path)
        mathcad_2_latex.parse()

        parsed_file_path = mathcad_2_latex.get_output_fpath()

        def generate():
            with open(parsed_file_path, 'rb') as f:
                yield from f
            try:
                os.remove(file_path)
                os.remove(parsed_file_path)
            except Exception as e:
                print(f"Error cleaning up files: {e}")

        response = Response(generate(), content_type='application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(parsed_file_path)}'
        
        return response
    return jsonify({'error': 'File not allowed'}), 400

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run()