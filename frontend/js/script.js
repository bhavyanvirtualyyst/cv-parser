const fileInput = document.getElementById("cvFile");
const convertButton = document.getElementById("convertButton");
const statusText = document.getElementById("statusText");
const downloadButton = document.getElementById("downloadButton");

console.log("JavaScript loaded");
convertButton.addEventListener("click", async (event) => {
    event.preventDefault();
    console.log("Button clicked");
    const file = fileInput.files[0];
    console.log(file);
    if (!file) {
        statusText.innerText = "Please upload a CV first.";
        return;
    }
    statusText.innerText = "Processing CV...";
    const formData = new FormData();
    formData.append(
        "file",
        file
    );
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/convert",
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {

            throw new Error("Conversion failed");

        }


        const blob = await response.blob();


        const downloadURL = window.URL.createObjectURL(blob);


        downloadButton.href = downloadURL;

        downloadButton.download = "converted_cv.docx";

        downloadButton.hidden = false;


        statusText.innerText = "CV generated successfully.";



    } catch (error) {


        console.log(error);

        statusText.innerText = "Something went wrong.";


    }


});