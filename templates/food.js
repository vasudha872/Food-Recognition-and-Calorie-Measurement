document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('food-recognition-form');
  const resultDiv = document.getElementById('food-result');

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    fetch('/food_recognition', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      const class_name = data.class_name;
      const calories = data.calories;
      const confidence_score = data.confidence_score;
      const foodName = document.getElementById('food-name');
      const foodCalories = document.getElementById('food-calories');
      const foodConfidence = document.getElementById('food-confidence');

      foodName.innerHTML = class_name;
      foodCalories.innerHTML = calories;
      foodConfidence.innerHTML = `${confidence_score.toFixed(2)}%`;

      resultDiv.classList.remove('hidden');
    })
    .catch(error => console.log(error));
  });
});
