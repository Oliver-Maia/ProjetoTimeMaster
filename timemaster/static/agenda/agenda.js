
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
    initialDate: '2025-07-01',
    navLinks: true, 
    editable: true,
    selectable: true,
    nowIndicator: true,
    events: '/agenda/eventos/',

  });

  calendar.render();
});