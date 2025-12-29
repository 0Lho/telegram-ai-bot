"""
Умный ИИ с доступом к Wikipedia и решением математических задач
"""

import re
import math
import sympy
import wikipediaapi
from typing import Dict, Optional, Tuple

class SmartAI:
    """Умный ИИ с официальными источниками"""
    
    def __init__(self):
        print("🧠 Инициализация умного ИИ...")
        
        # Wikipedia API
        self.wiki = wikipediaapi.Wikipedia(
            language='ru',
            user_agent='TelegramAI/1.0'
        )
        
        # Кэш запросов
        self.cache = {}
        
        print("✅ Умный ИИ готов (Wikipedia + математика)")
    
    def get_answer(self, question: str) -> str:
        """Получение ответа с источниками"""
        
        # Проверяем кэш
        if question in self.cache:
            return self.cache[question]
        
        # Определяем тип запроса
        if self._is_math_problem(question):
            answer = self._solve_math(question)
        
        elif self._is_wikipedia_query(question):
            answer = self._search_wikipedia(question)
        
        else:
            answer = self._general_response(question)
        
        # Сохраняем в кэш
        self.cache[question] = answer
        return answer
    
    def _is_math_problem(self, text: str) -> bool:
        """Определение математической задачи"""
        math_keywords = [
            'сколько будет', 'реши', 'посчитай', 'вычисли',
            'уравнение', 'равно', '=', '+', '-', '*', '/', '^',
            'квадрат', 'корень', 'производная', 'интеграл',
            'sin', 'cos', 'tg', 'ctg', 'логарифм'
        ]
        return any(keyword in text.lower() for keyword in math_keywords)
    
    def _is_wikipedia_query(self, text: str) -> bool:
        """Определение запроса для Wikipedia"""
        wiki_keywords = [
            'что такое', 'кто такой', 'кто такая',
            'определение', 'это', 'расскажи о',
            'информация о', 'статья о', 'википедия'
        ]
        return any(keyword in text.lower() for keyword in wiki_keywords)
    
    def _solve_math(self, problem: str) -> str:
        """Решение математических задач"""
        try:
            # Простые вычисления
            if 'сколько будет' in problem.lower():
                expression = self._extract_expression(problem)
                if expression:
                    result = self._calculate_expression(expression)
                    return f"🧮 **Решение:**\n\n`{expression} = {result}`"
            
            # Уравнения
            elif 'уравнение' in problem.lower():
                solution = self._solve_equation(problem)
                if solution:
                    return f"📐 **Решение уравнения:**\n\n{solution}"
            
            # Квадрат/корень
            elif any(word in problem.lower() for word in ['квадрат', 'корень']):
                solution = self._solve_power_root(problem)
                if solution:
                    return f"🔢 **Решение:**\n\n{solution}"
            
            # Тригонометрия
            elif any(word in problem.lower() for word in ['sin', 'cos', 'tg', 'ctg']):
                solution = self._solve_trigonometry(problem)
                if solution:
                    return f"📐 **Тригонометрия:**\n\n{solution}"
            
            # По умолчанию
            return "🧮 Для решения математической задачи уточните:\n- Конкретное выражение\n- Уравнение\n- Тип вычисления"
            
        except Exception as e:
            return f"❌ Ошибка решения: {str(e)}"
    
    def _extract_expression(self, text: str) -> Optional[str]:
        """Извлечение математического выражения"""
        patterns = [
            r'сколько будет\s+([^?]+)',
            r'посчитай\s+([^\.]+)',
            r'вычисли\s+([^\.]+)',
            r'([\d\s\+\-\*\/\^\(\)\.]+)='
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                expr = match.group(1).strip()
                # Заменяем слова на операторы
                expr = expr.replace(' плюс ', '+').replace(' минус ', '-')
                expr = expr.replace(' умножить на ', '*').replace(' разделить на ', '/')
                return expr
        
        # Ищем просто выражение
        math_expr = re.search(r'([\d\+\-\*\/\^\(\)\.\s]+)', text)
        return math_expr.group(1).strip() if math_expr else None
    
    def _calculate_expression(self, expression: str):
        """Вычисление выражения"""
        # Безопасный eval
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Недопустимые символы в выражении")
        
        # Заменяем ^ на **
        expression = expression.replace('^', '**')
        
        # Вычисляем
        return eval(expression, {"__builtins__": {}}, {"math": math})
    
    def _solve_equation(self, problem: str) -> Optional[str]:
        """Решение уравнений"""
        try:
            # Простые линейные уравнения
            if 'x' in problem.lower():
                # Пример: 2x + 5 = 15
                numbers = re.findall(r'\d+', problem)
                if len(numbers) >= 3:
                    a, b, c = map(int, numbers[:3])
                    x = (c - b) / a
                    return f"2x + 5 = 15\nx = ({c} - {b}) / {a} = {x}"
            
            # Квадратные уравнения
            elif 'x^2' in problem.lower() or 'x²' in problem.lower():
                return "📊 Для квадратного уравнения используйте формулу:\nax² + bx + c = 0\nx = [-b ± √(b² - 4ac)] / 2a"
            
        except:
            pass
        return None
    
    def _solve_power_root(self, problem: str) -> Optional[str]:
        """Решение степеней и корней"""
        numbers = re.findall(r'\d+', problem)
        if numbers:
            num = int(numbers[0])
            
            if 'квадрат' in problem.lower():
                return f"Квадрат {num} = {num ** 2}"
            
            elif 'корень' in problem.lower():
                if 'квадратн' in problem.lower():
                    return f"√{num} = {math.sqrt(num):.2f}"
                elif 'кубическ' in problem.lower():
                    return f"³√{num} = {num ** (1/3):.2f}"
        
        return None
    
    def _solve_trigonometry(self, problem: str) -> Optional[str]:
        """Решение тригонометрии"""
        numbers = re.findall(r'\d+', problem)
        if numbers:
            angle = int(numbers[0])
            rad = math.radians(angle)
            
            if 'sin' in problem.lower():
                return f"sin({angle}°) = {math.sin(rad):.4f}"
            elif 'cos' in problem.lower():
                return f"cos({angle}°) = {math.cos(rad):.4f}"
            elif 'tg' in problem.lower() or 'tan' in problem.lower():
                return f"tg({angle}°) = {math.tan(rad):.4f}"
            elif 'ctg' in problem.lower() or 'cot' in problem.lower():
                return f"ctg({angle}°) = {1/math.tan(rad):.4f}"
        
        return None
    
    def _search_wikipedia(self, query: str) -> str:
        """Поиск в Wikipedia"""
        try:
            # Очищаем запрос
            clean_query = query.lower()
            for word in ['что такое', 'кто такой', 'кто такая', 'расскажи о', 'определение']:
                clean_query = clean_query.replace(word, '').strip()
            
            # Ищем страницу
            page = self.wiki.page(clean_query)
            
            if page.exists():
                # Получаем первые 500 символов
                summary = page.summary[:500] + "..."
                
                # Формируем ответ
                response = f"📚 **{page.title}**\n\n"
                response += f"{summary}\n\n"
                response += f"🔗 Источник: [Wikipedia]({page.fullurl})"
                
                return response
            else:
                # Поиск похожих статей
                search_results = self.wiki.search(clean_query)
                if search_results:
                    suggestions = "\n".join([f"• {r}" for r in search_results[:3]])
                    return f"📖 По запросу '{clean_query}' не найдено статьи.\n\nВозможно вы имели в виду:\n{suggestions}"
                else:
                    return f"🔍 По запросу '{clean_query}' ничего не найдено в Wikipedia."
        
        except Exception as e:
            return f"❌ Ошибка поиска: {str(e)}"
    
    def _general_response(self, question: str) -> str:
        """Общий ответ"""
        responses = [
            f"🤔 Запрос: '{question}'\n\nМогу помочь с:\n• Математическими задачами\n• Поиском в Wikipedia\n• Определениями и фактами",
            f"📝 '{question}'\n\nУточните - нужно решение математики или информация из Wikipedia?",
            f"💡 '{question}'\n\nДля ответа укажите:\n• Конкретную задачу\n• Что найти в Wikipedia"
        ]
        
        import random
        return random.choice(responses)

# Глобальный экземпляр
smart_ai = SmartAI()

# Тестирование
if __name__ == "__main__":
    print("🧪 Тестирование ИИ...")
    
    tests = [
        "сколько будет 2+2*2",
        "что такое Python",
        "кто такой Альберт Эйнштейн",
        "реши уравнение 2x + 5 = 15",
        "квадрат 5",
        "корень из 16"
    ]
    
    for test in tests:
        print(f"\n{'='*50}")
        print(f"📝 Вопрос: {test}")
        answer = smart_ai.get_answer(test)
        print(f"✅ Ответ: {answer[:100]}...")