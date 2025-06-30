// JavaScript for handling sidebar and user dropdown interactions

document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById('sidebar');
  const content = document.getElementById('content');
  const topbar = document.querySelector('.topbar');
  const openSidebarBtn = document.getElementById('openSidebar');
  const toggles = document.querySelectorAll('.toggle-submenu');
  const userButton = document.getElementById('userButton');
  const userDropdown = document.getElementById('userDropdown');

  // Sidebar toggle
  if (sidebar && content && topbar && openSidebarBtn) {
    openSidebarBtn.addEventListener('click', () => {
      sidebar.classList.toggle('sidebar-open');
      content.classList.toggle('shifted');
      topbar.classList.toggle('shifted');
       console.log('Sidebar toggled')
    });
  }

  // User dropdown toggle
  if (userButton && userDropdown) {
    userButton.addEventListener('click', (e) => {
      e.stopPropagation(); // impede o clique de fechar imediatamente
      userDropdown.classList.toggle('show');
    });

    // Fecha o dropdown se clicar fora
    document.addEventListener('click', (e) => {
      if (!userButton.contains(e.target)) {
        userDropdown.classList.remove('show');
      }
    });
  }
  // Toggle submenu visibility
  toggles.forEach(toggle => {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();
      const item = this.closest('.sidebar-item');
      item.classList.toggle('active');
      });
  });
});
