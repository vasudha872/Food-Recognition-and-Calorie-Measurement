const foodImage = document.getElementById("foodImage");
const submitBtn = document.getElementById("submitBtn");
const calorieResult = document.getElementById("calorieResult");

submitBtn.addEventListener("click", () => {
  // Get the selected image file
  const file = foodImage.files[0];
  
  // Create a new FormData object and append the image file to it
  const formData = new FormData();
  formData.append("image", file);
  
  // Send a POST request to the server to process the image and get the calorie measurement result
  fetch("process-image.php", {
    method: "POST",
    body: formData
  })
  .then(response => response.text())
  .then(result => {
    // Update the calorie measurement result on the website
    calorieResult.textContent = `This food contains ${result} calories`;
  })
  .catch(error => console.error(error));
});
