"""
Генератор персонажей для D&D с использованием нейросети
Красивая русскоязычная версия с цветовой палитрой
"""

import json
import random
import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime

# Конфигурация программы
CONFIG = {
    "api_key": "sk-EUEqzbLI3UY4XLcFR3f5jQ",
    "api_url": "https://litellm.tokengate.ru/v1/chat/completions",
    "model": "gpt-4",
    "save_folder": "Персонажи"
}

class DnDCharacterGenerator:
    """Класс для генерации персонажей D&D"""
    
    def __init__(self, root):
        """Инициализация главного окна"""
        self.root = root
        self.root.title("Кузница Мастера Подземелий v3.0")
        self.root.geometry("1300x800")
        
        # Настраиваем цветовую палитру
        self.colors = {
            'bg_main': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_cards': '#0f3460',
            'bg_input': '#2d4059',
            'accent_primary': '#e94560',
            'accent_secondary': '#533483',
            'accent_success': '#00b894',
            'accent_warning': '#fdcb6e',
            'accent_error': '#d63031',
            'accent_info': '#74b9ff',
            'text_primary': '#ffffff',
            'text_secondary': '#dfe6e9',
            'text_muted': '#b2bec3',
            'border': '#636e72',
            'highlight': '#a29bfe'
        }
        
        # Настраиваем фон главного окна
        self.root.configure(bg=self.colors['bg_main'])
        
        # Создаем папку для сохранения
        os.makedirs(CONFIG["save_folder"], exist_ok=True)
        
        # Данные персонажа
        self.character_data = {}
        
        # Создаем интерфейс
        self.setup_ui()
    
    def create_card_frame(self, parent, padx=15, pady=15):
        """Создает стандартную карточку с рамкой"""
        return tk.Frame(
            parent,
            bg=self.colors['bg_cards'],
            highlightbackground=self.colors['border'],
            highlightthickness=1,
            padx=padx,
            pady=pady
        )
    
    def create_label(self, parent, text, font_size=10, is_bold=False, fg_color=None, bg_color=None):
        """Создает метку с единым стилем"""
        font = ('Segoe UI', font_size, 'bold' if is_bold else 'normal')
        fg = fg_color or self.colors['text_primary']
        bg = bg_color or self.colors['bg_secondary']
        
        return tk.Label(
            parent,
            text=text,
            font=font,
            bg=bg,
            fg=fg
        )
    
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'], padx=15, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель управления
        self.create_control_panel(main_container)
        
        # Правая панель результатов
        self.create_result_panel(main_container)
    
    def create_control_panel(self, parent):
        """Создание панели управления"""
        control_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], padx=20, pady=20)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 15))
        
        # Заголовок приложения
        title = self.create_label(control_frame, "КУЗНИЦА МАСТЕРА\nПОДЗЕМЕЛИЙ", 16, True, self.colors['accent_primary'])
        title.pack(pady=(0, 20))
        
        # Разделитель
        self.create_separator(control_frame)
        
        # Способ создания
        self.create_creation_section(control_frame)
        
        # Описание персонажа
        self.create_description_section(control_frame)
        
        # Настройки
        self.create_settings_section(control_frame)
        
        # Кнопки действий
        self.create_action_buttons(control_frame)
    
    def create_separator(self, parent):
        """Создает разделительную линию"""
        sep = tk.Frame(parent, height=2, bg=self.colors['border'])
        sep.pack(fill=tk.X, pady=10)
        return sep
    
    def create_creation_section(self, parent):
        """Создает секцию выбора способа создания"""
        section = tk.Frame(parent, bg=self.colors['bg_secondary'])
        section.pack(fill=tk.X, pady=(0, 20))
        
        title = self.create_label(section, "Способ создания:", 11, True, self.colors['accent_info'])
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Радиокнопки
        self.creation_mode = tk.StringVar(value="random")
        
        # Случайный герой
        random_frame = tk.Frame(section, bg=self.colors['bg_secondary'])
        random_frame.pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            random_frame,
            text="Случайный герой",
            variable=self.creation_mode,
            value="random",
            font=('Segoe UI', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            selectcolor=self.colors['bg_secondary']
        ).pack(side=tk.LEFT)
        
        tk.Label(random_frame, text="🎲", font=('Segoe UI', 14),
                bg=self.colors['bg_secondary'], fg=self.colors['accent_warning']).pack(side=tk.LEFT, padx=(5, 0))
        
        # По описанию
        manual_frame = tk.Frame(section, bg=self.colors['bg_secondary'])
        manual_frame.pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            manual_frame,
            text="По моему описанию",
            variable=self.creation_mode,
            value="manual",
            font=('Segoe UI', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            selectcolor=self.colors['bg_secondary']
        ).pack(side=tk.LEFT)
        
        tk.Label(manual_frame, text="✍️", font=('Segoe UI', 14),
                bg=self.colors['bg_secondary'], fg=self.colors['accent_success']).pack(side=tk.LEFT, padx=(5, 0))
        
        self.create_separator(parent)
    
    def create_description_section(self, parent):
        """Создает секцию описания персонажа"""
        section = tk.Frame(parent, bg=self.colors['bg_secondary'])
        section.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        title = self.create_label(section, "Описание персонажа:", 11, True, self.colors['accent_info'])
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Текстовое поле
        text_frame = tk.Frame(section, bg=self.colors['bg_input'])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.description_text = tk.Text(
            text_frame,
            height=8,
            font=('Segoe UI', 10),
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            relief='flat',
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.description_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.description_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.description_text.config(yscrollcommand=scrollbar.set)
        
        # Пример текста
        example = "Например: Молодой дворф-варвар из северных горных кланов. Невероятно сильный, честный до фанатизма, но вспыльчивый."
        self.description_text.insert("1.0", example)
        
        self.create_separator(parent)
    
    def create_settings_section(self, parent):
        """Создает секцию настроек"""
        section = tk.Frame(parent, bg=self.colors['bg_secondary'])
        section.pack(fill=tk.X, pady=(0, 20))
        
        title = self.create_label(section, "Настройки генерации:", 11, True, self.colors['accent_info'])
        title.pack(anchor=tk.W, pady=(0, 15))
        
        # Игровая система
        grid = tk.Frame(section, bg=self.colors['bg_secondary'])
        grid.pack(fill=tk.X)
        
        self.create_label(grid, "Игровая система:", 10, False, self.colors['text_primary']).grid(row=0, column=0, sticky=tk.W, pady=8)
        
        self.game_system = ttk.Combobox(
            grid,
            values=["D&D 5e", "Pathfinder 2e", "Warhammer Fantasy"],
            state="readonly",
            width=22,
            font=('Segoe UI', 10)
        )
        self.game_system.current(0)
        self.game_system.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        # Уровень персонажа
        self.create_label(grid, "Уровень персонажа:", 10, False, self.colors['text_primary']).grid(row=1, column=0, sticky=tk.W, pady=8)
        
        level_frame = tk.Frame(grid, bg=self.colors['bg_secondary'])
        level_frame.grid(row=1, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        self.level_var = tk.IntVar(value=5)
        
        tk.Label(level_frame, text="1", font=('Segoe UI', 9),
                bg=self.colors['bg_secondary'], fg=self.colors['text_muted']).pack(side=tk.LEFT)
        
        tk.Scale(
            level_frame,
            from_=1,
            to=20,
            variable=self.level_var,
            orient=tk.HORIZONTAL,
            length=150,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            troughcolor=self.colors['bg_input']
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(level_frame, text="20", font=('Segoe UI', 9),
                bg=self.colors['bg_secondary'], fg=self.colors['text_muted']).pack(side=tk.LEFT)
        
        tk.Label(level_frame, textvariable=self.level_var, font=('Segoe UI', 11, 'bold'),
                bg=self.colors['bg_secondary'], fg=self.colors['accent_primary']).pack(side=tk.LEFT, padx=(10, 0))
        
        self.create_separator(parent)
    
    def create_action_buttons(self, parent):
        """Создает кнопки действий"""
        section = tk.Frame(parent, bg=self.colors['bg_secondary'])
        section.pack(fill=tk.X)
        
        # Кнопка генерации
        self.generate_btn = tk.Button(
            section,
            text="СОЗДАТЬ ПЕРСОНАЖА",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent_primary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_secondary'],
            activeforeground=self.colors['text_primary'],
            relief='flat',
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.generate_character
        )
        self.generate_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопка сохранения
        self.save_btn = tk.Button(
            section,
            text="СОХРАНИТЬ В ФАЙЛ",
            font=('Segoe UI', 10),
            bg=self.colors['accent_secondary'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['highlight'],
            activeforeground=self.colors['text_primary'],
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled',
            command=self.save_character
        )
        self.save_btn.pack(fill=tk.X)
        
        # Статус
        self.status_label = self.create_label(parent, "Готов к созданию персонажа", 9, False, self.colors['accent_success'])
        self.status_label.pack(pady=(15, 0))
    
    def create_result_panel(self, parent):
        """Создание панели результатов"""
        result_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], padx=15, pady=15)
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Вкладки
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Создаем вкладки
        self.create_basic_tab()
        self.create_stats_tab()
        self.create_inventory_tab()
        self.create_bio_tab()
    
    def create_basic_tab(self):
        """Создает вкладку с основной информацией"""
        self.tab_basic = tk.Frame(self.notebook, bg=self.colors['bg_secondary'], padx=15, pady=15)
        self.notebook.add(self.tab_basic, text="Основная информация")
        
        # Заголовок
        self.character_header = self.create_label(self.tab_basic, "Ваш персонаж появится здесь", 18, True, self.colors['accent_primary'])
        self.character_header.pack(pady=(10, 25))
        
        # Сетка карточек
        self.info_grid = tk.Frame(self.tab_basic, bg=self.colors['bg_secondary'])
        self.info_grid.pack(fill=tk.BOTH, expand=True)
        
        # Данные для карточек
        cards_data = [
            ("Раса", "race", "Неизвестно", "👤"),
            ("Класс", "class", "Неизвестно", "⚔️"),
            ("Уровень", "level", "1", "📈"),
            ("Предыстория", "background", "Неизвестно", "🏰"),
            ("Мировоззрение", "alignment", "Неизвестно", "⚖️"),
            ("Возраст", "age", "Неизвестно", "🎂")
        ]
        
        self.cards = {}
        for i, (title, key, default, icon) in enumerate(cards_data):
            card = self.create_card_frame(self.info_grid)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            # Иконка и заголовок
            header = tk.Frame(card, bg=self.colors['bg_cards'])
            header.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(header, text=icon, font=('Segoe UI', 16),
                    bg=self.colors['bg_cards'], fg=self.colors['accent_warning']).pack(side=tk.LEFT)
            
            tk.Label(header, text=title, font=('Segoe UI', 11, 'bold'),
                    bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=(8, 0))
            
            # Значение
            value_label = tk.Label(
                card,
                text=default,
                font=('Segoe UI', 12),
                bg=self.colors['bg_cards'],
                fg=self.colors['text_secondary'],
                wraplength=180,
                justify=tk.CENTER
            )
            value_label.pack(fill=tk.BOTH, expand=True)
            
            self.cards[key] = value_label
        
        # Настройка сетки
        for i in range(2):
            self.info_grid.columnconfigure(i, weight=1)
        for i in range(3):
            self.info_grid.rowconfigure(i, weight=1)
    
    def create_stats_tab(self):
        """Создает вкладку с характеристиками"""
        self.tab_stats = tk.Frame(self.notebook, bg=self.colors['bg_secondary'], padx=15, pady=15)
        self.notebook.add(self.tab_stats, text="Характеристики")
        
        # Заголовок
        title = self.create_label(self.tab_stats, "ХАРАКТЕРИСТИКИ ПЕРСОНАЖА", 16, True, self.colors['accent_info'])
        title.pack(pady=(0, 25))
        
        # Сетка характеристик
        self.stats_grid = tk.Frame(self.tab_stats, bg=self.colors['bg_secondary'])
        self.stats_grid.pack(fill=tk.BOTH, expand=True)
        
        # Данные характеристик
        stats_data = [
            ("СИЛА", "strength", "Физическая мощь", "💪"),
            ("ЛОВКОСТЬ", "dexterity", "Координация и реакция", "🏃"),
            ("ТЕЛОСЛОЖЕНИЕ", "constitution", "Выносливость и здоровье", "❤️"),
            ("ИНТЕЛЛЕКТ", "intelligence", "Память и логика", "🧠"),
            ("МУДРОСТЬ", "wisdom", "Интуиция и восприятие", "👁️"),
            ("ХАРИЗМА", "charisma", "Обаяние и лидерство", "🎭")
        ]
        
        self.stat_widgets = {}
        for i, (title_text, key, desc, icon) in enumerate(stats_data):
            card = self.create_card_frame(self.stats_grid)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            # Заголовок
            header = tk.Frame(card, bg=self.colors['bg_cards'])
            header.pack(fill=tk.X, pady=(0, 15))
            
            tk.Label(header, text=icon, font=('Segoe UI', 20),
                    bg=self.colors['bg_cards'], fg=self.colors['accent_warning']).pack(side=tk.LEFT)
            
            tk.Label(header, text=title_text, font=('Segoe UI', 12, 'bold'),
                    bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=(10, 0))
            
            # Значение
            value_frame = tk.Frame(card, bg=self.colors['bg_cards'])
            value_frame.pack(pady=(0, 10))
            
            tk.Label(value_frame, text="Значение:", font=('Segoe UI', 9),
                    bg=self.colors['bg_cards'], fg=self.colors['text_muted']).pack()
            
            stat_value = tk.Label(value_frame, text="10", font=('Segoe UI', 28, 'bold'),
                                bg=self.colors['bg_cards'], fg=self.colors['accent_primary'])
            stat_value.pack()
            
            # Модификатор
            mod_frame = tk.Frame(card, bg=self.colors['bg_cards'])
            mod_frame.pack()
            
            tk.Label(mod_frame, text="Модификатор:", font=('Segoe UI', 9),
                    bg=self.colors['bg_cards'], fg=self.colors['text_muted']).pack()
            
            mod_value = tk.Label(mod_frame, text="+0", font=('Segoe UI', 20, 'bold'),
                               bg=self.colors['bg_cards'], fg=self.colors['accent_success'])
            mod_value.pack()
            
            # Описание
            tk.Label(card, text=desc, font=('Segoe UI', 8),
                    bg=self.colors['bg_cards'], fg=self.colors['text_muted'],
                    wraplength=160, justify=tk.CENTER).pack(pady=(15, 0))
            
            self.stat_widgets[key] = {'value': stat_value, 'modifier': mod_value}
        
        # Настройка сетки
        for i in range(3):
            self.stats_grid.columnconfigure(i, weight=1)
        for i in range(2):
            self.stats_grid.rowconfigure(i, weight=1)
    
    def create_inventory_tab(self):
        """Создает вкладку с инвентарем"""
        self.tab_inventory = tk.Frame(self.notebook, bg=self.colors['bg_secondary'])
        self.notebook.add(self.tab_inventory, text="Инвентарь")
        
        container = tk.Frame(self.tab_inventory, bg=self.colors['bg_secondary'], padx=15, pady=15)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Левая колонка
        left = tk.Frame(container, bg=self.colors['bg_secondary'])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Правая колонка
        right = tk.Frame(container, bg=self.colors['bg_secondary'])
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Снаряжение
        equip_frame = self.create_card_frame(left)
        equip_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(equip_frame, text="🎒 СНАРЯЖЕНИЕ", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(anchor=tk.W, padx=15, pady=10)
        
        self.equipment_text = self.create_text_widget(equip_frame, height=12)
        self.equipment_text.insert("1.0", "• Рюкзак\n• Фляга с водой\n• Верёвка\n• Факелы\n• Кремень\n• Кемпинг набор")
        self.equipment_text.config(state='disabled')
        
        # Оружие
        weapon_frame = self.create_card_frame(left)
        weapon_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(weapon_frame, text="⚔️ ОРУЖИЕ", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(anchor=tk.W, padx=15, pady=10)
        
        self.weapon_text = self.create_text_widget(weapon_frame, height=6)
        self.weapon_text.insert("1.0", "• Длинный меч\n• Лук\n• Стрелы\n• Кинжал")
        self.weapon_text.config(state='disabled')
        
        # Заклинания
        spell_frame = self.create_card_frame(right)
        spell_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(spell_frame, text="✨ ЗАКЛИНАНИЯ", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(anchor=tk.W, padx=15, pady=10)
        
        self.spell_text = self.create_text_widget(spell_frame, height=12)
        self.spell_text.insert("1.0", "• Магическая стрела\n• Обнаружение магии\n• Свет\n• Щит")
        self.spell_text.config(state='disabled')
        
        # Способности
        ability_frame = self.create_card_frame(right)
        ability_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(ability_frame, text="🌟 СПОСОБНОСТИ", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(anchor=tk.W, padx=15, pady=10)
        
        self.ability_text = self.create_text_widget(ability_frame, height=6)
        self.ability_text.insert("1.0", "• Боевой стиль\n• Второе дыхание\n• Рывок\n• Уклонение")
        self.ability_text.config(state='disabled')
    
    def create_text_widget(self, parent, height=10):
        """Создает текстовый виджет с единым стилем"""
        text_widget = tk.Text(
            parent,
            height=height,
            font=('Consolas', 10),
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            relief='flat',
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        return text_widget
    
    def create_bio_tab(self):
        """Создает вкладку с биографией (ИСПРАВЛЕНА ОШИБКА)"""
        self.tab_bio = tk.Frame(self.notebook, bg=self.colors['bg_secondary'])
        self.notebook.add(self.tab_bio, text="Биография")
        
        container = tk.Frame(self.tab_bio, bg=self.colors['bg_secondary'], padx=15, pady=15)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Личность
        personality_frame = self.create_card_frame(container)
        personality_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(personality_frame, text="👤 ЛИЧНОСТЬ ПЕРСОНАЖА", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(anchor=tk.W, padx=15, pady=15)
        
        # Сетка для черт личности (ИСПРАВЛЕННАЯ СТРОКА)
        personality_grid = tk.Frame(personality_frame, bg=self.colors['bg_cards'], padx=15, pady=15)  # Исправлено здесь
        personality_grid.pack(fill=tk.BOTH, expand=True)
        
        # Черты личности
        personality_data = [
            ("Черты характера", "traits", "🎭"),
            ("Идеалы", "ideals", "💡"),
            ("Привязанности", "bonds", "🤝"),
            ("Слабости", "flaws", "⚠️")
        ]
        
        self.personality_widgets = {}
        for i, (title, key, icon) in enumerate(personality_data):
            section = tk.Frame(
                personality_grid,
                bg=self.colors['bg_cards'],
                highlightbackground=self.colors['border'],
                highlightthickness=1
            )
            section.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            tk.Label(section, text=f"{icon} {title}", font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(anchor=tk.W, padx=10, pady=10)
            
            text_widget = self.create_text_widget(section, height=5)
            text_widget.insert("1.0", f"• {title.lower()} 1\n• {title.lower()} 2")
            text_widget.config(state='disabled')
            
            self.personality_widgets[key] = text_widget
        
        # История
        history_frame = self.create_card_frame(container)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(history_frame, text="📜 ИСТОРИЯ ПЕРСОНАЖА", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_cards'], fg=self.colors['text_primary']).pack(anchor=tk.W, padx=15, pady=15)
        
        self.history_text = self.create_text_widget(history_frame)
        self.history_text.insert("1.0", "Здесь появится уникальная история вашего персонажа.")
        self.history_text.config(state='disabled')
        
        # Настройка сетки личности
        for i in range(2):
            personality_grid.columnconfigure(i, weight=1)
        for i in range(2):
            personality_grid.rowconfigure(i, weight=1)
    
    def generate_character(self):
        """Генерация персонажа через нейросеть"""
        mode = self.creation_mode.get()
        description = ""
        
        if mode == "manual":
            description = self.description_text.get("1.0", tk.END).strip()
            if len(description) < 10:
                messagebox.showwarning("Внимание", "Опишите персонажа подробнее (минимум 10 символов)")
                return
        
        # Обновляем статус
        self.status_label.config(text="Идет создание персонажа...", fg=self.colors['accent_warning'])
        self.generate_btn.config(state='disabled')
        self.root.update()
        
        try:
            # Генерация через нейросеть
            self.character_data = self.generate_with_ai(mode, description)
            
            # Обновляем интерфейс
            self.update_character_display()
            self.save_btn.config(state='normal')
            
            # Успех
            self.status_label.config(text="Персонаж успешно создан!", fg=self.colors['accent_success'])
            messagebox.showinfo("Успех!", f"Персонаж '{self.character_data.get('name', 'Безымянный')}' создан!")
            
        except Exception as e:
            self.status_label.config(text="Ошибка при создании", fg=self.colors['accent_error'])
            messagebox.showerror("Ошибка", f"Не удалось создать персонажа:\n\n{str(e)}")
        finally:
            self.generate_btn.config(state='normal')
    
    def generate_with_ai(self, mode, description=""):
        """Запрос к нейросети для генерации персонажа"""
        if mode == "random":
            races = ["Человек", "Эльф", "Дварф", "Халфлинг", "Драконорожденный"]
            classes = ["Воин", "Волшебник", "Жрец", "Плут", "Варвар", "Паладин"]
            
            prompt = f"""
            Создай персонажа для {self.game_system.get()}:
            - Раса: {random.choice(races)}
            - Класс: {random.choice(classes)}
            - Уровень: {self.level_var.get()}
            
            ВЕРНИ ОТВЕТ В JSON формате!
            """
        else:
            prompt = f"""
            Создай персонажа на основе описания:
            "{description}"
            
            Уровень: {self.level_var.get()}
            Система: {self.game_system.get()}
            
            ВЕРНИ ОТВЕТ В JSON формате!
            """
        
        # Базовый JSON формат
        prompt += """
        {
            "name": "Имя Фамилия",
            "race": "Раса",
            "class": "Класс",
            "level": 1,
            "background": "Предыстория",
            "alignment": "Мировоззрение",
            "age": "Возраст",
            "stats": {
                "strength": 10,
                "dexterity": 10,
                "constitution": 10,
                "intelligence": 10,
                "wisdom": 10,
                "charisma": 10
            },
            "equipment": ["Предмет 1", "Предмет 2"],
            "weapons": ["Оружие 1", "Оружие 2"],
            "spells": ["Заклинание 1", "Заклинание 2"],
            "abilities": ["Способность 1", "Способность 2"],
            "backstory": "История персонажа"
        }
        """
        
        # Отправляем запрос
        headers = {
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": CONFIG["model"],
            "messages": [
                {"role": "system", "content": "Ты создаешь персонажей для настольных игр. Отвечай на русском."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 1500
        }
        
        response = requests.post(CONFIG["api_url"], headers=headers, json=data, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"Ошибка API: {response.status_code}")
        
        # Парсим ответ
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        try:
            # Извлекаем JSON
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            
            character_data = json.loads(json_str)
            
            # Метаданные
            character_data["_meta"] = {
                "created": datetime.now().isoformat(),
                "system": self.game_system.get(),
                "generation_mode": mode,
                "level": self.level_var.get()
            }
            
            # Модификаторы
            if "stats" in character_data:
                character_data["stat_modifiers"] = {}
                for stat, value in character_data["stats"].items():
                    if isinstance(value, int):
                        character_data["stat_modifiers"][stat] = (value - 10) // 2
            
            return character_data
            
        except json.JSONDecodeError:
            print("Ответ нейросети (первые 500 символов):")
            print(content[:500])
            raise Exception("Некорректный JSON формат от нейросети")
    
    def update_character_display(self):
        """Обновление интерфейса с данными персонажа"""
        if not self.character_data:
            return
        
        char = self.character_data
        
        # Заголовок
        self.character_header.config(text=f"{char.get('name', 'Безымянный Герой')}")
        
        # Основные карточки
        for key, label in self.cards.items():
            if key in char:
                label.config(text=str(char[key]))
        
        # Характеристики
        if 'stats' in char:
            for stat, widgets in self.stat_widgets.items():
                if stat in char['stats']:
                    value = char['stats'][stat]
                    mod = char.get('stat_modifiers', {}).get(stat, 0)
                    
                    widgets['value'].config(text=str(value))
                    
                    if mod > 0:
                        widgets['modifier'].config(text=f"+{mod}", fg=self.colors['accent_success'])
                    elif mod < 0:
                        widgets['modifier'].config(text=str(mod), fg=self.colors['accent_error'])
                    else:
                        widgets['modifier'].config(text="0", fg=self.colors['text_muted'])
        
        # Обновляем текстовые виджеты
        self.update_text_widget(self.equipment_text, char.get('equipment', []))
        self.update_text_widget(self.weapon_text, char.get('weapons', []))
        self.update_text_widget(self.spell_text, char.get('spells', []))
        self.update_text_widget(self.ability_text, char.get('abilities', []))
        
        # История
        if 'backstory' in char:
            self.history_text.config(state='normal')
            self.history_text.delete("1.0", tk.END)
            self.history_text.insert("1.0", char['backstory'])
            self.history_text.config(state='disabled')
    
    def update_text_widget(self, widget, data, bullet="• "):
        """Обновление текстового виджета"""
        widget.config(state='normal')
        widget.delete("1.0", tk.END)
        
        if isinstance(data, list):
            for item in data:
                widget.insert(tk.END, f"{bullet}{item}\n")
        elif isinstance(data, str):
            widget.insert(tk.END, data)
        
        widget.config(state='disabled')
    
    def save_character(self):
        """Сохранение персонажа в файл"""
        if not self.character_data:
            return
        
        char_name = self.character_data.get('name', 'character').replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"{char_name}_{timestamp}.json"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json")],
            initialdir=CONFIG["save_folder"],
            initialfile=default_name,
            title="Сохранить персонажа"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.character_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Успешно!", f"Сохранено в:\n{filename}")
                self.status_label.config(text=f"Сохранено: {os.path.basename(filename)}", 
                                       fg=self.colors['accent_info'])
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{str(e)}")

def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = DnDCharacterGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()