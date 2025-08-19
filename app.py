import os
import logging
from flask import Flask, render_template, request, jsonify, session
from book_folding import BookFoldingGenerator
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "book_folding_art_secret_key_2024")

# Initialize book folding generator
generator = BookFoldingGenerator()

@app.route('/')
def index():
    """Main page with the book folding art generator interface"""
    return render_template('index.html')

@app.route('/generate_pattern', methods=['POST'])
def generate_pattern():
    """Generate folding pattern for given text and book specifications"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
            
        text = data.get('text', '').strip().upper()
        book_pages = int(data.get('book_pages', 400))
        book_height = float(data.get('book_height', 200))
        book_width = float(data.get('book_width', 15))
        
        if not text:
            return jsonify({'error': 'Текст не может быть пустым'}), 400
        
        if len(text) > 20:
            return jsonify({'error': 'Текст не должен превышать 20 символов'}), 400
        
        if book_pages < 200:
            return jsonify({'error': 'Минимальное количество страниц: 200'}), 400
        
        # Generate the folding pattern
        pattern = generator.generate_text_pattern(
            text=text,
            book_pages=book_pages,
            book_height_mm=book_height,
            book_width_mm=book_width
        )
        
        # Calculate statistics
        total_folds = len(pattern)
        pages_used = list(set([fold['page'] for fold in pattern]))
        
        result = {
            'pattern': pattern,
            'statistics': {
                'total_folds': total_folds,
                'pages_used': len(pages_used),
                'text': text,
                'estimated_time_minutes': total_folds * 2  # 2 minutes per fold estimate
            },
            'book_specs': {
                'pages': book_pages,
                'height': book_height,
                'width': book_width
            }
        }
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({'error': f'Ошибка в параметрах: {str(e)}'}), 400
    except Exception as e:
        app.logger.error(f"Error generating pattern: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при генерации паттерна'}), 500

@app.route('/get_templates')
def get_templates():
    """Get predefined templates for common shapes and symbols"""
    templates = generator.get_predefined_templates()
    return jsonify(templates)

@app.route('/generate_template_pattern', methods=['POST'])
def generate_template_pattern():
    """Generate pattern for a predefined template"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
            
        template_id = data.get('template_id')
        book_pages = int(data.get('book_pages', 400))
        book_height = float(data.get('book_height', 200))
        book_width = float(data.get('book_width', 15))
        
        if not template_id:
            return jsonify({'error': 'Template ID is required'}), 400
        
        pattern = generator.generate_template_pattern(
            template_id=template_id,
            book_pages=book_pages,
            book_height_mm=book_height,
            book_width_mm=book_width
        )
        
        if not pattern:
            return jsonify({'error': 'Шаблон не найден'}), 404
        
        # Calculate statistics
        total_folds = len(pattern)
        pages_used = list(set([fold['page'] for fold in pattern]))
        
        result = {
            'pattern': pattern,
            'statistics': {
                'total_folds': total_folds,
                'pages_used': len(pages_used),
                'template_id': template_id,
                'estimated_time_minutes': total_folds * 2
            },
            'book_specs': {
                'pages': book_pages,
                'height': book_height,
                'width': book_width
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        app.logger.error(f"Error generating template pattern: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при генерации шаблона'}), 500

@app.route('/export_pattern', methods=['POST'])
def export_pattern():
    """Export pattern as downloadable instructions"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
            
        pattern = data.get('pattern', [])
        book_specs = data.get('book_specs', {})
        text_or_template = data.get('text', data.get('template_id', 'Pattern'))
        
        # Generate formatted instructions
        instructions = generator.format_instructions(pattern, book_specs, text_or_template)
        
        return jsonify({
            'instructions': instructions,
            'filename': f"book_folding_{text_or_template.lower().replace(' ', '_')}.txt"
        })
        
    except Exception as e:
        app.logger.error(f"Error exporting pattern: {str(e)}")
        return jsonify({'error': 'Ошибка при экспорте инструкций'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
