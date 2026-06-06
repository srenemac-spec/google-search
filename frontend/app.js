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

    document.getElementById("status").innerText = `${data.results.length} : tolik jsem jich našel.`;

    renderResults(data.results);
    // update debug counter
    const debug = document.getElementById('debug-count');
    if (debug) debug.textContent = `Returned: ${data.results.length} | Rendered: ${document.getElementById('results').childElementCount}`;
}

function renderResults(results) {
    const container = document.getElementById('results');
    container.innerHTML = '';
    const frag = document.createDocumentFragment();

    for (const result of results) {
        const card = document.createElement('div');
        card.className = 'result';

        const title = document.createElement('div');
        title.className = 'result-title';
        title.textContent = `${result.position}. ${result.title}`;

        const urlWrap = document.createElement('div');
        urlWrap.className = 'result-url';
        const a = document.createElement('a');
        a.href = result.url || '#';
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.textContent = result.url || '';
        urlWrap.appendChild(a);

        const snippet = document.createElement('div');
        snippet.className = 'result-snippet';
        snippet.textContent = result.snippet || '';

        card.appendChild(title);
        card.appendChild(urlWrap);
        card.appendChild(snippet);
        frag.appendChild(card);
    }

    container.appendChild(frag);
    const debug = document.getElementById('debug-count');
    if (debug) debug.textContent = `Returned: ${lastResults ? lastResults.results.length : 0} | Rendered: ${container.childElementCount}`;
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