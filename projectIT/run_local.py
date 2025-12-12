"""
Альтернативная версия с локальной моделью через transformers
Требует мощного ПК с видеокартой!
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LocalCharacterGenerator:
    def __init__(self):
        print("Загрузка модели...")
        # Можно использовать русскоязычные модели
        self.model_name = "IlyaGusev/rugpt3large_based_on_gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        if torch.cuda.is_available():
            self.model.cuda()
        
    def generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=500,
                temperature=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Пример использования
if __name__ == "__main__":
    generator = LocalCharacterGenerator()
    prompt = "Создай персонажа для D&D: "
    result = generator.generate(prompt)
    print(result)