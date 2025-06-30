document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
  if (!calendarEl) {
    console.error("Elemento #calendar não encontrado!");
    return;
  }

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'pt-br',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,listWeek'
    },
    events: '/agenda/eventos/',
    eventClick: function(info) {
      alert('Evento: ' + info.event.title);
    }
  });

  calendar.render();
});
