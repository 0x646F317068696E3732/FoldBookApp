import math
from typing import List, Dict, Tuple

class DualFoldBookGenerator:
    """
    Генератор book folding с двумя сгибами на каждую страницу
    Формат выхода: Н(низ)26мм В50 - нижний сгиб от низа 26мм, верхний от верха 50мм
    """
    
    def __init__(self):
        self.min_offset = 5   # минимальный отступ
        self.max_offset = 50  # максимальный отступ
        
    def generate_pattern(self, text: str, book_pages: int, book_height: float) -> List[Dict]:
        """
        Генерирует паттерн с двумя сгибами на каждую страницу
        
        Args:
            text: Текст для преобразования
            book_pages: Общее количество страниц
            book_height: Высота страницы в мм
            
        Returns:
            Список с инструкциями: {"page": 1, "bottom_mm": 26, "top_mm": 50}
        """
        text = text.strip().upper()
        if not text:
            return []
            
        # Создаем растр текста
        raster = self._create_text_raster(text, book_height)
        
        # Преобразуем растр в инструкции
        return self._raster_to_folds(raster, book_pages, book_height)
    
    def _create_text_raster(self, text: str, book_height: float) -> List[List[int]]:
        """Создает двумерный растр текста"""
        # Высота растра пропорциональна количеству символов
        height = max(20, len(text) * 8)
        width = 60
        
        raster = [[0] * width for _ in range(height)]
        
        # Позиция для отрисовки символов
        x_pos = 5
        
        for char in text:
            if char == ' ':
                x_pos += 8
                continue
                
            char_pattern = self._get_character_pattern(char)
            char_width = len(char_pattern[0]) if char_pattern else 8
            
            # Отрисовываем символ в растр
            for y, row in enumerate(char_pattern):
                for dx, pixel in enumerate(row):
                    if pixel and x_pos + dx < width and y < height:
                        raster[y][x_pos + dx] = 1
            
            x_pos += char_width + 2
        
        return raster
    
    def _get_character_pattern(self, char: str) -> List[List[int]]:
        """Возвращает растровый паттерн символа"""
        patterns = {
            'A': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,1,1,1,1],
                [1,0,0,0,1],
                [1,0,0,0,1]
            ],
            'B': [
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,1,1,1,0]
            ],
            'C': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,0],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            'H': [
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,1],
                [1,0,0,0,1],
                [1,0,0,0,1]
            ],
            'I': [
                [1,1,1],
                [0,1,0],
                [0,1,0],
                [0,1,0],
                [1,1,1]
            ],
            'L': [
                [1,0,0,0],
                [1,0,0,0],
                [1,0,0,0],
                [1,0,0,0],
                [1,1,1,1]
            ],
            'O': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ]
        }
        
        return patterns.get(char, [
            [1,1,1],
            [1,0,1],
            [1,1,1],
            [1,0,1],
            [1,1,1]
        ])
    
    def _raster_to_folds(self, raster: List[List[int]], book_pages: int, book_height: float) -> List[Dict]:
        """
        Преобразует растр в инструкции сгибов
        Каждая страница получает два сгиба: нижний и верхний
        """
        folds = []
        
        # Количество страниц на строку растра
        pages_per_row = max(1, book_pages // len(raster))
        
        for i, row in enumerate(raster):
            if not any(row):  # Пустая строка
                continue
                
            # Находим границы текста в строке
            first_pixel = next((j for j, pixel in enumerate(row) if pixel), 0)
            last_pixel = next((len(row) - 1 - j for j, pixel in enumerate(reversed(row)) if pixel), len(row) - 1)
            
            # Рассчитываем отступы
            # Нижний сгиб - от левой границы текста
            bottom_offset = (first_pixel / len(row)) * (book_height * 0.8) + 10
            # Верхний сгиб - от правой границы текста  
            top_offset = ((len(row) - last_pixel - 1) / len(row)) * (book_height * 0.8) + 10
            
            # Ограничиваем отступы
            bottom_offset = max(self.min_offset, min(self.max_offset, bottom_offset))
            top_offset = max(self.min_offset, min(self.max_offset, top_offset))
            
            # Генерируем страницы для этой строки
            page_start = i * pages_per_row + 1
            page_end = min((i + 1) * pages_per_row, book_pages)
            
            for page in range(page_start, page_end + 1):
                folds.append({
                    "page": page,
                    "bottom_mm": round(bottom_offset, 1),
                    "top_mm": round(top_offset, 1)
                })
        
        return folds