// Adicione isso em um arquivo separado ou no final do seu HTML
document.addEventListener('DOMContentLoaded', function() {
  // Validação do formulário
  const form = document.getElementById('obra-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      const nome = document.getElementById('id_nome').value;
      const numero = document.getElementById('id_numero_controle').value;
      
      if (!nome || !numero) {
        e.preventDefault();
        alert('Por favor, preencha os campos obrigatórios!');
      }
    });
  }
  
  // Filtro para a tabela (opcional)
  const searchInput = document.createElement('input');
  searchInput.type = 'text';
  searchInput.placeholder = 'Filtrar obras...';
  searchInput.style.marginBottom = '10px';
  searchInput.style.padding = '8px';
  searchInput.style.width = '100%';
  searchInput.style.boxSizing = 'border-box';
  
  const table = document.getElementById('obras-table');
  if (table) {
    table.parentNode.insertBefore(searchInput, table);
    
    searchInput.addEventListener('keyup', function() {
      const filter = this.value.toLowerCase();
      const rows = table.getElementsByTagName('tr');
      
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let showRow = false;
        
        for (let j = 0; j < cells.length; j++) {
          if (cells[j]) {
            const text = cells[j].textContent || cells[j].innerText;
            if (text.toLowerCase().indexOf(filter) > -1) {
              showRow = true;
              break;
            }
          }
        }
        
        rows[i].style.display = showRow ? '' : 'none';
      }
    });
  }
});