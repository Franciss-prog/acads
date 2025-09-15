//  projectData
const projects = [
  {
    name: "Listify",
    description:
      "Listify is a secure web app to keep you organized. It uses login and registration to protect your tasks and saves them in a reliable database, so nothing is lost. Manage your to-do lists anytime, anywhere with ease!",
    sourceCode:
      "https://github.com/Franciss-prog/web-app-projects/tree/main/Listify",
    livePreview: "https://production-omega-rust.vercel.app/",
    image:
      "https://images.unsplash.com/photo-1644329843283-640d00509d43?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dG8lMjBkbyUyMGxpc3R8ZW58MHx8MHx8fDA%3D",
  },
  {
    name: "Brewcode",
    description:
      "BrewCode is a coffee shop web app that offers various types of coffee. It’s designed to be user-friendly and ensures secure, private orders for a smooth experience.",
    sourceCode:
      "https://github.com/Franciss-prog/web-app-projects/tree/main/prisma-bun-brewcode",

    image:
      "https://i.pinimg.com/736x/d9/ec/e7/d9ece738e31bf788ae82db250b2316bc.jpg",
  },
  {
    name: "Portolio",
    description:
      "This is my portfolio website where I showcase my work as a frontend developer. It includes sections about me, my skills, my projects, and a contact form to reach out.",
    sourceCode:
      "https://github.com/Franciss-prog/web-app-projects/tree/main/portfolio",
    livePreview: "https://franciss-prog.vercel.app/",
    image:
      "https://imgs.search.brave.com/XZOHArSHhHMhOKE95mfQ-mBVu0c2BCa9YA9jEvMCV8s/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cHJvZC53ZWJzaXRl/LWZpbGVzLmNvbS82/MDA5ZWM4Y2RhN2Yz/MDU2NDVjOWQ5MWIv/NjAxMDdmMWViNGJh/NDUxODk5ODQzMDQy/XzYwMDIwODZmNzJi/NzI3NjQ1ODAxZTQ2/MV9waG90b2dyYXBo/b3MuanBlZw",
  },
];

// loaded functions
document.addEventListener("DOMContentLoaded", () => {
  initializeNavbarStyling();
  setupToggleNavbar();
  validatePathname();
  styleTechStack();
  initializePortfolio();
  styleSocialMedia();
});

//  function for initializing navbar styling
const initializeNavbarStyling = () => {
  const links = document.querySelectorAll("nav ul li a");
  const { pathname } = window.location;
  const currentPath = pathname;

  // mapping the data
  links.forEach((link) => {
    const href = link.getAttribute("href");
    if (href === currentPath || currentPath.includes(href)) {
      link.classList.add("underline");
      link.classList.add("text-violet-400");
      document.title = link.innerHTML;
    } else {
      link.classList.remove("underline");
      link.classList.add("hover:underline");
      link.classList.add("hover:text-violet-400");
    }
  });
};

// function for setting up toggle navbar
const setupToggleNavbar = () => {
  const toggleNavbarButton = document.getElementById("toggleNavbar");

  toggleNavbarButton?.addEventListener("click", () => {
    Swal.fire({
      title: "Where did you want to go?",
      html: `
        <div class="flex flex-col gap-2 items-start" id="togglenavbarContent">
          <a href="index.html" class="hover:underline max-md:text-md max-sm:text-sm">---> Home</a>  
          <a href="about.html" class="hover:underline max-md:text-md max-sm:text-sm">---> About</a>  
          <a href="portfolio.html" class="hover:underline max-md:text-md max-sm:text-sm">---> Portfolio</a>  
          <a href="contact.html" class="hover:underline max-md:text-md max-sm:text-sm">---> Contacts</a>  
        </div>
      `,
      showConfirmButton: false,
      customClass: {
        popup: "bg-dark text-white",
        title: "text-lg",
      },
      didOpen: () => {
        // Reapply styles for the links inside #togglenavbarContent
        const toggleNavbarLinks = document.querySelectorAll(
          "#togglenavbarContent a"
        );

        toggleNavbarLinks.forEach((toggleNavbarlink) => {
          const toggleNavbarhref = toggleNavbarlink.getAttribute("href");
          const { pathname: currentPath } = window.location;

          if (
            toggleNavbarhref === currentPath ||
            currentPath.includes(toggleNavbarhref)
          ) {
            toggleNavbarlink.classList.add("underline");
            toggleNavbarlink.classList.add("text-violet-400");
          } else {
            toggleNavbarlink.classList.remove("underline");
            toggleNavbarlink.classList.add("hover:underline");
            toggleNavbarlink.classList.add("hover:text-violet-400");
          }
        });
      },
    });
  });
};

// function for validation in pathname
const validatePathname = () => {
  // Get the current pathname and origin
  const { pathname, origin } = window.location;

  // Handle local development path validation (e.g., localhost)
  if (pathname === "/") {
    window.location.href = "index.html";
  }

  // Extract the base path (repo name) for GitHub Pages from the origin
  const basePath = window.location.origin.includes("github.io")
    ? window.location.origin.split("/")[3]
    : "";

  // If the pathname is the root or includes the base path, redirect to index.html
  if (pathname === `/${basePath}/` || pathname.includes(`/${basePath}/`)) {
    window.location.href = "index.html";
  }
};

// function for styling tech stack links
const styleTechStack = () => {
  const stacks = document.querySelectorAll("#techstack a");
  stacks.forEach((stack) => stack.classList.add("hover:text-orange-400"));
};
// function for styling social media
const styleSocialMedia = () => {
  const socials = document.querySelectorAll("#socials a");
  socials.forEach((social) => social.classList.add("hover:text-orange-400"));
};

//  function for initializing portfolio
const initializePortfolio = () => {
  const techStackContainer = document.getElementById("portfolio");

  projects.forEach(({ name, description, image, livePreview, sourceCode }) => {
    const button = document.createElement("button");
    button.className = "flex flex-col items-center";
    button.id = "showProject";
    button.innerHTML = `
    <div class="flex flex-col items-center hover:text-orange-500">
        <i class="bi bi-folder"></i>
      <span class=' text-3xl max-md:text-xl'>${name}</span>
    </div>
    `;

    button?.addEventListener("click", () => {
      Swal.fire({
        html: `
           <div class="flex flex-col items-start text-light gap-5 text-left text-xl max-md:text-md max-sm:text-sm h-auto ">
           <img src="${image}" class=" aspect-video h-[200px] w-full max-md:h-[170px]"/>
                  <span>${name}</span>
                  <span>${description}</span>
                  <div class="flex gap-10 items-center">
                    <a href="${sourceCode}" target="_blank" class="hover:text-orange-500">[source Code]</a>
                   ${
                     livePreview
                       ? `<a href="${livePreview}" target="_blank" id="live" class="hover:text-orange-500">Live Preview</a>`
                       : `<span class=" cursor-not-allowed text-red-600 underline">Under Construction</span>`
                   }
                  </div>
          </div>
        `,
        imageAlt: "Custom image",
        customClass: {
          popup: "bg-dark text-white max-md:",
          title: "text-lg flex items-start",
          image: "max-md:h-[150px] max-md:w-[300px]",
        },
        showConfirmButton: false,
      });
    });
    techStackContainer?.appendChild(button);
  });
};
