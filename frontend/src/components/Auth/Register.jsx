import { useState, useEffect } from "react";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "react-toastify/dist/ReactToastify.css";
import config from "../../config";
import axios from "axios";
import gsap from "gsap";
import Button from "../Button/Button";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate(); 

  useEffect(() => {
    // Set initial states
    gsap.set(".register-logo", { opacity: 0, y: -50 });
    gsap.set(".register-title", { opacity: 0, x: -50 });
    gsap.set(".register-subtitle", { opacity: 0, x: -50 });
    gsap.set(".register-form", { opacity: 0, y: 50 });
    gsap.set(".register-image", { opacity: 0, scale: 1.1 });

    // Create timeline
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    // Animate logo
    tl.to(".register-logo", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "elastic.out(1, 0.5)"
    });

    // Animate title
    tl.to(".register-title", {
      opacity: 1,
      x: 0,
      duration: 0.8
    }, "-=0.5");

    // Animate subtitle
    tl.to(".register-subtitle", {
      opacity: 1,
      x: 0,
      duration: 0.8
    }, "-=0.6");

    // Animate form
    tl.to(".register-form", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "back.out(1.7)"
    }, "-=0.4");

    // Animate background image
    tl.to(".register-image", {
      opacity: 1,
      scale: 1,
      duration: 1.5,
      ease: "power2.out"
    }, "-=1");

    // Add hover animations to form elements
    const formElements = document.querySelectorAll(".register-form input, .register-form button");
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
  
  const handleSignup = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    try {
      const res = await axios.post(`${config.backendUrl}/register`, 
        { email, password },
        {
          headers: { 
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          withCredentials: true
        }
      );

      if (res.status === 201) {
        // Animate out before navigation
        gsap.to(".register-form", {
          opacity: 0,
          y: -50,
          duration: 0.5,
          ease: "power2.in",
          onComplete: () => {
            setTimeout(() => navigate("/dashboard"), 500);
          }
        });
        toast.success(res.data.message || "Registration successful!");
        localStorage.setItem("email", email);
      }
    } catch (err) {
      toast.error(err.response?.data?.error || "Server error. Please try again.");
    }
  };

  return (
    <div className="flex min-h-screen w-full overflow-hidden">
      {/* Left - Form */}
      <div className="flex flex-1 flex-col justify-center px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
        <div className="mx-auto w-full max-w-sm lg:w-96">
          <div>
            <div className="flex items-center w-[150px] register-logo">
              <a href="/" className="">
                <img
                  alt="Logo"
                  src="./logo.jpg"
                  className="w-auto h-20 object-contain"
                />
              </a>
            </div>
            <h2 className="mt-8 text-2xl font-bold tracking-tight text-gray-900 register-title">
              Create a new account
            </h2>
            <p className="mt-2 text-sm text-gray-500 register-subtitle">
              Already have an account?{" "}
              <a href="/login" className="font-semibold text-primary hover:underline">
                Sign in here
              </a>
            </p>
          </div>

          <div className="mt-10">
            <form onSubmit={handleSignup} className="space-y-6 register-form">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-900">
                  Email address
                </label>
                <input
                  id="email"
                  type="email"
                  required
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
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="mt-2 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-900">
                  Confirm Password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="mt-2 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <button
                type="submit"
                className="login-button text-white hover:text-gray-300 transition-colors duration-200 group relative flex h-[calc(48px+8px)] items-center justify-center text-center rounded-full bg-primary py-1 pl-14 pr-14 font-medium"
              >
                Sign up
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Right - Image */}
      <div className="relative hidden w-0 flex-1 lg:block">
        <img
          className="absolute inset-0 h-full w-full object-cover register-image"
          src="https://images.unsplash.com/photo-1694923450868-b432a8ee52aa?q=80&w=1972&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          alt="Signup background"
        />
      </div>

      {/* Toast container */}
      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  );
}
