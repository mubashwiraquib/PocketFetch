function bytesToSize(bytes) {
    if (!bytes) return "Unknown";

    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));

    return (bytes / Math.pow(1024, i)).toFixed(1) + " " + sizes[i];
}

function formatDuration(seconds) {
    if (!seconds) return "Unknown";

    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;

    if (h > 0)
        return `${h}h ${m}m ${s}s`;

    return `${m}m ${s}s`;
}

const button = document.getElementById("analyzeBtn");

button.addEventListener("click", async () => {

    const url = document.getElementById("url").value.trim();

    if (!url) {
        alert("Please enter a URL.");
        return;
    }

    document.getElementById("result").innerHTML = "<p>Analyzing...</p>";

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: url
        })
    });

    const data = await response.json();

    if (!data.success) {
        document.getElementById("result").innerHTML =
            `<p>${data.error}</p>`;
        return;
    }

    let html = `
        <h2>${data.title}</h2>

        <img src="${data.thumbnail}" alt="Thumbnail">

        <div class="info">
            <strong>Duration:</strong>
            ${formatDuration(data.duration)}
        </div>

        <h3>Formats</h3>
    `;

    for (const f of data.formats) {

        html += `
            <div class="info">
                <b>${f.resolution || "Unknown"}</b>
                ${f.ext}
                (${bytesToSize(f.filesize)})
                <button onclick="downloadFile('${url}','${f.id}')">
    Download
</button>
            </div>
        `;
    }

    document.getElementById("result").innerHTML = html;

});
async function downloadFile(url, formatId){

    const response = await fetch("/download",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            url:url,

            format_id:formatId

        })

    });

    const blob = await response.blob();

    const downloadUrl = window.URL.createObjectURL(blob);

    const a=document.createElement("a");

    a.href=downloadUrl;

    a.download="download";

    document.body.appendChild(a);

    a.click();

    a.remove();

}