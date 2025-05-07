import { useState, useEffect } from "react";
import { Dialog, DialogPanel } from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Button from "../components/Button/Button";
import { useNavigate } from "react-router-dom";
import GroceryForm from "../components/GroceryForm";
import gsap from "gsap";

const Home = () => {
  const navigate = useNavigate();

  const handleRedirectToLogin = () => {
    navigate("/login");
  };

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Set initial states
    gsap.set(".logo", { opacity: 1, y: 0, rotation: 0 });
    gsap.set(".hero-title", { opacity: 1, x: 0 });
    gsap.set(".hero-text", { opacity: 1, y: 0 });
    gsap.set(".hero-button", { opacity: 1, y: 0, scale: 1 });
    gsap.set(".login-button", { opacity: 0, x: 100 });

    // Create a GSAP timeline for better control and sequencing
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Logo animation with rotation
    tl.fromTo(".logo", 
      { opacity: 0, y: -50, rotation: -15 },
      { 
        opacity: 1,
        y: 0,
        rotation: 0,
        duration: 1.2,
        ease: "elastic.out(1, 0.5)"
      }
    );

    // Login button animation
    tl.fromTo(".login-button",
      { opacity: 0, x: 100 },
      {
        opacity: 1,
        x: 0,
        duration: 1,
        ease: "elastic.out(1, 0.5)"
      },
      "-=0.8"
    );

    // Hero title animation
    tl.fromTo(".hero-title",
      { opacity: 0, x: -100 },
      {
        opacity: 1,
        x: 0,
        duration: 1.5,
        ease: "back.out(1.7)"
      },
      "-=0.5"
    );

    // Hero text animation
    tl.fromTo(".hero-text",
      { opacity: 0, y: 50 },
      {
        opacity: 1,
        y: 0,
        duration: 1,
        ease: "power2.out"
      },
      "-=0.8"
    );

    // Button animation
    tl.fromTo(".hero-button",
      { opacity: 0, y: 100, scale: 0.8 },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 1,
        ease: "elastic.out(1, 0.5)"
      },
      "-=0.5"
    );

    // Add a subtle floating animation to the logo
    gsap.to(".logo", {
      y: 10,
      duration: 2,
      repeat: -1,
      yoyo: true,
      ease: "power1.inOut"
    });

    // Add hover animations to both buttons
    const buttons = document.querySelectorAll(".hero-button, .login-button");
    buttons.forEach(button => {
      button.addEventListener("mouseenter", () => {
        gsap.to(button, {
          scale: 1.05,
          duration: 0.3,
          ease: "power2.out"
        });
      });
      button.addEventListener("mouseleave", () => {
        gsap.to(button, {
          scale: 1,
          duration: 0.3,
          ease: "power2.out"
        });
      });
    });

    // Cleanup function
    return () => {
      buttons.forEach(button => {
        button.removeEventListener("mouseenter", () => {});
        button.removeEventListener("mouseleave", () => {});
      });
    };
  }, []);

  return (
    <div className="bg-pink-200 overflow-hidden">
      <header className="fixed inset-x-0 top-0 z-50">
        <nav
          aria-label="Global"
          className="flex items-center justify-between p-12 lg:px-16"
        >
          <div className="flex lg:flex-1">
            <a href="#">
              <span className="sr-only">Forkast</span>
              <img
                alt="Logo"
                src="./logo.jpg"
                className="logo h-40 w-auto relative z-50"
              />
            </a>
          </div>
          <div className="flex lg:hidden">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(true)}
              className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-400"
            >
              <span className="sr-only">Open main menu</span>
              <Bars3Icon aria-hidden="true" className="size-6" />
            </button>
          </div>

          <div className="hidden lg:flex lg:gap-x-8 lg:justify-end">
            <Button 
              onClick={handleRedirectToLogin}
              className="login-button text-white hover:text-gray-300 transition-colors duration-200"
            > 
              Log In 
            </Button>
          </div>
        </nav>
        <Dialog
          open={mobileMenuOpen}
          onClose={setMobileMenuOpen}
          className="lg:hidden"
        >
          <div className="fixed inset-0 z-50" />
          <DialogPanel className="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-gray-900 px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-white/10">
            <div className="flex items-center justify-between">
              <a href="#" className="-m-1.5 p-1.5">
                <span className="sr-only">Your Company</span>
                <img
                  alt="Logo"
                  src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500"
                  className="h-8 w-auto"
                />
              </a>
              <button
                type="button"
                onClick={() => setMobileMenuOpen(false)}
                className="-m-2.5 rounded-md p-2.5 text-gray-400"
              >
                <span className="sr-only">Close menu</span>
                <XMarkIcon aria-hidden="true" className="size-6" />
              </button>
            </div>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/25">
                <div className="py-6">
                  <a
                    href="#"
                    className="-mx-3  p-8 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-white hover:bg-gray-800"
                  >
                    Log in
                  </a>
                </div>
              </div>
            </div>
          </DialogPanel>
        </Dialog>
      </header>

      <div className="relative h-screen w-full overflow-hidden">
        <div className="absolute inset-0 before:bg-[#7f1f2d] before:content-[''] before:opacity-[0.2] before:absolute before:top-0 before:left-0 before:w-full before:h-full">
          <img
            alt="Background"
            src="https://images.unsplash.com/photo-1630445396366-8dea03c85ead?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            className="absolute inset-0 w-full h-full object-cover"
          />
        </div>
        <div className="relative h-full flex items-center justify-center">
          <div className="mx-auto max-w-7xl px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <h1 className="hero-title text-balance text-6xl font-semibold tracking-tight text-white md:text-8xl">
                Welcome to FORKAST
              </h1>
              <p className="hero-text mt-8 text-pretty text-lg font-medium text-gray-400 sm:text-xl/8">
                Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui
                lorem cupidatat commodo. Elit sunt amet fugiat veniam occaecat.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Button
                  className="hero-button"
                  onClick={() => {
                    localStorage.setItem("email", "guest@forkast.ai");
                    localStorage.setItem("token", "guest-session");
                    window.location.href = "/dashboard";
                  }}
                >
                  Get started without login
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
