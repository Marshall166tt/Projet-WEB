const counters = document.querySelectorAll('.counter');

counters.forEach(counter => {
  const count = counter.querySelector('.count');
  const plusBtn = counter.querySelector('.plus');
  const minusBtn = counter.querySelector('.minus');

  let currentValue = 0;

  plusBtn.addEventListener('click', () => {
    currentValue++;
    count.textContent = currentValue;
  });

  minusBtn.addEventListener('click', () => {
    if (currentValue > 0) {
      currentValue--;
      count.textContent = currentValue;
    }
  });
});