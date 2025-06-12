# recipe_engine.py

from collections import defaultdict
from models.elements import Element
from models.rune_circle import RuneCircle
from typing import Dict
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

DEFAULT_WEIGHT = 1.0

# Загрузка переменных окружения из .env файла
load_dotenv()
client = OpenAI(api_key=os.getenv("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"))

class Recipe:
    def __init__(self):
        self.components = defaultdict(float)
        self._cached_description = None

    def add(self, element: Element, amount: float = 1.0):
        self.components[element] += amount

    def normalize(self):
        total = sum(self.components.values())
        if total == 0:
            return {el: 0.0 for el in self.components}
        return {el: round(val / total, 3) for el, val in self.components.items()}

    def summary(self):
        return {el.name: round(amt, 2) for el, amt in self.components.items()}

    def vector(self):
        return self.normalize()

    def to_prompt(self):
        norm = self.normalize()
        sorted_elements = sorted(norm.items(), key=lambda x: -x[1])
        parts = [f"{el.name} {int(weight * 100)}%" for el, weight in sorted_elements if weight > 0.01]
        return ", ".join(parts)

    def describe(self, max_tokens: int = 300, temperature: float = 0.7) -> Dict[str, str]:
        """
        Генерирует описание заклинания через OpenAI ChatGPT на основе пропорций элементов.
        Использует кэш, чтобы не отправлять одинаковый запрос повторно.
        Возвращает словарь с ключами: Название, Эффект, Редкость, Пропорции или Ошибка.
        """
        if self._cached_description:
            return self._cached_description

        prompt = (
            f"Ты — мудрый маг. Придумай магическое заклинание на основе стихий.\n"
            f"Пропорции: {self.to_prompt()}\n"
            f"Выведи результат строго в формате:\n"
            f"Название: ...\nЭффект: ...\nРедкость: ...\n"
            f"Никакого другого текста, только три строки в указанном формате."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ты выдающийся магический алхимик и мастер составления заклинаний."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            result = response.choices[0].message.content.strip()

            # Отладочный вывод результата
            print("[DEBUG] Ответ от OpenAI:\n", result)

            name_match = re.search(r"(?i)название\s*[:\-]\s*(.*)", result)
            effect_match = re.search(r"(?i)эффект\s*[:\-]\s*(.*)", result)
            rarity_match = re.search(r"(?i)редкость\s*[:\-]\s*(.*)", result)

            name = name_match.group(1).strip() if name_match else None
            if not name:
                lines = result.splitlines()
                if lines:
                    name_guess = lines[0].strip()
                    if len(name_guess.split()) <= 8:
                        name = name_guess

            if not (name or effect_match or rarity_match):
                raise ValueError("Ответ не соответствует ожидаемому формату")

            self._cached_description = {
                "Название": name if name else "Неизвестно",
                "Эффект": effect_match.group(1).strip() if effect_match else result,
                "Редкость": rarity_match.group(1).strip() if rarity_match else "Неизвестно",
                "Пропорции": self.to_prompt(),
            }
            return self._cached_description

        except Exception as e:
            self._cached_description = {
                "Ошибка": str(e),
                "Название": "Ошибка",
                "Эффект": str(e),
                "Редкость": "-",
                "Пропорции": self.to_prompt()
            }
            return self._cached_description


def build_recipe_from_circle(circle: RuneCircle) -> Recipe:
    recipe = Recipe()

    if circle.core:
        recipe.add(circle.core.element, 2.0)

    for level, sigils in circle.layers.items():
        for sigil in sigils:
            if sigil:
                level_weight = 1.0 / (level + 1)
                recipe.add(sigil.element, level_weight)

    return recipe