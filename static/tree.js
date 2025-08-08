function renderTree(node, container) {
    const ul = document.createElement('ul');
    for (const key in node.children) {
        const li = document.createElement('li');
        li.textContent = key;
        if (Object.keys(node.children[key].children).length > 0) {
            renderTree(node.children[key], li);
        }
        ul.appendChild(li);
    }
    container.appendChild(ul);
}
