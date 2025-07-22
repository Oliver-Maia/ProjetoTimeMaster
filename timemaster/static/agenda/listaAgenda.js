document.addEventListener("DOMContentLoaded", () => {
  const inputNome = document.getElementById("filtro-nome");
  const inputData = document.getElementById("filtro-data");
  const botaoFiltrar = document.getElementById("btn-filtrar");
  const linhas = document.querySelectorAll("#tabela-corpo tr");

  function filtrar() {
    const nomeValor = inputNome.value.toLowerCase();
    const dataValor = inputData.value;

    linhas.forEach(linha => {
      const nome = linha.children[1]?.textContent.toLowerCase();
      const data = linha.children[3]?.textContent;

      const nomeOk = nome.includes(nomeValor);
      const dataOk = !dataValor || data.includes(dataValor.split("-").reverse().join("/"));

      linha.style.display = nomeOk && dataOk ? "" : "none";
    });
  }

  botaoFiltrar.addEventListener("click", filtrar);

  // Modal
  const modal = document.getElementById("modal-agendamento");
  const btn = document.getElementById("abrir-modal");
  const fechar = document.getElementById("fechar-modal");


  // Filtros por status
 document.querySelectorAll('.status-card').forEach(card => {
    card.addEventListener('click', () => {
        const status = card.getAttribute('data-status');
        const nome = document.getElementById("filtro-nome").value;
        const data = document.getElementById("filtro-data").value;
        
        // Cria URL com todos os parâmetros
        const params = new URLSearchParams();
        if (nome) params.append('nome', nome);
        if (data) params.append('data', data);
        params.append('status', status);
        
        // Mantém a paginação se existir
        const page = new URL(window.location.href).searchParams.get('page');
        if (page) params.append('page', page);
        
        window.location.href = `?${params.toString()}`;
    });
});

// listaAgenda.js
document.addEventListener('DOMContentLoaded', function() {
    // ... seu código existente ...

  
    // Função auxiliar para pegar o cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

});
