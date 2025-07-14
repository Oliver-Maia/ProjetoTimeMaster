document.addEventListener('DOMContentLoaded', function() {
  // Validação do formulário
  const form = document.getElementById('agendamento-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      const obra = document.getElementById('id_obra').value;
      const data = document.getElementById('id_data_agendamento').value;
      
      if (!obra || !data) {
        e.preventDefault();
        alert('Por favor, preencha todos os campos obrigatórios!');
      }
    });
  }
  
  // Filtro da tabela
  const searchInput = document.getElementById('search-agendamentos');
  const table = document.getElementById('agendamentos-table');
  
  if (searchInput && table) {
    searchInput.addEventListener('keyup', function() {
      const filter = this.value.toLowerCase();
      const rows = table.getElementsByTagName('tr');
      
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let showRow = false;
        
        for (let j = 0; j < cells.length; j++) {
          if (cells[j]) {
            const text = cells[j].textContent || cells[j].innerText;
            if (text.toLowerCase().includes(filter)) {
              showRow = true;
              break;
            }
          }
        }
        
        rows[i].style.display = showRow ? '' : 'none';
      }
    });
  }
  
  // Melhorar a experiência do datetime-local
  const dataField = document.getElementById('id_data_agendamento');
  if (dataField) {
    // Definir valor mínimo como data/hora atual
    const now = new Date();
    const timezoneOffset = now.getTimezoneOffset() * 60000;
    const localISOTime = (new Date(now - timezoneOffset)).toISOString().slice(0, 16);
    dataField.min = localISOTime;
    
    // Opcional: Adicionar datepicker melhorado
    // Você pode integrar uma biblioteca como flatpickr aqui
  }
});