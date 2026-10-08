async function predictImage() {

    const input = document.getElementById("imageInput");
    const message = document.getElementById("message");
    const preview = document.getElementById("preview");

    if (input.files.length === 0) {
        message.innerText = "Please select an image first.";
        return;
    }

    const file = input.files[0];

    // Show image preview
    const imageURL = URL.createObjectURL(file);

    preview.innerHTML = `
        <img src="${imageURL}" alt="Selected Image">
    `;

    message.innerText = "Analyzing image...";

    // Prepare image for upload
    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Prediction request failed.");
        }

        const data = await response.json();

        let output = "<h2>Prediction Result</h2>";

        data.predictions.forEach((prediction) => {

            const percentage =
                (prediction.confidence * 100).toFixed(2);

            output += `
                <div class="prediction">
                    <strong>${prediction.label}</strong>
                    <br>
                    Confidence: ${percentage}%
                </div>
            `;
        });

        document.getElementById("result").innerHTML = output;

    } catch (error) {

        document.getElementById("result").innerHTML = `
            <h2>Error</h2>
            <p>${error.message}</p>
        `;
    }
}