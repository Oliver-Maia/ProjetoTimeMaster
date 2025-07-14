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

  btn.onclick = () => modal.style.display = "block";
  fechar.onclick = () => modal.style.display = "none";
  window.onclick = e => {
    if (e.target === modal) modal.style.display = "none";
  }
  // Filtros por status
  document.querySelectorAll('.status-card').forEach(card => {
  card.addEventListener('click', () => {
    const status = card.getAttribute('data-status');

    // Marca visual
    document.querySelectorAll('.status-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');

    // Redireciona com o filtro
    const nome = document.getElementById("filtro-nome").value;
    const data = document.getElementById("filtro-data").value;
    const query = new URLSearchParams({
      nome: nome || "",
      data: data || "",
      status: status
    }).toString();
    window.location.href = `?${query}`;
  });
});


});
