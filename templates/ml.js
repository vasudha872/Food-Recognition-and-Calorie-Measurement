// Add an event listener to the submit button
submitBtn.addEventListener("click", () => {
    // Get the selected image file
    const file = foodImage.files[0];
  
    // Create a new image element and load the selected file into it
    const img = new Image();
    img.onload = () => {
      // Preprocess the image and convert it to a tensor
      const tensor = tf.browser.fromPixels(img)
        .resizeNearestNeighbor([224, 224])  // resize to the input size of the model
        .toFloat()
        .sub(255/2)  // normalize the pixel values
        .div(255/2)
        .expandDims();
  
      // Make a prediction with the loaded model
      const prediction = model.predict(tensor);
  
      // Get the predicted calorie measurement
      const result = prediction.dataSync()[0];
  
      // Update the DOM element with the predicted calorie measurement
      calorieResult.textContent = `This food contains ${result.toFixed(0)} calories`;
    };
    img.src = URL.createObjectURL(file);
  });
  