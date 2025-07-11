document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    initialView: 'dayGridMonth',
    height: '100%',
    slotMinTime: '08:00',
    slotMaxTime: '20:00',
    locale: 'pt-br',
    navLinks: true,
    editable: true,
    selectable: true,
    nowIndicator: true,
    events: '/agenda/eventos/',

    eventClick: function(info) {
      const event = info.event;
      const partes = event.title.split(' - ');
      const nomeObra = partes[0];
      const nomeMontador = partes[1] || 'Indefinido';

      document.getElementById('modalTitulo').innerText = 'Detalhes da Entrega';
      document.getElementById('modalData').innerText = new Date(event.start).toLocaleString('pt-BR');
      document.getElementById('modalMontador').innerText = nomeMontador;
      document.getElementById('modalObra').innerText = nomeObra;

      document.getElementById('eventoModal').style.display = 'block';
    }
  });

  calendar.render();
});

// Função para fechar o modal
function fecharModal() {
  document.getElementById('eventoModal').style.display = 'none';
}
