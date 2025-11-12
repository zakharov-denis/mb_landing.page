#!/usr/bin/env python3
import re

# Read the file
with open('page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Improve language switcher to prevent breaking and add mobile support
old_inject = r'''            // Create and inject language switcher into navigation
            function injectLanguageSwitcher\(\) \{
                // Find the navigation container - try multiple selectors
                const navContainers = document\.querySelectorAll\('\[data-framer-name="Navigation"\], \.framer-1nhqjuk'\);

                if \(navContainers\.length > 0\) \{
                    navContainers\.forEach\(nav => \{
                        // Check if switcher already exists
                        if \(nav\.querySelector\('\.language-switcher'\)\) return;

                        // Create language switcher
                        const switcher = document\.createElement\('div'\);
                        switcher\.className = 'language-switcher';
                        switcher\.innerHTML = `
                            <button id="lang-en-\$\{nav\.id \|\| Math\.random\(\)\}" class="lang-en-btn \$\{savedLang === 'en' \? 'active' : ''\}" title="English">🇺🇸</button>
                            <button id="lang-ru-\$\{nav\.id \|\| Math\.random\(\)\}" class="lang-ru-btn \$\{savedLang === 'ru' \? 'active' : ''\}" title="Русский">🇷🇺</button>
                        `;

                        // Append to navigation
                        nav\.appendChild\(switcher\);
                    \}\);

                    setupEventListeners\(\);
                \}
            \}'''

new_inject = '''            // Create and inject language switcher into navigation
            function injectLanguageSwitcher() {
                // Find the navigation container - try multiple selectors (including mobile)
                const navContainers = document.querySelectorAll('[data-framer-name="Navigation"], .framer-1nhqjuk, [data-framer-name="Content"] .framer-1l7jsio');

                if (navContainers.length > 0) {
                    navContainers.forEach(nav => {
                        // Check if switcher already exists in this specific nav
                        if (nav.querySelector('.language-switcher')) {
                            // Switcher exists, just update active states
                            updateActiveButtons(savedLang);
                            return;
                        }

                        // Create language switcher
                        const switcher = document.createElement('div');
                        switcher.className = 'language-switcher';
                        switcher.innerHTML = `
                            <button class="lang-en-btn ${savedLang === 'en' ? 'active' : ''}" title="English">🇺🇸</button>
                            <button class="lang-ru-btn ${savedLang === 'ru' ? 'active' : ''}" title="Русский">🇷🇺</button>
                        `;

                        // Append to navigation
                        nav.appendChild(switcher);
                    });

                    // Always setup event listeners to ensure they work
                    setupEventListeners();
                }
            }'''

content = re.sub(old_inject, new_inject, content)

# Fix 2: Update CSS to show language switcher on mobile
old_css = r'''        \.language-switcher \{
            display: inline-flex;
            gap: 8px;
            align-items: center;
            margin-left: 20px;
        \}'''

new_css = '''        .language-switcher {
            display: inline-flex;
            gap: 8px;
            align-items: center;
            margin-left: 20px;
        }

        /* Show language switcher on mobile */
        @media (max-width: 809.98px) {
            .language-switcher {
                margin-left: auto;
                margin-right: 10px;
            }
        }'''

content = re.sub(old_css, new_css, content)

# Fix 3: Replace "Join Waitlist" with "Get Started" and update URL
# Also update the translation
content = content.replace(
    '"Join Waitlist": "Присоединиться"',
    '"Get Started": "Начать"'
)

# Replace button text (there are multiple instances)
content = content.replace(
    '>Join Waitlist<',
    '>Get Started<'
)

# Replace form action - we need to change the button to a link
# Find the form sections and replace with a link button
old_form_button = r'<button type="submit" class="framer-bTL5I framer-1kwuebo framer-v-1kwuebo" data-framer-name="Default" data-reset="button" tabindex="0" style="background-color:rgb\(111, 60, 255\);border-bottom-left-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-top-right-radius:10px;height:100%;width:100%;opacity:1"><div class="framer-138ofpz" data-framer-component-type="RichTextContainer" style="--extracted-r6o4lv:rgb\(255, 255, 255\);--framer-link-text-color:rgb\(0, 153, 255\);--framer-link-text-decoration:underline;transform:none"><p class="framer-text" style="--font-selector:SW50ZXItU2VtaUJvbGQ=;--framer-font-size:14px;--framer-font-weight:600;--framer-text-color:var\(--extracted-r6o4lv, rgb\(255, 255, 255\)\)">Get Started</p></div></button>'

new_link_button = r'<a href="https://mobile--morningbuddies.us-central1.hosted.app/" target="_blank" rel="noopener noreferrer" class="framer-bTL5I framer-1kwuebo framer-v-1kwuebo" data-framer-name="Default" tabindex="0" style="background-color:rgb(111, 60, 255);border-bottom-left-radius:10px;border-bottom-right-radius:10px;border-top-left-radius:10px;border-top-right-radius:10px;height:100%;width:100%;opacity:1;display:flex;align-items:center;justify-content:center;text-decoration:none"><div class="framer-138ofpz" data-framer-component-type="RichTextContainer" style="--extracted-r6o4lv:rgb(255, 255, 255);--framer-link-text-color:rgb(0, 153, 255);--framer-link-text-decoration:underline;transform:none"><p class="framer-text" style="--font-selector:SW50ZXItU2VtaUJvbGQ=;--framer-font-size:14px;--framer-font-weight:600;--framer-text-color:var(--extracted-r6o4lv, rgb(255, 255, 255))">Get Started</p></div></a>'

content = re.sub(old_form_button, new_link_button, content)

# Write the updated content
with open('page.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All fixes applied successfully!")
print("1. Language switcher breaking issue fixed")
print("2. Language switcher now shows on mobile")
print("3. 'Join Waitlist' replaced with 'Get Started' linking to the app")
