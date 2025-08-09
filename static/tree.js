function renderTree(node, container) {
    const ul = document.createElement('ul');

    // Sort keys (folders/files) ascending
    const sortedKeys = Object.keys(node.children || {}).sort((a, b) => a.localeCompare(b));

    for (const key of sortedKeys) {
        const data = node.children[key];
        const li = document.createElement('li');

        if (data.type === "folder") {
            const span = document.createElement('span');
            span.textContent = "📁 " + key;
            span.style.cursor = "pointer";

            const childContainer = document.createElement('div');
            childContainer.style.marginLeft = "20px";
            renderTree(data, childContainer);

            // Start collapsed
            childContainer.style.display = "none";

            // Toggle collapse
            span.addEventListener('click', () => {
                childContainer.style.display =
                    childContainer.style.display === "none" ? "block" : "none";
            });

            li.appendChild(span);
            li.appendChild(childContainer);
        } else {
            li.textContent = "📄 " + key;
        }

        ul.appendChild(li);
    }

    container.appendChild(ul);
}
