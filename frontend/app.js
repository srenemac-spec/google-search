let lastResults = null;

async function search() {

    const query =
        document.getElementById("query").value;

    if (!query) {
        alert("Co chceš vyhledat?");
        return;
    }

    document.getElementById(
        "status"
    ).innerText = "Gůgluji...";

    const response =
        await fetch(
            "http://localhost:8000/search",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    query: query
                })
            }
        );

    const data =
        await response.json();

    lastResults = data;

    document.getElementById(
        "status"
    ).innerText =
        `${data.results.length} : tolik jsem jich našel.`;

    renderResults(
        data.results
    );
}

function renderResults(results) {

    const container =
        document.getElementById(
            "results"
        );

    container.innerHTML = "";

    for (const result of results) {

        container.innerHTML += `
            <div class="result">

                <div class="result-title">
                    ${result.position}. ${result.title}
                </div>

                <div class="result-url">
                    <a href="${result.url}" target="_blank">
                        ${result.url}
                    </a>
                </div>

                <div class="result-snippet">
                    ${result.snippet}
                </div>

            </div>
        `;
    }
}

function downloadJson() {

    if (!lastResults) {
        alert("Nemám co stahovat!");
        return;
    }

    const blob =
        new Blob(
            [
                JSON.stringify(
                    lastResults,
                    null,
                    2
                )
            ],
            {
                type:
                    "application/json"
            }
        );

    const url =
        URL.createObjectURL(
            blob
        );

    const a =
        document.createElement("a");

    a.href = url;

    a.download =
        "results.json";

    a.click();

    URL.revokeObjectURL(
        url
    );
}

function downloadCsv() {

    if (!lastResults) {
        alert("Nemám co stahovat!");
        return;
    }

    let csv =
        "position,title,url,snippet\n";

    for (const result of lastResults.results) {

        const row = [
            result.position,
            `"${(result.title || "").replaceAll('"', '""')}"`,
            `"${(result.url || "").replaceAll('"', '""')}"`,
            `"${(result.snippet || "").replaceAll('"', '""')}"`
        ];

        csv += row.join(",") + "\n";
    }

    const blob = new Blob(
        [csv],
        {
            type: "text/csv"
        }
    );

    const url =
        URL.createObjectURL(blob);

    const a =
        document.createElement("a");

    a.href = url;
    a.download = "results.csv";

    a.click();

    URL.revokeObjectURL(url);
}

window.addEventListener("load", () => {
    document.getElementById("query").addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            search();
        }
    });
});