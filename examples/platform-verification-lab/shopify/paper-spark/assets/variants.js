for (const picker of document.querySelectorAll('[data-variant-picker]')) {
  const form = picker.closest('form');
  const sync = () => {
    const variant = picker.selectedOptions[0];
    if (!variant) return;
    const available = variant.dataset.available === 'true';
    const button = form.querySelector('[data-add]');
    const price = form.querySelector('[data-current-price]');
    button.disabled = !available;
    button.textContent = available ? 'Add to bag' : 'Sold out';
    price.textContent = variant.dataset.price;
  };
  picker.addEventListener('change', sync);
  sync();
}
