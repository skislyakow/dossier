const text = "Python Django Developer";
const el = document.getElementById('typing-text');
let i = 0;

function type() {
    if (i < text.length) {
        el.textContent += text.charAt(i);
        i++;
        const delay = text.charAt(i - 1) === ' ' ? 160 : 100;
        setTimeout(type, delay);
    }
}

setTimeout(type, 500);