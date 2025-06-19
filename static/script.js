document.getElementById("resumeForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const jobDescription = document.getElementById("job-description").value;
    const resumeFiles = document.getElementById("resume-upload").files;

    if (!jobDescription.trim() || resumeFiles.length === 0) {
        alert("⚠️ Please enter a job description and upload at least one resume.");
        return;
    }

    let formData = new FormData();
    formData.append("job_description", jobDescription);

    for (let file of resumeFiles) {
        formData.append("resumes", file);
    }

    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error("Error:", error);
        alert("❌ Something went wrong! Please try again.");
    }
});

function displayResults(results) {
    let tbody = document.querySelector("#resultTable tbody");
    tbody.innerHTML = "";

    results.forEach((resume) => {
        let row = `<tr>
            <td>${resume.resume_name}</td>
            <td>${(resume.match_score * 100).toFixed(2)}%</td>
        </tr>`;
        tbody.innerHTML += row;
    });

    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
}
