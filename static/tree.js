fetch('/api/tree')
  .then(r => r.json())
  .then(data => {
    const container = document.getElementById('tree');
    function build(node) {
      const ul = document.createElement('ul');
      ul.className = 'tree';
      Object.entries(node).forEach(([name, child]) => {
        const li = document.createElement('li');
        li.textContent = name;
        if (Object.keys(child).length) {
          li.classList.add('folder', 'collapsed');
          li.addEventListener('click', e => {
            e.stopPropagation();
            li.classList.toggle('collapsed');
          });
          li.appendChild(build(child));
        } else {
          li.classList.add('file');
        }
        ul.appendChild(li);
      });
      return ul;
    }
    container.appendChild(build(data));
  })
  .catch(console.error);
