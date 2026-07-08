function bytesToSize(bytes) {

    if (!bytes)
        return "Unknown";

    const sizes = [
        "Bytes",
        "KB",
        "MB",
        "GB",
        "TB"
    ];

    const i = Math.floor(
        Math.log(bytes) /
        Math.log(1024)
    );

    return (
        bytes /
        Math.pow(1024, i)
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

    document.getElementById("result").innerHTML = `

<div class="loading">

<h2>

🔍 Analyzing...

</h2>

</div>

`;

    const response = await fetch(
        "/analyze",
        {

            method: "POST",

            headers: {

                "Content-Type":
                "application/json"

            },

            body: JSON.stringify({

                url: url

            })

        }
    );

    const data =
        await response.json();

    if (!data.success) {

        document.getElementById(
            "result"
        ).innerHTML = `

<div class="error">

${data.error}

</div>

`;

        return;

    }

    let html = `

<div class="video-card">

<img

class="thumbnail"

src="${data.thumbnail}"

>

<h2>

${data.title}

</h2>

<p class="duration">

⏱

${formatDuration(data.duration)}

</p>

<h3>

Available Formats

</h3>

`;

    for (const f of data.formats) {

        html += `

<div class="format-card">

<div class="format-left">

<div class="resolution">

🎥

${f.resolution}

</div>

<div class="details">

${f.ext.toUpperCase()}

•

${bytesToSize(f.filesize)}

</div>

</div>

<button

onclick="downloadFile(

'${url}',

'${f.id}'

)"

>

⬇ Download

</button>

</div>

`;

    }

    html += `

<div id="progressArea">

</div>

</div>

`;

    document.getElementById(
        "result"
    ).innerHTML = html;

}
async function downloadFile(url, formatId) {

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

<div class="download-card">

<h3>

⬇ Downloading...

</h3>

<progress

id="progressBar"

value="0"

max="100">

</progress>

<div id="progressText">

0%

</div>

<div id="speedText">

Speed: -

</div>

<div id="etaText">

ETA: -

</div>

</div>

`;

    checkProgress(data.download_id);

}


async function checkProgress(downloadId) {

    const timer = setInterval(async () => {

        const response = await fetch(

            "/progress/" + downloadId

        );

        const job = await response.json();

        if (!job) {

            clearInterval(timer);

            return;

        }

        const bar = document.getElementById("progressBar");

        if (bar)
            bar.value = job.progress;

        const progress = document.getElementById("progressText");

        if (progress)
            progress.innerHTML =
                job.progress.toFixed(1) + "%";

        const speed = document.getElementById("speedText");

        if (speed)
            speed.innerHTML =
                "Speed: " +
                bytesToSize(job.speed) +
                "/s";

        const eta = document.getElementById("etaText");

        if (eta)
            eta.innerHTML =
                "ETA: " +
                job.eta +
                " sec";

        if (job.status === "finished") {

            clearInterval(timer);

            if (progress)
                progress.innerHTML =
                    "✅ Download Complete";

            window.location =
                "/file/" + downloadId;

        }

        if (job.status === "error") {

            clearInterval(timer);

            alert(job.error);

        }

    }, 1000);

}
document.addEventListener("DOMContentLoaded", () => {

    const analyzeButton = document.getElementById("analyzeBtn");

    analyzeButton.addEventListener("click", analyze);

    const urlInput = document.getElementById("url");

    urlInput.addEventListener("keypress", (event) => {

        if (event.key === "Enter") {

            analyze();

        }

    });

});