document.addEventListener('DOMContentLoaded', function() {
  const carrosselContainer = document.querySelector('.carrossel-container');
  const carrossel = document.querySelector('.carrossel');
  const items = document.querySelectorAll('.carrossel-item');
  const btnPrev = document.querySelector('.carrossel-btn.prev');
  const btnNext = document.querySelector('.carrossel-btn.next');
  
  // Configurações
  let currentIndex = 0;
  let visibleItems = 3; // Quantidade padrão de itens visíveis
  let itemWidth = 0;
  
  // Calcula quantos itens são visíveis com base na largura do container
  function calculateVisibleItems() {
    const containerWidth = carrosselContainer.offsetWidth;
    const firstItem = items[0];
    if (!firstItem) return;
    
    itemWidth = firstItem.offsetWidth + 20; // Largura + margem
    visibleItems = Math.floor(containerWidth / itemWidth);
    
    // Garante pelo menos 1 item visível
    visibleItems = Math.max(1, visibleItems);
  }
  
  // Atualiza a posição do carrossel
  function updateCarrossel() {
    calculateVisibleItems();
    const maxIndex = Math.max(items.length - visibleItems, 0);
    currentIndex = Math.min(currentIndex, maxIndex);
    currentIndex = Math.max(currentIndex, 0);
    
    const offset = -currentIndex * itemWidth;
    carrossel.style.transform = `translateX(${offset}px)`;
    
    // Atualiza visibilidade dos botões
    btnPrev.style.display = currentIndex === 0 ? 'none' : 'flex';
    btnNext.style.display = currentIndex >= maxIndex ? 'none' : 'flex';
  }
  
  // Event listeners
  btnPrev.addEventListener('click', function() {
    currentIndex--;
    updateCarrossel();
  });
  
  btnNext.addEventListener('click', function() {
    currentIndex++;
    updateCarrossel();
  });
  
  // Inicialização
  calculateVisibleItems();
  updateCarrossel();
  
  // Redimensionamento da janela
  window.addEventListener('resize', function() {
    updateCarrossel();
  });
});
  