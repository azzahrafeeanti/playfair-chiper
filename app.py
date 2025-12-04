from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def generate_matrix(key):
    key = re.sub(r'[^A-Z]', '', key.upper()).replace('J', 'I')
    matrix_str = ""
    seen = set()
    adasdasdadasdas
  
    for char in key:
        if char not in seen:
            matrix_str += char
            seen.add(char)
            

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ": 
        if char not in seen:
            matrix_str += char
            seen.add(char)
            

    return [list(matrix_str[i:i+5]) for i in range(0, 25, 5)]

def find_position(matrix, char):
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == char:
                return r, c
    return None

def prepare_text(text, is_encrypt):
    text = re.sub(r'[^A-Z]', '', text.upper()).replace('J', 'I')
    if not is_encrypt:
        return text


    result = ""
    i = 0
    while i < len(text):
        result += text[i]
        if i + 1 < len(text):
            if text[i] == text[i+1]:
                result += 'X'
            else:
                result += text[i+1]
                i += 1
        i += 1
        
    
    if len(result) % 2 != 0:
        result += 'X'
    return result

def process_playfair(key, text, mode):
    matrix = generate_matrix(key)
    is_encrypt = (mode == 'encrypt')
    prepared_text = prepare_text(text, is_encrypt)
    
    result_text = ""
    steps = []

    for i in range(0, len(prepared_text), 2):
        if i+1 >= len(prepared_text): break 
        
        char1, char2 = prepared_text[i], prepared_text[i+1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        rule = ""
        out1, out2 = "", ""
        
        if row1 == row2:
            rule = "Baris Sama"
            shift = 1 if is_encrypt else -1
            out1 = matrix[row1][(col1 + shift) % 5]
            out2 = matrix[row2][(col2 + shift) % 5]
        elif col1 == col2:
            rule = "Kolom Sama"
            shift = 1 if is_encrypt else -1
            out1 = matrix[(row1 + shift) % 5][col1]
            out2 = matrix[(row2 + shift) % 5][col2]
        else:
            rule = "Persegi Panjang"
            out1 = matrix[row1][col2]
            out2 = matrix[row2][col1]
            
        result_text += out1 + out2
        steps.append({
            "input": char1 + char2,
            "output": out1 + out2,
            "rule": rule
        })
        
    return {
        "result": result_text,
        "matrix": matrix, 
        "steps": steps
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    key = data.get('key', '')
    text = data.get('text', '')
    mode = data.get('mode', 'encrypt')
    
    if not key or not text:
        return jsonify({'error': 'Key dan Text harus diisi'}), 400
        
    response_data = process_playfair(key, text, mode)
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)