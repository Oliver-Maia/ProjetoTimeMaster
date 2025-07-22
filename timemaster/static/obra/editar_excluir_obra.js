document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const obrasList = document.getElementById('obras-list');
    const filtroStatus = document.getElementById('filtro-status');
    const btnFiltrar = document.getElementById('btn-filtrar');
    const modalEdicao = document.getElementById('modal-edicao');
    const modalConfirmacao = document.getElementById('modal-confirmacao');
    const closeModal = document.querySelector('.close');
    const formEdicao = document.getElementById('form-edicao');
    const btnConfirmarExclusao = document.getElementById('btn-confirmar-exclusao');
    const btnCancelarExclusao = document.getElementById('btn-cancelar-exclusao');
    const urlParams = new URLSearchParams(window.location.search);
    const statusParam = urlParams.get('status');
    
    // Variáveis globais
    let obras = [];
    let obraParaExcluir = null;
    
    // Carregar obras
    async function carregarObras(status = '') {
    try {
        // Mostrar loading
        obrasList.innerHTML = '<tr><td colspan="6">Carregando...</td></tr>';
        
        const response = await fetch(`/obras/api/listar/?status=${status}`);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const obrasData = await response.json();
        let obrasFiltradas = obrasData;
        
        // Filtro adicional no cliente para pendentes
        if (status === 'pendente') {
            obrasFiltradas = obrasData.filter(obra => !obra.tem_agendamento);
        }
        
        renderizarObras(obrasFiltradas);
        
        // Atualizar filtro ativo visualmente
        document.querySelectorAll('.filtro-link').forEach(link => {
            link.classList.toggle('active', link.getAttribute('data-status') === status);
        });
        
    } catch (error) {
        console.error('Erro ao carregar obras:', error);
        obrasList.innerHTML = '<tr><td colspan="6">Erro ao carregar dados</td></tr>';
    }
}
    // Renderizar obras na tabela
    function renderizarObras(obrasParaRenderizar) {
        obrasList.innerHTML = '';
        
        obrasParaRenderizar.forEach(obra => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${obra.nome}</td>
                <td>${obra.numero || '-'}</td>
                <td>${obra.endereco || '-'}</td>
                <td>${obra.status}</td>
                <td>${obra.data_agendamento ? formatarData(obra.data_agendamento) : '-'}</td>
                <td>
                    <button class="btn-action btn-edit" data-id="${obra.id}">Editar</button>
                    ${!obra.excluido ? `<button class="btn-action btn-delete" data-id="${obra.id}">Excluir</button>` : ''}
                </td>
            `;
            obrasList.appendChild(tr);
        });
        
        // Adicionar eventos aos botões
        document.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', abrirModalEdicao);
        });
        
        document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
            obraParaExcluir = parseInt(e.target.getAttribute('data-id'));
            modalConfirmacao.style.display = 'block';
                });
        });
    }
    
    // Formatador de status
    function formatarStatus(status) {
        const statusMap = {
            'pendente': 'Pendente',
            'em_andamento': 'Em Andamento',
            'realizado': 'Realizado',
            'cancelada': 'Cancelada',
            'excluida': 'Excluída'
        };
        return statusMap[status] || status;
    }
    
    // Formatador de data
    function formatarData(dataString) {
        const data = new Date(dataString);
        return data.toLocaleDateString('pt-BR') + ' ' + data.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'});
    }
    
    // Abrir modal de edição
// Função para editar obra
function abrirModalEdicao(e) {
    const obraId = e.target.getAttribute('data-id');
    const obra = obras.find(o => o.id == obraId);
    
    if (obra) {
        document.getElementById('obra-id').value = obra.id;
        document.getElementById('nome').value = obra.nome;
        document.getElementById('numero').value = obra.numero || '';
        document.getElementById('cliente').value = obra.cliente || '';
        document.getElementById('endereco').value = obra.endereco || '';
        document.getElementById('status').value = obra.status;
        
        modalEdicao.style.display = 'block';
    }
}

// Função para excluir obra
function confirmarExclusao() {
    if (!obraParaExcluir) return;
    
    fetch(`/obras/api/obras/${obraParaExcluir}/excluir/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.message || 'Erro ao excluir'); });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Obra excluída com sucesso!');
            fecharModais();
            carregarObras(filtroStatus.value);
        } else {
            throw new Error(data.message || 'Erro ao excluir obra');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert(error.message);
    });
}

// Configuração dos event listeners
document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', abrirModalEdicao);
});

document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', function(e) {
        obraParaExcluir = e.target.getAttribute('data-id');
        modalConfirmacao.style.display = 'block';
    });
});

btnConfirmarExclusao.addEventListener('click', confirmarExclusao);
    
    // Abrir modal de confirmação
    function abrirModalConfirmacao(e) {
        obraParaExcluir = parseInt(e.target.getAttribute('data-id'));
        modalConfirmacao.style.display = 'block';
    }
    
    // Fechar modais
    function fecharModais() {
        modalEdicao.style.display = 'none';
        modalConfirmacao.style.display = 'none';
    }
    
    // Event Listeners
    btnFiltrar.addEventListener('click', (e) => {
        e.preventDefault();
        carregarObras(filtroStatus.value);
        history.pushState({}, '', `?status=${filtroStatus.value}`);
    });
    
    closeModal.addEventListener('click', fecharModais);
    
    window.addEventListener('click', (e) => {
        if (e.target === modalEdicao || e.target === modalConfirmacao) {
            fecharModais();
        }
    });
    
    // Salvar edição
    formEdicao.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const obraId = document.getElementById('obra-id').value;
        const obraData = {
            nome: document.getElementById('nome').value,
            numero: document.getElementById('numero').value,
            cliente: document.getElementById('cliente').value, 
            endereco: document.getElementById('endereco').value,
            status: document.getElementById('status').value
        };
        
        fetch(`/obras/api/obras/${obraId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(obraData)
        })
        .then(response => {
            if (!response.ok) throw new Error('Erro na resposta do servidor');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Obra atualizada com sucesso!');
                fecharModais();
                carregarObras(filtroStatus.value);
            } else {
                throw new Error(data.message || 'Erro ao atualizar obra');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao atualizar obra: ' + error.message);
        });
    });
    
    // Confirmar exclusão
    btnConfirmarExclusao.addEventListener('click', function() {
        if (!obraParaExcluir) return;
        
        fetch(`/obras/api/obras/${obraParaExcluir}/excluir/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Erro na resposta do servidor');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Obra excluída com sucesso!');
                fecharModais();
                carregarObras(filtroStatus.value);
            } else {
                throw new Error(data.message || 'Erro ao excluir obra');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao excluir obra: ' + error.message);
        });
    });
    
    btnCancelarExclusao.addEventListener('click', fecharModais);
    
    // Função auxiliar para pegar CSRF token (Django)
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
    
    // Carregar obras ao iniciar
    carregarObras();
});