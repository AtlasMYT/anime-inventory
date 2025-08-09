function renderTree(node, container) {
    const ul = document.createElement('ul');

    for (const key in node.children) {
        const data = node.children[key];
        const li = document.createElement('li');

        // Add icon for file/folder
        if (data.type === "folder") {
            li.textContent = "📁 " + key;
        } else {
            li.textContent = "📄 " + key;
        }

        // Recurse for folders with children
        if (data.type === "folder" && data.children && Object.keys(data.children).length > 0) {
            renderTree(data, li);
        }

        ul.appendChild(li);
    }

    container.appendChild(ul);
}
