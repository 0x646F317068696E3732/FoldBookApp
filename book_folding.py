import math
import json
from typing import List, Dict, Tuple, Optional

class BookFoldingGenerator:
    """
    Book Folding Art Pattern Generator
    Generates precise folding instructions for creating 3D text from book pages
    """
    
    def __init__(self):
        # Character patterns defined as binary matrices (1 = fold, 0 = no fold)
        # Each character is 7 units high and 5 units wide for consistency
        self.char_patterns = {
            'A': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 0]
            ],
            'B': [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ],
            'C': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]
            ],
            'D': [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ],
            'E': [
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1]
            ],
            'F': [
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0]
            ],
            'G': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]
            ],
            'H': [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1]
            ],
            'I': [
                [1, 1, 1, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 1, 1, 1, 1]
            ],
            'J': [
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]
            ],
            'K': [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 1, 0],
                [1, 0, 1, 0, 0],
                [1, 1, 0, 0, 0],
                [1, 0, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1]
            ],
            'L': [
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1]
            ],
            'M': [
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1]
            ],
            'N': [
                [1, 0, 0, 0, 1],
                [1, 1, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1]
            ],
            'O': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]
            ],
            'P': [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0]
            ],
            'Q': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 1, 0],
                [0, 1, 1, 0, 1]
            ],
            'R': [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1]
            ],
            'S': [
                [0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ],
            'T': [
                [1, 1, 1, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0]
            ],
            'U': [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]
            ],
            'V': [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            'W': [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 0, 0, 1]
            ],
            'X': [
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1]
            ],
            'Y': [
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0]
            ],
            'Z': [
                [1, 1, 1, 1, 1],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1]
            ],
            ' ': [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            '❤': [  # Heart symbol
                [0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]
            ]
        }
    
    def generate_text_pattern(self, text: str, book_pages: int, book_height_mm: float, book_width_mm: float) -> List[Dict]:
        """
        Generate folding pattern for given text
        """
        text = text.upper().strip()
        if not text:
            raise ValueError("Text cannot be empty")
        
        # Calculate text dimensions
        text_width = len(text) * 5 + (len(text) - 1) * 1  # 5 units per char + 1 unit spacing
        text_height = 7  # Standard character height
        
        # Calculate available pages (only even pages are used for folding)
        usable_pages = book_pages // 2
        
        if text_width > usable_pages:
            raise ValueError(f"Text too long for book. Maximum {usable_pages // 6} characters for {book_pages} pages")
        
        # Generate binary matrix for entire text
        text_matrix = self._create_text_matrix(text)
        
        # Convert matrix to folding pattern
        pattern = self._matrix_to_pattern(text_matrix, book_pages, book_height_mm, book_width_mm)
        
        return pattern
    
    def _create_text_matrix(self, text: str) -> List[List[int]]:
        """Create binary matrix representation of text"""
        if not text:
            return []
        
        # Initialize matrix with proper dimensions
        text_height = 7
        text_width = len(text) * 5 + (len(text) - 1) * 1  # Character width + spacing
        matrix = [[0 for _ in range(text_width)] for _ in range(text_height)]
        
        col_offset = 0
        for char in text:
            if char in self.char_patterns:
                char_pattern = self.char_patterns[char]
                # Copy character pattern to matrix
                for row in range(text_height):
                    for col in range(5):  # Each character is 5 units wide
                        if col_offset + col < text_width:
                            matrix[row][col_offset + col] = char_pattern[row][col]
                col_offset += 6  # 5 for character + 1 for spacing
            else:
                # Unknown character, skip
                col_offset += 6
        
        return matrix
    
    def _matrix_to_pattern(self, matrix: List[List[int]], book_pages: int, book_height_mm: float, book_width_mm: float) -> List[Dict]:
        """Convert binary matrix to folding instructions"""
        if not matrix:
            return []
        
        pattern = []
        matrix_height = len(matrix)
        matrix_width = len(matrix[0]) if matrix else 0
        
        usable_pages = book_pages // 2
        
        # Calculate scaling
        pages_per_column = max(1, usable_pages / matrix_width) if matrix_width > 0 else 1
        height_per_row = book_height_mm / matrix_height if matrix_height > 0 else book_height_mm
        
        # Process each column of the matrix
        for col in range(matrix_width):
            # Calculate which page this column corresponds to
            page_offset = int(col / pages_per_column)
            page_number = (page_offset + 1) * 2  # Only even pages
            
            if page_number > book_pages:
                break
            
            # Find fold segments in this column
            fold_segments = self._find_fold_segments(matrix, col)
            
            # Convert segments to measurements
            for start_row, end_row in fold_segments:
                start_mm = round(start_row * height_per_row, 1)
                end_mm = round((end_row + 1) * height_per_row, 1)
                
                # Ensure measurements are within book bounds
                start_mm = max(0, min(start_mm, book_height_mm))
                end_mm = max(start_mm, min(end_mm, book_height_mm))
                
                if end_mm > start_mm:  # Only add valid folds
                    pattern.append({
                        'page': page_number,
                        'start_mm': start_mm,
                        'end_mm': end_mm,
                        'depth_mm': round(book_width_mm * 0.7, 1)  # Fold to 70% depth
                    })
        
        # Sort pattern by page number
        pattern.sort(key=lambda x: x['page'])
        
        return pattern
    
    def _find_fold_segments(self, matrix: List[List[int]], col: int) -> List[Tuple[int, int]]:
        """Find continuous segments of 1s in a column"""
        segments = []
        if col >= len(matrix[0]):
            return segments
        
        start = None
        for row in range(len(matrix)):
            if matrix[row][col] == 1:
                if start is None:
                    start = row
            else:
                if start is not None:
                    segments.append((start, row - 1))
                    start = None
        
        # Handle case where segment continues to end
        if start is not None:
            segments.append((start, len(matrix) - 1))
        
        return segments
    
    def get_predefined_templates(self) -> Dict:
        """Get list of predefined templates"""
        return {
            'logos': [
                {'id': 'apple', 'name': 'Apple Logo', 'description': 'Знаменитый логотип Apple'},
                {'id': 'nike', 'name': 'Nike Swoosh', 'description': 'Логотип Nike'},
                {'id': 'batman', 'name': 'Batman Logo', 'description': 'Символ Бэтмена'},
                {'id': 'superman', 'name': 'Superman Logo', 'description': 'Символ Супермена'}
            ],
            'symbols': [
                {'id': 'heart', 'name': 'Сердце ❤', 'description': 'Символ сердца'},
                {'id': 'star', 'name': 'Звезда ⭐', 'description': 'Пятиконечная звезда'},
                {'id': 'peace', 'name': 'Мир ☮', 'description': 'Символ мира'},
                {'id': 'infinity', 'name': 'Бесконечность ∞', 'description': 'Символ бесконечности'}
            ],
            'emojis': [
                {'id': 'smile', 'name': 'Улыбка 😊', 'description': 'Улыбающийся смайлик'},
                {'id': 'love', 'name': 'Любовь 😍', 'description': 'Влюбленный смайлик'},
                {'id': 'thumbs_up', 'name': 'Лайк 👍', 'description': 'Большой палец вверх'},
                {'id': 'fire', 'name': 'Огонь 🔥', 'description': 'Символ огня'}
            ]
        }
    
    def generate_template_pattern(self, template_id: str, book_pages: int, book_height_mm: float, book_width_mm: float) -> Optional[List[Dict]]:
        """Generate pattern for a predefined template"""
        # Template patterns (simplified versions for demonstration)
        template_matrices = {
            'apple': [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            'heart': [
                [0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            'star': [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            # Add more templates as needed
        }
        
        if template_id not in template_matrices:
            return None
        
        matrix = template_matrices[template_id]
        return self._matrix_to_pattern(matrix, book_pages, book_height_mm, book_width_mm)
    
    def format_instructions(self, pattern: List[Dict], book_specs: Dict, text_or_template: str) -> str:
        """Format pattern as human-readable instructions"""
        if not pattern:
            return "Нет инструкций для генерации."
        
        instructions = []
        instructions.append(f"ИНСТРУКЦИИ ПО СКЛАДЫВАНИЮ КНИГИ")
        instructions.append(f"=" * 50)
        instructions.append(f"Текст/Шаблон: {text_or_template}")
        instructions.append(f"Параметры книги:")
        instructions.append(f"  - Страниц: {book_specs.get('pages', 'N/A')}")
        instructions.append(f"  - Высота: {book_specs.get('height', 'N/A')} мм")
        instructions.append(f"  - Ширина: {book_specs.get('width', 'N/A')} мм")
        instructions.append("")
        instructions.append("ПОШАГОВЫЕ ИНСТРУКЦИИ:")
        instructions.append("-" * 30)
        
        for i, fold in enumerate(pattern, 1):
            instructions.append(f"Шаг {i}:")
            instructions.append(f"  Страница: {fold['page']}")
            instructions.append(f"  Измерьте от верха книги: {fold['start_mm']} мм")
            instructions.append(f"  Измерьте до: {fold['end_mm']} мм")
            instructions.append(f"  Согните на глубину: {fold['depth_mm']} мм")
            instructions.append("")
        
        instructions.append("СОВЕТЫ:")
        instructions.append("- Используйте линейку для точных измерений")
        instructions.append("- Сгибайте страницы аккуратно, чтобы не порвать")
        instructions.append("- Работайте медленно и терпеливо")
        instructions.append("- Проверяйте результат после каждых 10-20 сгибов")
        
        return "\n".join(instructions)
