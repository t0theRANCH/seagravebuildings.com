const inputs = document.querySelectorAll('.text-field')
const textareas = document.querySelectorAll('.text-area')

inputs.forEach(
    (item) => {
        item.addEventListener('input', () => {
            item.setAttribute('value', item.value);
        });
    }
);

textareas.forEach(
    (item) => {
        item.addEventListener('input', () => {
            item.setAttribute('data-info', item.value);
        });
    }
);
