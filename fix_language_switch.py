#!/usr/bin/env python3

# Read the file
with open('page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the translatePage function with a better implementation
old_translate = '''        // Function to translate text nodes
        function translatePage(lang) {
            if (lang === 'ru') {
                // Clear previous translations
                translatedElements.clear();

                // Translate h1 elements
                document.querySelectorAll('h1').forEach(el => {
                    const text = el.textContent.trim();
                    if (translations[text]) {
                        translatedElements.set(el, text);
                        el.textContent = translations[text];
                    }
                });

                // Translate p elements
                document.querySelectorAll('p').forEach(el => {
                    const text = el.textContent.trim();
                    if (translations[text]) {
                        translatedElements.set(el, text);
                        el.textContent = translations[text];
                    }
                });

                // Translate buttons
                document.querySelectorAll('button').forEach(el => {
                    const text = el.textContent.trim();
                    if (translations[text]) {
                        translatedElements.set(el, text);
                        el.textContent = translations[text];
                    }
                });

                // Translate input placeholders
                document.querySelectorAll('input[placeholder]').forEach(el => {
                    const placeholder = el.getAttribute('placeholder');
                    if (translations[placeholder]) {
                        if (!el.getAttribute('data-original-placeholder')) {
                            el.setAttribute('data-original-placeholder', placeholder);
                        }
                        el.setAttribute('placeholder', translations[placeholder]);
                    }
                });
            } else {
                // Restore English from stored originals
                translatedElements.forEach((originalText, element) => {
                    element.textContent = originalText;
                });
                translatedElements.clear();

                // Restore input placeholders
                document.querySelectorAll('[data-original-placeholder]').forEach(el => {
                    el.setAttribute('placeholder', el.getAttribute('data-original-placeholder'));
                });
            }
        }'''

new_translate = '''        // Function to translate text nodes
        function translatePage(lang) {
            console.log('=== translatePage called with:', lang, '===');

            if (lang === 'ru') {
                console.log('Starting Russian translation...');

                // Translate h1 elements
                let h1Count = 0;
                document.querySelectorAll('h1').forEach(el => {
                    const currentText = el.textContent.trim();

                    // Check if we already have original stored
                    if (!translatedElements.has(el)) {
                        // This is first time translating this element
                        if (translations[currentText]) {
                            translatedElements.set(el, currentText);
                            el.textContent = translations[currentText];
                            h1Count++;
                        }
                    } else {
                        // Element was already translated, use stored original
                        const originalText = translatedElements.get(el);
                        if (translations[originalText]) {
                            el.textContent = translations[originalText];
                            h1Count++;
                        }
                    }
                });
                console.log(`Translated ${h1Count} h1 elements`);

                // Translate h2 elements
                let h2Count = 0;
                document.querySelectorAll('h2').forEach(el => {
                    const currentText = el.textContent.trim();

                    if (!translatedElements.has(el)) {
                        if (translations[currentText]) {
                            translatedElements.set(el, currentText);
                            el.textContent = translations[currentText];
                            h2Count++;
                        }
                    } else {
                        const originalText = translatedElements.get(el);
                        if (translations[originalText]) {
                            el.textContent = translations[originalText];
                            h2Count++;
                        }
                    }
                });
                console.log(`Translated ${h2Count} h2 elements`);

                // Translate h3 elements (FAQ questions)
                let h3Count = 0;
                document.querySelectorAll('h3').forEach(el => {
                    const currentText = el.textContent.trim();

                    if (!translatedElements.has(el)) {
                        if (translations[currentText]) {
                            translatedElements.set(el, currentText);
                            el.textContent = translations[currentText];
                            h3Count++;
                        }
                    } else {
                        const originalText = translatedElements.get(el);
                        if (translations[originalText]) {
                            el.textContent = translations[originalText];
                            h3Count++;
                        }
                    }
                });
                console.log(`Translated ${h3Count} h3 elements`);

                // Translate p elements
                let pCount = 0;
                document.querySelectorAll('p').forEach(el => {
                    const currentText = el.textContent.trim();

                    if (!translatedElements.has(el)) {
                        if (translations[currentText]) {
                            translatedElements.set(el, currentText);
                            el.textContent = translations[currentText];
                            pCount++;
                        }
                    } else {
                        const originalText = translatedElements.get(el);
                        if (translations[originalText]) {
                            el.textContent = translations[originalText];
                            pCount++;
                        }
                    }
                });
                console.log(`Translated ${pCount} p elements`);

                // Translate buttons
                let btnCount = 0;
                document.querySelectorAll('button').forEach(el => {
                    const currentText = el.textContent.trim();

                    if (!translatedElements.has(el)) {
                        if (translations[currentText]) {
                            translatedElements.set(el, currentText);
                            el.textContent = translations[currentText];
                            btnCount++;
                        }
                    } else {
                        const originalText = translatedElements.get(el);
                        if (translations[originalText]) {
                            el.textContent = translations[originalText];
                            btnCount++;
                        }
                    }
                });
                console.log(`Translated ${btnCount} button elements`);

                // Translate input placeholders
                document.querySelectorAll('input[placeholder]').forEach(el => {
                    const placeholder = el.getAttribute('placeholder');
                    if (translations[placeholder]) {
                        if (!el.getAttribute('data-original-placeholder')) {
                            el.setAttribute('data-original-placeholder', placeholder);
                        }
                        el.setAttribute('placeholder', translations[placeholder]);
                    }
                });

                console.log(`Total elements tracked: ${translatedElements.size}`);
            } else {
                console.log('Restoring English...');
                // Restore English from stored originals
                const restoreCount = translatedElements.size;
                translatedElements.forEach((originalText, element) => {
                    element.textContent = originalText;
                });
                console.log(`Restored ${restoreCount} elements to English`);

                // Restore input placeholders
                document.querySelectorAll('[data-original-placeholder]').forEach(el => {
                    el.setAttribute('placeholder', el.getAttribute('data-original-placeholder'));
                });
            }
            console.log('=== translatePage finished ===');
        }'''

content = content.replace(old_translate, new_translate)

# Write back
with open('page.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Исправлена система переключения языков!")
print("\nЧто изменилось:")
print("  • Оригинальные тексты сохраняются НАВСЕГДА (не очищаются)")
print("  • При повторном переключении используются сохраненные оригиналы")
print("  • Добавлена поддержка H2 и H3 элементов (для FAQ)")
print("  • Добавлено детальное логирование каждого типа элементов")
print("\nТеперь можно переключать язык сколько угодно раз!")
