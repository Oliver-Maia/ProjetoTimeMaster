document.addEventListener('DOMContentLoaded', function() {
 
  // CÓDIGO DO CARROSSEL (mantido do seu original)
  const carrosselContainer = document.querySelector('.carrossel-container');
  const carrossel = document.querySelector('.carrossel');
  const items = document.querySelectorAll('.carrossel-item');
  const btnPrev = document.querySelector('.carrossel-btn.prev');
  const btnNext = document.querySelector('.carrossel-btn.next');
  
  // Configurações
  let currentIndex = 0;
  let visibleItems = 3;
  let itemWidth = 0;
  
  function calculateVisibleItems() {
    const containerWidth = carrosselContainer.offsetWidth;
    const firstItem = items[0];
    if (!firstItem) return;
    
    itemWidth = firstItem.offsetWidth + 20;
    visibleItems = Math.floor(containerWidth / itemWidth);
    visibleItems = Math.max(1, visibleItems);
  }
  
  function updateCarrossel() {
    calculateVisibleItems();
    const maxIndex = Math.max(items.length - visibleItems, 0);
    currentIndex = Math.min(currentIndex, maxIndex);
    currentIndex = Math.max(currentIndex, 0);
    
    const offset = -currentIndex * itemWidth;
    carrossel.style.transform = `translateX(${offset}px)`;
    
    btnPrev.style.display = currentIndex === 0 ? 'none' : 'flex';
    btnNext.style.display = currentIndex >= maxIndex ? 'none' : 'flex';
  }
  
  btnPrev.addEventListener('click', function() {
    currentIndex--;
    updateCarrossel();
  });
  
  btnNext.addEventListener('click', function() {
    currentIndex++;
    updateCarrossel();
  });
  
  calculateVisibleItems();
  updateCarrossel();
  
  window.addEventListener('resize', function() {
    updateCarrossel();
  });


  // NOVO CÓDIGO PARA A TIMELINE INTERATIVA
  const modal = document.getElementById('eventModal');
  const closeModal = document.querySelector('.close-modal');
  
  // Função para abrir o modal com os detalhes do agendamento
  function openEventModal(details) {
    // Preencher os dados no modal
    document.querySelector('.modal-title').textContent = `${details.obra} (${details.numero})`;
    document.querySelector('.modal-cliente').textContent = details.cliente || 'Não informado';
    document.querySelector('.modal-hora').textContent = details.hora || 'Não agendado';
    document.querySelector('.modal-endereco').textContent = details.endereco || 'Não informado';
    document.querySelector('.modal-montador').textContent = details.montador || 'Não designado';
    
    // Exibir o modal
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Impede scroll da página
  }
  
  // Fechar o modal
  function closeEventModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restaura scroll da página
  }
  
  // Adicionar eventos de clique para cada item da timeline
  document.querySelectorAll('.timeline-event:not(.empty)').forEach(eventElement => {
    eventElement.addEventListener('click', function() {
      // Obter os dados do atributo data-details
      const detailsJson = this.getAttribute('data-details');
      
      try {
        const details = JSON.parse(detailsJson);
        openEventModal(details);
      } catch (error) {
        console.error('Erro ao analisar dados do evento:', error);
        alert('Ocorreu um erro ao carregar os detalhes deste agendamento.');
      }
    });
  });
  
  // Fechar modal ao clicar no X
  closeModal.addEventListener('click', closeEventModal);
  
  // Fechar modal ao clicar fora do conteúdo
  modal.addEventListener('click', function(event) {
    if (event.target === modal) {
      closeEventModal();
    }
  });
  
  // Fechar modal com tecla ESC
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && modal.style.display === 'flex') {
      closeEventModal();
    }
  });

 
});