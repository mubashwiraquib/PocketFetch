function bytesToSize(bytes) {

    if (!bytes)
        return "Unknown";

    const sizes = ["Bytes", "KB", "MB", "GB", "TB"];

    const i = Math.floor(
        Math.log(bytes) / Math.log(1024)
    );

    return (
        bytes / Math.pow(1024, i)
    ).toFixed(1) + " " + sizes[i];
}


function formatDuration(seconds) {

    if (!seconds)
        return "Unknown";

    const h = Math.floor(seconds / 3600);

    const m = Math.floor(
        (seconds % 3600) / 60
    );

    const s = seconds % 60;

    if (h > 0)
        return `${h}h ${m}m ${s}s`;

    return `${m}m ${s}s`;
}


async function analyze() {

    const url = document
        .getElementById("url")
        .value
        .trim();

    if (!url) {

        alert("Please enter a URL.");

        return;
    }

    document.getElementById("result").innerHTML =
        "<p>Analyzing...</p>";

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

<img
src="${data.thumbnail}"
style="
max-width:300px;
border-radius:12px;
">

<p>

Duration:

${formatDuration(data.duration)}

</p>

<h3>Available Formats</h3>

`;

    for (const f of data.formats) {

        html += `

<div class="info">

<b>${f.resolution}</b>

${f.ext}

(${bytesToSize(f.filesize)})

<button
onclick="downloadMedia(
'${url}',
'${f.id}'
)">
Download
</button>

</div>

`;
    }

    html += `

<div id="progressArea"></div>

`;

    document.getElementById("result").innerHTML = html;

}
async function downloadMedia(url, formatId) {

    const response = await fetch("/download", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            url: url,

            format_id: formatId

        })

    });

    const data = await response.json();

    if (!data.download_id) {

        alert("Unable to start download.");

        return;
    }

    document.getElementById("progressArea").innerHTML = `

<h3>Downloading...</h3>

<progress
id="progressBar"
value="0"
max="100"
style="width:100%;">
</progress>

<p id="progressText">
0%
</p>

<p id="speedText"></p>

<p id="etaText"></p>

`;

    checkProgress(data.download_id);

}


async function checkProgress(downloadId) {

    const timer = setInterval(async () => {

        const response = await fetch(

            "/progress/" + downloadId

        );

        const job = await response.json();

        document.getElementById("progressBar").value =
            job.progress;

        document.getElementById("progressText").innerHTML =
            job.progress.toFixed(1) + "%";

        document.getElementById("speedText").innerHTML =
            "Speed: " + bytesToSize(job.speed) + "/s";

        document.getElementById("etaText").innerHTML =
            "ETA: " + job.eta + " sec";

        if (job.status === "finished") {

            clearInterval(timer);

            document.getElementById("progressText").innerHTML =
                "Download Completed!";

            window.location =
                "/file/" + downloadId;

        }

        if (job.status === "error") {

            clearInterval(timer);

            alert(job.error);

        }

    }, 1000);

}


document.addEventListener(

    "DOMContentLoaded",

    () => {

        const analyzeButton = document.getElementById("analyzeBtn");

        analyzeButton.addEventListener(

            "click",

            analyze

        );

    }

);