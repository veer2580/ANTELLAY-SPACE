
    const menuToggle = document.querySelector(".menu-toggle");
    const mobileMenu = document.querySelector("#mobile-menu");
    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener("click", () => {
        const isOpen = mobileMenu.classList.toggle("open");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
      });
      mobileMenu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
          mobileMenu.classList.remove("open");
          menuToggle.setAttribute("aria-expanded", "false");
        });
      });
    }

    const revealItems = document.querySelectorAll(".tile, .panel, .engine, .video-band, .stat-card, .why-copy, .why-card, footer, .product-hero, .diagram-container, .card, .center-globe-wrapper, .process-flow, .built-to-connect, .os-cta, .footer-hero, .os-header, .source, .center-column, .right-column, .fragment-stack, .core, .earth, .intel");

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px 18% 0px" });

    const viewportHeight = window.innerHeight;
    let delayIndex = 0;

    revealItems.forEach((item) => {
      const rect = item.getBoundingClientRect();
      if (rect.top < viewportHeight) {
        item.classList.add("is-visible");
      } else {
        item.classList.add("reveal");
        item.style.transitionDelay = `${Math.min(delayIndex * 45, 360)}ms`;
        revealObserver.observe(item);
      }
      delayIndex += 1;
    });

    const videoModal = document.querySelector("#space-video-modal");
    const spaceVideo = document.querySelector("#space-video");
    const openVideoButtons = document.querySelectorAll(".big-play, .watch");
    const closeVideoButton = document.querySelector(".close-video");
    let lastFocusedElement = null;

    const openVideo = () => {
      lastFocusedElement = document.activeElement;
      videoModal.classList.add("is-open");
      videoModal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      spaceVideo.currentTime = 0;
      closeVideoButton.focus();
      const playAttempt = spaceVideo.play();
      if (playAttempt) {
        playAttempt.catch(() => {
          spaceVideo.controls = true;
        });
      }
    };

    const closeVideo = () => {
      videoModal.classList.remove("is-open");
      videoModal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      spaceVideo.pause();
      if (lastFocusedElement) lastFocusedElement.focus();
    };

    openVideoButtons.forEach((button) => button.addEventListener("click", openVideo));
    closeVideoButton.addEventListener("click", closeVideo);
    videoModal.addEventListener("click", (event) => {
      if (event.target === videoModal) closeVideo();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && videoModal.classList.contains("is-open")) closeVideo();
    });

    const scrollTo = (selector) => {
      const target = document.querySelector(selector);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    };

    const exploreButton = document.querySelector(".hero-actions .cta");
    if (exploreButton) exploreButton.addEventListener("click", () => scrollTo("#spaceos"));

    const watchDemoButton = document.querySelector(".hero-actions .cta.ghost");
    if (watchDemoButton) watchDemoButton.addEventListener("click", openVideo);

    const contactButton = document.querySelector(".contact");
    if (contactButton) contactButton.addEventListener("click", () => scrollTo("#contact"));

    const learnButton = document.querySelector(".learn");
    if (learnButton) learnButton.addEventListener("click", () => scrollTo("#spaceos"));

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", (event) => {
        const href = anchor.getAttribute("href");
        if (href === "#" || href.length < 2) return;
        const target = document.querySelector(href);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });

    const crossfadeLoops = document.querySelectorAll(".tile-video-wrap, .why-orbit");

    crossfadeLoops.forEach((wrap) => {
      const videos = wrap.querySelectorAll("video");
      if (videos.length < 2) return;
      const [primary, alt] = videos;
      const switchTo = (next, outgoing) => {
        next.currentTime = 0;
        next.style.opacity = 1;
        outgoing.style.opacity = 0;
        next.play().catch(() => {});
      };
      primary.addEventListener("ended", () => switchTo(alt, primary));
      alt.addEventListener("ended", () => switchTo(primary, alt));
      alt.style.opacity = 0;
      alt.muted = true;
      primary.play().catch(() => {});
    });

