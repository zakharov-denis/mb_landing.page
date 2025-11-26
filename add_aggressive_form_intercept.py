#!/usr/bin/env python3

# Read the file
with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert the interception script (right after opening body tag or before closing head)
# Let's insert it right before the first <script> tag in the body

insert_point = '<script async src="https://events.framer.com'

aggressive_intercept = '''<script>
    console.log('🛡️ Form interception script loaded');

    // AGGRESSIVE form submission blocker
    // This runs IMMEDIATELY, before any other scripts
    (function() {
        // Override form submit method globally
        const originalSubmit = HTMLFormElement.prototype.submit;
        HTMLFormElement.prototype.submit = function() {
            console.log('⚠️ Form.submit() called - BLOCKED');
            return false;
        };

        // Intercept at the earliest possible phase
        document.addEventListener('submit', function(e) {
            const form = e.target;
            console.log('🔍 Submit event captured:', form.className);

            if (form.classList.contains('framer-rf4jiv')) {
                console.log('🛑 BLOCKING Framer form submission');
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();

                // Call our custom handler
                if (typeof window.handleFormSubmit === 'function') {
                    console.log('✅ Calling custom handleFormSubmit');
                    const fakeEvent = new Event('submit', { bubbles: false, cancelable: false });
                    Object.defineProperty(fakeEvent, 'currentTarget', { value: form, writable: false });
                    Object.defineProperty(fakeEvent, 'target', { value: form, writable: false });
                    window.handleFormSubmit(fakeEvent);
                } else {
                    console.error('❌ handleFormSubmit not found yet');
                }

                return false;
            }
        }, true); // Capture phase - runs FIRST

        // Also block button clicks
        document.addEventListener('click', function(e) {
            const button = e.target.closest('button[type="submit"]');
            if (button && button.closest('form.framer-rf4jiv')) {
                console.log('🛑 BLOCKING submit button click');
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                return false;
            }
        }, true); // Capture phase

        console.log('✅ Form interception initialized');
    })();
</script>

<script async src="https://events.framer.com'''

content = content.replace(insert_point, aggressive_intercept)

# Make handleFormSubmit global
content = content.replace(
    'async function handleFormSubmit(event) {',
    'window.handleFormSubmit = async function(event) {'
)

# Write back
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added aggressive form interception!")
print("\nChanges:")
print("  • Overrode HTMLFormElement.prototype.submit")
print("  • Added submit event blocker in capture phase")
print("  • Added button click blocker in capture phase")
print("  • Made handleFormSubmit globally accessible")
print("  • Script loads BEFORE any Framer scripts")
