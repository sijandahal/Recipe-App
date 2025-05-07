import { useState, useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "react-toastify/dist/ReactToastify.css";
import config from "../../config";
import gsap from "gsap";

export default function SigninPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Set initial states
    gsap.set(".login-logo", { opacity: 0, y: -50 });
    gsap.set(".login-title", { opacity: 0, x: -50 });
    gsap.set(".login-subtitle", { opacity: 0, x: -50 });
    gsap.set(".login-form", { opacity: 0, y: 50 });
    gsap.set(".login-image", { opacity: 0, scale: 1.1 });

    // Create timeline
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Animate logo
    tl.to(".login-logo", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "elastic.out(1, 0.5)"
    });

    // Animate title
    tl.to(".login-title", {
      opacity: 1,
      x: 0,
      duration: 0.8
    }, "-=0.5");

    // Animate subtitle
    tl.to(".login-subtitle", {
      opacity: 1,
      x: 0,
      duration: 0.8
    }, "-=0.6");

    // Animate form
    tl.to(".login-form", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "back.out(1.7)"
    }, "-=0.4");

    // Animate background image
    tl.to(".login-image", {
      opacity: 1,
      scale: 1,
      duration: 1.5,
      ease: "power2.out"
    }, "-=1");

    // Add hover animations to form elements
    const formElements = document.querySelectorAll(".login-form input, .login-form button");
    formElements.forEach(element => {
      element.addEventListener("mouseenter", () => {
        gsap.to(element, {
          scale: 1.02,
          duration: 0.3,
          ease: "power2.out"
        });
      });
      element.addEventListener("mouseleave", () => {
        gsap.to(element, {
          scale: 1,
          duration: 0.3,
          ease: "power2.out"
        });
      });
    });

    // Cleanup
    return () => {
      formElements.forEach(element => {
        element.removeEventListener("mouseenter", () => {});
        element.removeEventListener("mouseleave", () => {});
      });
    };
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(`${config.backendUrl}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (data.token) {
        localStorage.setItem("token", data.token);
        // Animate out before navigation
        gsap.to(".login-form", {
          opacity: 0,
          y: -50,
          duration: 0.5,
          ease: "power2.in",
          onComplete: () => {
            setTimeout(() => navigate("/dashboard"), 500);
          }
        });
        toast.success("Login successful!");
        localStorage.setItem("email", email);
      } else {
        toast.error(data.error || "Login failed");
      }
    } catch (err) {
      toast.error("Server error. Please try again.");
    }
  };

  return (
    <div className="flex min-h-screen w-full overflow-hidden">
      {/* Left - Login Form */}
      <div className="flex flex-1 flex-col justify-center px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
        <div className="mx-auto w-full max-w-sm lg:w-96">
          <div>
            <div className="flex items-center w-[150px] login-logo">
              <a href="/" className="">
                <img alt="Logo" src="./logo.jpg" className="w-auto h-20 object-contain" />
              </a>
            </div>
            <h2 className="mt-8 text-2xl font-bold tracking-tight text-gray-900 login-title">
              Sign in to your account
            </h2>
            <p className="mt-2 text-sm text-gray-500 login-subtitle">
              Don't have an account?{" "}
              <a href="/signup" className="font-semibold text-primary hover:underline">
                Sign up here
              </a>
            </p>
          </div>

          <div className="mt-10">
            <form onSubmit={handleLogin} className="space-y-6 login-form">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-900">
                  Email address
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="mt-2 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-900">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  required
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="mt-2 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="flex items-center justify-between">
                <label className="flex items-center gap-2 text-sm text-gray-900">
                  <input type="checkbox" className="h-4 w-4 rounded border-gray-300" />
                  Remember me
                </label>
              </div>

              <button
                type="submit"
                className="login-button text-white hover:text-gray-300 transition-colors duration-200 group relative flex h-[calc(48px+8px)] items-center justify-center text-center rounded-full bg-primary py-1 pl-14 pr-14 font-medium"
              >
                Sign in
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Right - Image */}
      <div className="relative hidden w-0 flex-1 lg:block">
        <img
          className="absolute inset-0 h-full w-full object-cover login-image"
          src="https://images.unsplash.com/photo-1730900737724-5b752e1ed3dd?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          alt="Login background"
        />
      </div>

      {/* Toast container */}
      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  );
}
