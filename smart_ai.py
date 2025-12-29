"""
Умный ИИ с доступом к Wikipedia и решением математических задач
"""

import re
import math
from typing import Dict, Optional, Tuple
import requests

class SmartAI:
    """Умный ИИ с официальными источниками"""
    
    def __init__(self):
        print("🧠 Инициализация умного ИИ...")
        
        # Wikipedia через requests (проще и надежнее)
        self.wikipedia_url = "https://ru.wikipedia.org/w/api.php"
        
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
            'квадрат', 'корень', 'синус', 'косинус', 'тангенс',
            'логарифм', 'процент', 'степень', 'модуль'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in math_keywords)
    
    def _is_wikipedia_query(self, text: str) -> bool:
        """Определение запроса для Wikipedia"""
        wiki_keywords = [
            'что такое', 'кто такой', 'кто такая',
            'определение', 'это', 'расскажи о',
            'информация о', 'статья о', 'википедия'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in wiki_keywords)
    
    def _solve_math(self, problem: str) -> str:
        """Решение математических задач"""
        try:
            problem_lower = problem.lower()
            
            # Простые вычисления
            if 'сколько будет' in problem_lower:
                expression = self._extract_expression(problem)
                if expression:
                    result = self._calculate_expression(expression)
                    return f"🧮 **Решение:**\n\n`{expression} = {result}`"
            
            # Уравнения
            elif 'уравнение' in problem_lower or 'x=' in problem_lower:
                solution = self._solve_equation(problem)
                if solution:
                    return f"📐 **Решение уравнения:**\n\n{solution}"
                else:
                    return "📐 *Решение уравнений:*\n\nНапишите уравнение в формате:\n`2x + 5 = 15` или `x^2 - 4 = 0`"
            
            # Квадрат/корень
            elif any(word in problem_lower for word in ['квадрат', 'корень', '√']):
                solution = self._solve_power_root(problem)
                if solution:
                    return f"🔢 **Решение:**\n\n{solution}"
                else:
                    return "🔢 *Степени и корни:*\n\nПримеры:\n• квадрат 5\n• корень из 16\n• 2 в степени 3"
            
            # Проценты
            elif 'процент' in problem_lower or '%' in problem_lower:
                solution = self._solve_percentage(problem)
                if solution:
                    return f"📊 **Проценты:**\n\n{solution}"
                else:
                    return "📊 *Проценты:*\n\nПример:\n`15% от 200` или `сколько процентов составляет 30 от 150?`"
            
            # Тригонометрия
            elif any(word in problem_lower for word in ['sin', 'cos', 'tg', 'ctg', 'синус', 'косинус', 'тангенс']):
                solution = self._solve_trigonometry(problem)
                if solution:
                    return f"📐 **Тригонометрия:**\n\n{solution}"
                else:
                    return "📐 *Тригонометрия:*\n\nПримеры:\n• sin 30\n• cos 45\n• tg 60"
            
            # Общий математический запрос
            else:
                expression = self._extract_expression(problem)
                if expression:
                    result = self._calculate_expression(expression)
                    return f"🧮 **Решение:**\n\n`{expression} = {result}`"
                else:
                    return "🧮 *Математическая помощь:*\n\nУточните:\n• Конкретное выражение\n• Тип задачи\n• Пример"
            
        except Exception as e:
            return f"❌ Ошибка решения: {str(e)}\n\nПопробуйте сформулировать иначе."
    
    def _extract_expression(self, text: str) -> Optional[str]:
        """Извлечение математического выражения"""
        patterns = [
            r'сколько будет\s+([^?]+)',
            r'посчитай\s+([^\.]+)',
            r'вычисли\s+([^\.]+)',
            r'([\d\s\+\-\*\/\^\(\)\.]+)=?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                expr = match.group(1).strip()
                # Заменяем слова на операторы
                expr = expr.replace(' плюс ', '+').replace(' минус ', '-')
                expr = expr.replace(' умножить на ', '*').replace(' умножить ', '*')
                expr = expr.replace(' разделить на ', '/').replace(' разделить ', '/')
                expr = expr.replace(' на ', '/')  # "делить на"
                return expr
        
        # Ищем просто выражение
        math_expr = re.search(r'([\d\+\-\*\/\^\(\)\.\s]+)', text)
        return math_expr.group(1).strip() if math_expr else None
    
    def _calculate_expression(self, expression: str) -> str:
        """Вычисление выражения"""
        try:
            # Безопасная проверка
            allowed_chars = set('0123456789+-*/.()^ ')
            expr_clean = expression.replace(' ', '')
            
            if not all(c in allowed_chars for c in expr_clean):
                raise ValueError("Недопустимые символы")
            
            # Заменяем ^ на **
            expression = expression.replace('^', '**')
            
            # Вычисляем
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            
            # Если получилось целое число, убираем .0
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            return str(result)
            
        except Exception as e:
            return f"Ошибка вычисления: {e}"
    
    def _solve_equation(self, problem: str) -> Optional[str]:
        """Решение уравнений"""
        try:
            # Простые линейные уравнения типа 2x + 5 = 15
            if 'x' in problem.lower():
                # Упрощаем: 2x + 5 = 15 -> 2x = 10 -> x = 5
                nums = re.findall(r'[-+]?\d*\.?\d+', problem)
                if len(nums) >= 3:
                    # Простейший случай: ax + b = c
                    a = float(nums[0]) if nums[0] else 1
                    b = float(nums[1]) if len(nums) > 1 else 0
                    c = float(nums[2]) if len(nums) > 2 else 0
                    
                    if a != 0:
                        x = (c - b) / a
                        return f"Уравнение: {problem}\nРешение: x = ({c} - {b}) / {a} = {x}"
        
        except:
            pass
        
        return None
    
    def _solve_power_root(self, problem: str) -> Optional[str]:
        """Решение степеней и корней"""
        try:
            nums = re.findall(r'\d+', problem)
            if nums:
                num = float(nums[0])
                
                if 'квадрат' in problem.lower():
                    return f"Квадрат числа {num} = {num ** 2}"
                
                elif 'корень' in problem.lower() or '√' in problem:
                    if 'кубич' in problem.lower():
                        return f"Кубический корень из {num} = {num ** (1/3):.4f}"
                    else:
                        return f"Квадратный корень из {num} = {math.sqrt(num):.4f}"
                
                elif 'степень' in problem.lower() or '^' in problem:
                    if len(nums) >= 2:
                        base, exp = float(nums[0]), float(nums[1])
                        return f"{base} в степени {exp} = {base ** exp}"
        
        except:
            pass
        
        return None
    
    def _solve_percentage(self, problem: str) -> Optional[str]:
        """Решение процентных задач"""
        try:
            # 15% от 200
            match = re.search(r'(\d+)%\s*от\s*(\d+)', problem, re.IGNORECASE)
            if match:
                percent, number = map(float, match.groups())
                result = (percent / 100) * number
                return f"{percent}% от {number} = {result}"
            
            # сколько процентов составляет 30 от 150
            match = re.search(r'сколько процентов составляет (\d+)\s*от\s*(\d+)', problem, re.IGNORECASE)
            if match:
                part, whole = map(float, match.groups())
                if whole != 0:
                    percent = (part / whole) * 100
                    return f"{part} от {whole} = {percent:.1f}%"
        
        except:
            pass
        
        return None
    
    def _solve_trigonometry(self, problem: str) -> Optional[str]:
        """Решение тригонометрии"""
        try:
            nums = re.findall(r'\d+', problem)
            if nums:
                angle = float(nums[0])
                rad = math.radians(angle)
                
                if 'sin' in problem.lower() or 'синус' in problem.lower():
                    return f"sin({angle}°) = {math.sin(rad):.4f}"
                elif 'cos' in problem.lower() or 'косинус' in problem.lower():
                    return f"cos({angle}°) = {math.cos(rad):.4f}"
                elif 'tg' in problem.lower() or 'tan' in problem.lower() or 'тангенс' in problem.lower():
                    return f"tg({angle}°) = {math.tan(rad):.4f}"
        
        except:
            pass
        
        return None
    
    def _search_wikipedia(self, query: str) -> str:
        """Поиск в Wikipedia через API"""
        try:
            # Очищаем запрос
            clean_query = query.lower()
            for word in ['что такое', 'кто такой', 'кто такая', 'расскажи о', 'определение']:
                clean_query = clean_query.replace(word, '').strip()
            
            if not clean_query:
                return "📚 *Wikipedia поиск:*\n\nУкажите, что найти:\n• что такое [термин]\n• кто такой [имя]\n• информация о [тема]"
            
            # API запрос к Wikipedia
            params = {
                'action': 'query',
                'format': 'json',
                'titles': clean_query,
                'prop': 'extracts|info',
                'exintro': True,
                'explaintext': True,
                'inprop': 'url',
                'redirects': True,
            }
            
            response = requests.get(self.wikipedia_url, params=params, timeout=10)
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Страница найдена
                    title = page_data.get('title', '')
                    extract = page_data.get('extract', '')
                    url = f"https://ru.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    
                    if extract:
                        # Берем первые 400 символов
                        summary = extract[:400].strip()
                        if len(extract) > 400:
                            summary += "..."
                        
                        return f"📚 **{title}**\n\n{summary}\n\n🔗 [Читать далее на Wikipedia]({url})"
                    else:
                        return f"📚 **{title}**\n\nСтатья найдена, но без описания.\n🔗 [Wikipedia]({url})"
            
            # Если не найдено
            return f"🔍 По запросу '{clean_query}' ничего не найдено в Wikipedia.\n\nПопробуйте:\n• Другие формулировки\n• Английские термины\n• Более общие запросы"
        
        except requests.exceptions.Timeout:
            return "⏰ Wikipedia не отвечает. Попробуйте позже."
        except Exception as e:
            return f"❌ Ошибка поиска: {str(e)}"
    
    def _general_response(self, question: str) -> str:
        """Общий ответ"""
        import random
        
        responses = [
            f"🤔 *Ваш запрос:* '{question}'\n\n*Я могу помочь с:*\n• Математическими задачами\n• Поиском в Wikipedia\n• Вычислениями и формулами\n\n*Примеры:*\n• сколько будет 15% от 200\n• что такое искусственный интеллект\n• sin 30 градусов",
            f"📝 *Запрос:* '{question}'\n\nУточните, что нужно:\n• **Математика**: решение, вычисление\n• **Информация**: определение, факты\n• **Объяснение**: как работает, что значит",
            f"💡 *'{question}'*\n\nДля лучшего ответа:\n1. Математика → напишите выражение\n2. Wikipedia → 'что такое [термин]'\n3. Помощь → конкретный вопрос"
        ]
        
        return random.choice(responses)

# Глобальный экземпляр
smart_ai = SmartAI()
