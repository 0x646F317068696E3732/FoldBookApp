import os
import logging
from flask import Flask, render_template, request, jsonify, session
from book_folding_dual import DualFoldBookGenerator
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "book_folding_art_secret_key_2024")

# Initialize book folding generator
generator = DualFoldBookGenerator()

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
        
        if not text:
            return jsonify({'error': 'Текст не может быть пустым'}), 400
        
        if len(text) > 20:
            return jsonify({'error': 'Текст не должен превышать 20 символов'}), 400
        
        if book_pages < 200:
            return jsonify({'error': 'Минимальное количество страниц: 200'}), 400
        
        # Generate the folding pattern
        pattern = generator.generate_pattern(text, book_pages, book_height)
        
        # Calculate statistics
        total_folds = len(pattern) * 2  # Каждая страница имеет 2 сгиба
        pages_used = len(pattern)
        estimated_time = total_folds * 2  # 2 минуты на сгиб
        
        stats = {
            'total_folds': total_folds,
            'pages_used': pages_used,
            'estimated_time_minutes': estimated_time
        }
        
        result = {
            'pattern': pattern,
            'statistics': {
                'total_folds': stats['total_folds'],
                'pages_used': stats['pages_used'],
                'text': text,
                'estimated_time_minutes': stats['estimated_time_minutes']
            },
            'book_specs': {
                'pages': book_pages,
                'height': book_height
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
    # Простые готовые шаблоны
    templates = {
        'logos': [
            {'id': 'love', 'name': 'LOVE', 'icon': '❤️'},
            {'id': 'hope', 'name': 'HOPE', 'icon': '🌟'},
            {'id': 'dream', 'name': 'DREAM', 'icon': '💭'}
        ],
        'symbols': [
            {'id': 'heart', 'name': 'Сердце', 'icon': '♥'},
            {'id': 'star', 'name': 'Звезда', 'icon': '★'},
            {'id': 'smile', 'name': 'Улыбка', 'icon': '☺'}
        ]
    }
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
        
        if not template_id:
            return jsonify({'error': 'Template ID is required'}), 400
        
        # Простая конвертация template_id в текст
        template_texts = {
            'love': 'LOVE',
            'hope': 'HOPE', 
            'dream': 'DREAM',
            'heart': '♥',
            'star': '★',
            'smile': '☺'
        }
        
        text = template_texts.get(template_id, template_id.upper())
        
        # Generate pattern
        pattern = generator.generate_pattern(text, book_pages, book_height)
        
        # Calculate statistics
        total_folds = len(pattern) * 2  # Каждая страница имеет 2 сгиба
        pages_used = len(pattern)
        estimated_time = total_folds * 2  # 2 минуты на сгиб
        
        stats = {
            'total_folds': total_folds,
            'pages_used': pages_used,
            'estimated_time_minutes': estimated_time
        }
        
        result = {
            'pattern': pattern,
            'statistics': {
                'total_folds': stats['total_folds'],
                'pages_used': stats['pages_used'],
                'template_id': template_id,
                'estimated_time_minutes': stats['estimated_time_minutes']
            },
            'book_specs': {
                'pages': book_pages,
                'height': book_height
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
        
        # Простое форматирование инструкций
        instructions = f"ИНСТРУКЦИИ ПО СКЛАДЫВАНИЮ КНИГИ\nТекст: {text_or_template}\n\n"
        instructions += f"Параметры книги:\n"
        instructions += f"- Страниц: {book_specs.get('pages', 'не указано')}\n"
        instructions += f"- Высота: {book_specs.get('height', 'не указана')} мм\n\n"
        instructions += "ПОШАГОВЫЕ ИНСТРУКЦИИ:\n\n"
        
        for i, fold in enumerate(pattern, 1):
            fold_type = fold.get('fold_type', 'оба')
            if fold_type == 'top':
                corner_text = "верхний угол"
            elif fold_type == 'bottom':
                corner_text = "нижний угол"
            else:
                corner_text = "оба угла"
                
            instructions += f"{i}. Страница {fold['page']}: согнуть {corner_text} на {fold['offset_mm']} мм\n"
        
        return jsonify({
            'instructions': instructions,
            'filename': f"book_folding_{text_or_template.lower().replace(' ', '_')}.txt"
        })
        
    except Exception as e:
        app.logger.error(f"Error exporting pattern: {str(e)}")
        return jsonify({'error': 'Ошибка при экспорте инструкций'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
