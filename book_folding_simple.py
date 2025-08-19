import math
from typing import List, Dict, Tuple

class SimpleBookFoldingGenerator:
    """
    Упрощенный генератор book folding - только сгибы углов страниц
    """
    
    def __init__(self):
        # Параметры книги
        self.total_pages = 400
        self.page_height = 200  # мм - единственный важный параметр
        
        # Минимальные требования
        self.min_pages_per_letter = 8
        self.min_offset = 5      # минимальный отступ от края
        self.max_offset = 195    # максимальный отступ (почти до конца страницы)
        
    def set_book_parameters(self, pages: int, height: int):
        """Установить параметры книги - только страницы и высота"""
        self.total_pages = pages
        self.page_height = height
        self.max_offset = height - 5  # оставляем 5мм от края
        
    def text_to_pattern(self, text: str) -> List[Dict]:
        """
        Преобразует текст в простой паттерн сгибов углов
        """
        text = text.strip().upper()
        if not text:
            return []
            
        # Поддерживаемые символы
        supported_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789 ')
        clean_text = ''.join(c for c in text if c in supported_chars)
        
        if not clean_text:
            return []
        
        # Рассчитываем доступные четные страницы
        available_pages = self.total_pages // 2
        letter_count = len([c for c in clean_text if c != ' '])
        
        if letter_count == 0:
            return []
            
        # Страниц на символ
        pages_per_letter = max(self.min_pages_per_letter, available_pages // letter_count)
        
        # Генерируем паттерн
        pattern = []
        current_page = 2  # Начинаем с первой четной страницы
        
        for char in clean_text:
            if char == ' ':
                # Пропуск для пробела
                current_page += max(2, pages_per_letter // 4)
                continue
                
            char_folds = self._generate_letter_corner_folds(char, current_page, pages_per_letter)
            pattern.extend(char_folds)
            current_page += pages_per_letter
            
            if current_page > self.total_pages:
                break
        
        return pattern
    
    def _generate_letter_corner_folds(self, letter: str, start_page: int, page_count: int) -> List[Dict]:
        """Генерирует сгибы углов для одной буквы"""
        folds = []
        
        # Получаем паттерн сгибов для буквы
        letter_pattern = self._get_letter_fold_pattern(letter)
        
        for i in range(page_count):
            page_num = start_page + (i * 2)
            if page_num > self.total_pages:
                break
                
            # Позиция в букве (0.0 - 1.0)
            progress = i / (page_count - 1) if page_count > 1 else 0.5
            
            # Получаем сгибы углов для этой позиции
            corner_folds = self._calculate_corner_folds(letter_pattern, progress)
            
            for fold_type, offset_mm in corner_folds:
                if self.min_offset <= offset_mm <= self.max_offset:
                    folds.append({
                        'page': page_num,
                        'fold_type': fold_type,  # 'top' или 'bottom' или 'both'
                        'offset_mm': round(offset_mm, 1)
                    })
        
        return folds
    
    def _get_letter_fold_pattern(self, letter: str) -> List[Tuple[str, float]]:
        """
        Возвращает паттерн сгибов для буквы
        Каждый элемент: (тип_сгиба, позиция_от_0_до_1)
        """
        patterns = {
            # Латинские буквы - упрощенные паттерны сгибов
            'A': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            'B': [('top', 0.1), ('both', 0.3), ('both', 0.7), ('bottom', 0.9)],
            'C': [('top', 0.2), ('top', 0.8)],
            'D': [('top', 0.1), ('both', 0.5), ('bottom', 0.9)],
            'E': [('top', 0.1), ('both', 0.5), ('bottom', 0.9)],
            'F': [('top', 0.1), ('both', 0.5)],
            'G': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            'H': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'I': [('both', 0.5)],
            'J': [('top', 0.1), ('bottom', 0.7)],
            'K': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'L': [('both', 0.3), ('bottom', 0.9)],
            'M': [('both', 0.1), ('both', 0.3), ('both', 0.7), ('both', 0.9)],
            'N': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'O': [('top', 0.2), ('both', 0.4), ('both', 0.6), ('bottom', 0.8)],
            'P': [('top', 0.1), ('both', 0.4), ('both', 0.6)],
            'Q': [('top', 0.2), ('both', 0.4), ('both', 0.6), ('bottom', 0.8)],
            'R': [('top', 0.1), ('both', 0.4), ('both', 0.6), ('bottom', 0.9)],
            'S': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            'T': [('top', 0.1), ('both', 0.5)],
            'U': [('both', 0.3), ('both', 0.6), ('bottom', 0.9)],
            'V': [('both', 0.2), ('bottom', 0.8)],
            'W': [('both', 0.2), ('both', 0.4), ('both', 0.6), ('bottom', 0.8)],
            'X': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'Y': [('both', 0.3), ('both', 0.6)],
            'Z': [('top', 0.1), ('both', 0.5), ('bottom', 0.9)],
            
            # Русские буквы
            'А': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            'Б': [('top', 0.1), ('both', 0.5), ('bottom', 0.9)],
            'В': [('top', 0.1), ('both', 0.3), ('both', 0.7), ('bottom', 0.9)],
            'Г': [('top', 0.1), ('both', 0.5)],
            'Д': [('top', 0.1), ('both', 0.5), ('bottom', 0.9)],
            'Е': [('top', 0.1), ('both', 0.5), ('bottom', 0.9)],
            'Ё': [('top', 0.1), ('both', 0.5), ('bottom', 0.9)],
            'Ж': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'З': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            'И': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'Й': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'К': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'Л': [('both', 0.3), ('both', 0.6), ('bottom', 0.9)],
            'М': [('both', 0.1), ('both', 0.3), ('both', 0.7), ('both', 0.9)],
            'Н': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'О': [('top', 0.2), ('both', 0.4), ('both', 0.6), ('bottom', 0.8)],
            'П': [('top', 0.1), ('both', 0.5), ('both', 0.8)],
            'Р': [('top', 0.1), ('both', 0.4), ('both', 0.6)],
            'С': [('top', 0.2), ('bottom', 0.8)],
            'Т': [('top', 0.1), ('both', 0.5)],
            'У': [('both', 0.3), ('bottom', 0.7)],
            'Ф': [('top', 0.2), ('both', 0.4), ('both', 0.6), ('bottom', 0.8)],
            'Х': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'Ц': [('both', 0.3), ('both', 0.6), ('bottom', 0.9)],
            'Ч': [('both', 0.2), ('both', 0.6)],
            'Ш': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'Щ': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'Ъ': [('top', 0.2), ('both', 0.6)],
            'Ы': [('both', 0.2), ('both', 0.5), ('both', 0.8)],
            'Ь': [('both', 0.3), ('both', 0.6)],
            'Э': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            'Ю': [('both', 0.2), ('both', 0.4), ('both', 0.6), ('both', 0.8)],
            'Я': [('top', 0.1), ('both', 0.4), ('both', 0.7), ('bottom', 0.9)],
            
            # Цифры
            '0': [('top', 0.2), ('both', 0.4), ('both', 0.6), ('bottom', 0.8)],
            '1': [('both', 0.5)],
            '2': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            '3': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            '4': [('both', 0.3), ('both', 0.6)],
            '5': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            '6': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)],
            '7': [('top', 0.1), ('bottom', 0.7)],
            '8': [('top', 0.2), ('both', 0.4), ('both', 0.6), ('bottom', 0.8)],
            '9': [('top', 0.2), ('both', 0.5), ('bottom', 0.8)]
        }
        
        return patterns.get(letter, [('both', 0.5)])  # По умолчанию один сгиб посередине
    
    def _calculate_corner_folds(self, pattern: List[Tuple[str, float]], progress: float) -> List[Tuple[str, float]]:
        """
        Рассчитывает сгибы углов для текущей позиции в букве
        """
        folds = []
        
        for fold_type, position in pattern:
            # Интерполируем позицию сгиба в зависимости от прогресса
            # Добавляем вариацию для естественности
            variation = math.sin(progress * math.pi * 3) * 0.1
            adjusted_position = position + variation * (1 - abs(position - 0.5))
            
            # Конвертируем в миллиметры
            offset_mm = adjusted_position * self.page_height
            
            # Ограничиваем диапазон
            offset_mm = max(self.min_offset, min(self.max_offset, offset_mm))
            
            folds.append((fold_type, offset_mm))
        
        return folds
    
    def calculate_statistics(self, pattern: List[Dict]) -> Dict:
        """Рассчитывает статистику паттерна"""
        if not pattern:
            return {
                'total_folds': 0,
                'pages_used': 0,
                'estimated_time_minutes': 0
            }
        
        total_folds = len(pattern)
        pages_used = len(set(fold['page'] for fold in pattern))
        
        # Время: сгиб угла быстрее чем полный сгиб - 20 секунд на сгиб
        estimated_time = math.ceil(total_folds * 0.33)
        
        return {
            'total_folds': total_folds,
            'pages_used': pages_used,
            'estimated_time_minutes': estimated_time
        }