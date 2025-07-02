document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');  
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'pt-br',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    events: {
      url: '/eventos/',
      failure: function() {
        alert('Erro ao carregar eventos!');
      }
    },
    eventClick: function(info) {
      // Exemplo: abrir modal com detalhes
      const event = info.event;
      const extendedProps = event.extendedProps;
      
      alert(`
        Obra: ${event.title}\n
        Data: ${event.start.toLocaleString()}\n
        ID Agendamento: ${extendedProps.agendamento_id}
      `);

    },
    eventTimeFormat: {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    },
    navLinks: true,
    editable: true,
    dayMaxEvents: true
  });

  calendar.render();
});