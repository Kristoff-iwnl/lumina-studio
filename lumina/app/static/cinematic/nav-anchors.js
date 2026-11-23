document.addEventListener("DOMContentLoaded", () => {
  const navLinks = document.querySelectorAll(".site-nav a, .site-logo");
  const cinemaSection = document.querySelector(".cinema-scroll");

  navLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (!href) return;

      if (href === "#cinema" || href === "#intro") {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else if (href === "#bridge") {
        e.preventDefault();
        if (cinemaSection) {
          const rect = cinemaSection.getBoundingClientRect();
          const targetY = window.pageYOffset + rect.top + 1100;
          window.scrollTo({ top: targetY, behavior: "smooth" });
        }
      } else if (href === "#bazaar") {
        e.preventDefault();
        if (cinemaSection) {
          const rect = cinemaSection.getBoundingClientRect();
          const targetY = window.pageYOffset + rect.top + 2340;
          window.scrollTo({ top: targetY, behavior: "smooth" });
        }
      } else if (href === "#routes") {
        e.preventDefault();
        if (cinemaSection) {
          const rect = cinemaSection.getBoundingClientRect();
          const targetY = window.pageYOffset + rect.top + 3660;
          window.scrollTo({ top: targetY, behavior: "smooth" });
        }
      } else if (href === "#enquiry" || href === "#contact") {
        e.preventDefault();
        const enquirySec = document.getElementById("enquiry");
        if (enquirySec) {
          enquirySec.scrollIntoView({ behavior: "smooth" });
        }
      }
    });
  });

  const noteBtn = document.querySelector(".note-button");
  if (noteBtn) {
    noteBtn.addEventListener("click", () => {
      const enquirySec = document.getElementById("enquiry");
      if (enquirySec) {
        enquirySec.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
});
