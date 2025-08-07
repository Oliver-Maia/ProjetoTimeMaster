document.addEventListener('DOMContentLoaded', function() {
    // Configuração do Carrossel
    const carrosselContainer = document.querySelector('.carrossel-container');
    const carrossel = document.querySelector('.carrossel');
    const carrosselItems = document.querySelectorAll('.carrossel-item');
    const btnCarrosselPrev = document.querySelector('.carrossel-btn.prev');
    const btnCarrosselNext = document.querySelector('.carrossel-btn.next');

    // Configuração da Timeline
    const timelineContainer = document.querySelector('.timeline-container');
    const timeline = document.querySelector('.timeline');
    const timelineDays = document.querySelectorAll('.timeline-day');
    const btnTimelinePrev = document.querySelector('.timeline-btn.prev');
    const btnTimelineNext = document.querySelector('.timeline-btn.next');

    // Configurações comuns de carrossel/timeline
    let currentCarrosselIndex = 0;
    let currentTimelineIndex = 0;
    let visibleCarrosselItems = 0;
    let visibleTimelineItems = 0;
    let itemWidth = 0;
    let dayWidth = 0;

    function calculateVisibleItems() {
        // Para o carrossel
        // É crucial verificar se carrosselContainer existe antes de tentar obter offsetWidth
        if (carrosselContainer && carrosselItems.length > 0) {
            itemWidth = carrosselItems[0].offsetWidth + 15; // Ajuste o gap para 15px se for o que você usa no CSS
            visibleCarrosselItems = Math.max(1, Math.floor(carrosselContainer.offsetWidth / itemWidth));
        }

        // Para a timeline
        // É crucial verificar se timelineContainer existe antes de tentar obter offsetWidth
        if (timelineContainer && timelineDays.length > 0) {
            dayWidth = timelineDays[0].offsetWidth + 20; // Ajuste o gap para 20px se for o que você usa no CSS
            visibleTimelineItems = Math.max(1, Math.floor(timelineContainer.offsetWidth / dayWidth));
        }
    }

    // Atualiza o carrossel
    function updateCarrossel() {
        calculateVisibleItems();
        if (carrosselItems.length === 0 || !carrossel) return; // Se não houver itens ou carrossel, sai da função

        const maxIndex = Math.max(carrosselItems.length - visibleCarrosselItems, 0);
        currentCarrosselIndex = Math.min(currentCarrosselIndex, maxIndex);
        currentCarrosselIndex = Math.max(currentCarrosselIndex, 0);

        const offset = -currentCarrosselIndex * itemWidth;
        carrossel.style.transform = `translateX(${offset}px)`;

        // Verifica se os botões existem antes de tentar manipulá-los
        if (btnCarrosselPrev && btnCarrosselNext) {
            btnCarrosselPrev.style.display = currentCarrosselIndex === 0 ? 'none' : 'flex';
            btnCarrosselNext.style.display = currentCarrosselIndex >= maxIndex ? 'none' : 'flex';
        }
    }

    // Atualiza a timeline
    function updateTimeline() {
        calculateVisibleItems();
        if (timelineDays.length === 0 || !timeline) return; // Se não houver dias ou timeline, sai da função

        const maxIndex = Math.max(timelineDays.length - visibleTimelineItems, 0);
        currentTimelineIndex = Math.min(currentTimelineIndex, maxIndex);
        currentTimelineIndex = Math.max(currentTimelineIndex, 0);

        const offset = -currentTimelineIndex * dayWidth;
        timeline.style.transform = `translateX(${offset}px)`;

        // Verifica se os botões existem antes de tentar manipulá-los
        if (btnTimelinePrev && btnTimelineNext) {
            btnTimelinePrev.style.display = currentTimelineIndex === 0 ? 'none' : 'flex';
            btnTimelineNext.style.display = currentTimelineIndex >= maxIndex ? 'none' : 'flex';
        }
    }

    // Event listeners para o carrossel
    if (btnCarrosselPrev && btnCarrosselNext) { // Verifica se os botões foram encontrados
        btnCarrosselPrev.addEventListener('click', function() {
            currentCarrosselIndex--;
            updateCarrossel();
        });

        btnCarrosselNext.addEventListener('click', function() {
            currentCarrosselIndex++;
            updateCarrossel();
        });
    }

    // Event listeners para a timeline
    if (btnTimelinePrev && btnTimelineNext) { // Verifica se os botões foram encontrados
        btnTimelinePrev.addEventListener('click', function() {
            currentTimelineIndex--;
            updateTimeline();
        });

        btnTimelineNext.addEventListener('click', function() {
            currentTimelineIndex++;
            updateTimeline();
        });
    }

    // Inicialização dos carrosséis/timelines
    // É importante chamar updateCarrossel e updateTimeline APÓS todos os elementos terem sido selecionados
    // e suas variáveis definidas.
    updateCarrossel();
    updateTimeline();

    // Re-inicializa ao redimensionar a janela
    window.addEventListener('resize', function() {
        updateCarrossel();
        updateTimeline();
    });

    // --- CÓDIGO DO MODAL MOVIDO PARA DENTRO DE DOMContentLoaded ---

    const modal = document.querySelector('.event-modal');
    const closeModal = document.querySelector('.close-modal');

    // Verifica se o modal e o botão de fechar existem
    if (!modal || !closeModal) {
        console.warn("Elemento .event-modal ou .close-modal não encontrado. Modal pode não funcionar.");
        // Pode ser útil retornar ou desabilitar funcionalidades do modal se os elementos não existirem
    }

    function openEventModal(details) {
        if (!modal) return; // Garante que o modal existe

        // Preencher os dados no modal
        // Certifique-se de que os seletores de classe dentro do modal estão corretos no seu HTML
        const modalTitle = modal.querySelector('.modal-title');
        const modalCliente = modal.querySelector('.modal-cliente');
        const modalHora = modal.querySelector('.modal-hora');
        const modalEndereco = modal.querySelector('.modal-endereco');
        const modalMontador = modal.querySelector('.modal-montador');

        if (modalTitle) modalTitle.textContent = `${details.obra || 'Não informado'} (${details.numero || 'N/A'})`;
        if (modalCliente) modalCliente.textContent = details.cliente || 'Não informado';
        if (modalHora) modalHora.textContent = details.hora || 'Não agendado';
        if (modalEndereco) modalEndereco.textContent = details.endereco || 'Não informado';
        if (modalMontador) modalMontador.textContent = details.montador || 'Não designado';

        // Exibir o modal
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Impede scroll da página
    }

    // Fechar o modal
    function closeEventModal() {
        if (!modal) return; // Garante que o modal existe
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restaura scroll da página
    }

    // Event listeners para fechar o modal
    if (closeModal) {
        closeModal.addEventListener('click', closeEventModal);
    }

    if (modal) { // Verifica se o modal existe antes de adicionar listeners
        modal.addEventListener('click', function(event) {
            if (event.target === modal) { // Clicou na área escura fora do conteúdo
                closeEventModal();
            }
        });
    }

    // Fechar modal com tecla ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal && modal.style.display === 'flex') {
            closeEventModal();
        }
    });

    // --- Event listener para ABRIR o modal quando um evento da timeline é clicado ---
    const timelineEvents = document.querySelectorAll('.timeline-event');
    timelineEvents.forEach(eventElement => {
        eventElement.addEventListener('click', function() {
            // Verifica se o dataset.details existe e é um JSON válido
            try {
                const details = JSON.parse(eventElement.dataset.details);
                openEventModal(details);
            } catch (e) {
                console.error("Erro ao parsear dados do evento da timeline:", e);
                console.log("Dados recebidos:", eventElement.dataset.details);
            }
        });
    });
});