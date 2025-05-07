"use client";

import { useEffect, useState } from "react";
import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  TransitionChild,
} from "@headlessui/react";
import {
  Bars3Icon,
  BellIcon,
  CalendarIcon,
  ChartPieIcon,
  Cog6ToothIcon,
  DocumentDuplicateIcon,
  FolderIcon,
  HomeIcon,
  UsersIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import {
  ChevronDownIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/20/solid";
import GroceryForm from "../GroceryForm";

const navigation = [
  { name: "Dashboard", href: "#", icon: HomeIcon, current: true },
  { name: "Team", href: "#", icon: UsersIcon, current: false },
  { name: "Projects", href: "#", icon: FolderIcon, current: false },
  { name: "Calendar", href: "#", icon: CalendarIcon, current: false },
  { name: "Documents", href: "#", icon: DocumentDuplicateIcon, current: false },
  { name: "Reports", href: "#", icon: ChartPieIcon, current: false },
];
const teams = [
  { id: 1, name: "Heroicons", href: "#", initial: "H", current: false },
  { id: 2, name: "Tailwind Labs", href: "#", initial: "T", current: false },
  { id: 3, name: "Workcation", href: "#", initial: "W", current: false },
];
const userNavigation = [
  { name: "Your profile", href: "#" },
  {
    name: "Sign out",
    href: "#",
    onClick: () => {
      localStorage.removeItem("email");
      localStorage.removeItem("token");
      window.location.href = "/login";
    },
  },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [userEmail, setUserEmail] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    const storedEmail = localStorage.getItem("email");
    if (storedEmail) setUserEmail(storedEmail);
  }, []);

  const handleFetchRecommendations = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/latest-recommendations");
      const data = await response.json();
      setRecommendations(data);
      setShowResults(true);
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    }
  };

  return (
    <div>
      <Dialog open={sidebarOpen} onClose={setSidebarOpen} className="relative z-50 lg:hidden">
        <DialogBackdrop className="fixed inset-0 bg-gray-900/80" />
        <div className="fixed inset-0 flex">
          <DialogPanel className="relative mr-16 flex w-full max-w-xs flex-1 transform bg-indigo-600">
            <TransitionChild>
              <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                <button
                  type="button"
                  onClick={() => setSidebarOpen(false)}
                  className="-m-2.5 p-2.5"
                >
                  <span className="sr-only">Close sidebar</span>
                  <XMarkIcon className="size-6 text-white" />
                </button>
              </div>
            </TransitionChild>
            <div className="flex grow flex-col gap-y-5 overflow-y-auto px-6 pb-4">
              <div className="flex h-16 items-center">
              <img alt="" src="./logo.jpg" className="h-40 w-auto" />
              </div>
              <nav className="flex flex-1 flex-col">
                <ul className="flex flex-1 flex-col gap-y-7">
                  <li>
                    <ul className="-mx-2 space-y-1">
                      {navigation.map((item) => (
                        <li key={item.name}>
                          <a
                            href={item.href}
                            className={classNames(
                              item.current
                                ? "bg-indigo-700 text-white"
                                : "text-indigo-200 hover:bg-indigo-700 hover:text-white",
                              "group flex gap-x-3 rounded-md p-2 text-sm font-semibold"
                            )}
                          >
                            <item.icon
                              className={classNames(
                                item.current
                                  ? "text-white"
                                  : "text-indigo-200 group-hover:text-white",
                                "size-6 shrink-0"
                              )}
                            />
                            {item.name}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </li>
                </ul>
              </nav>
            </div>
          </DialogPanel>
        </div>
      </Dialog>

      {userEmail === "guest@forkast.ai" && (
        <div className="p-3 bg-yellow-100 text-yellow-800 rounded-md text-center">
          You're using Forkast as a guest. Sign up to save your data!
        </div>
      )}

<div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col bg-primary px-6 pb-4">
  <div className="">
    <a href="/" className=" mb-10 h-20">
      <img alt="Logo" src="./logo.jpg" className=" w-auto" />
    </a>
  </div>
        <nav className="flex flex-1 flex-col">
          <ul className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul className="-mx-2 space-y-1">
                {navigation.map((item) => (
                  <li key={item.name}>
                    <a
                      href={item.href}
                      className={classNames(
                        item.current
                          ? "bg-primaryLight text-white"
                          : "text-white hover:bg-primaryLight hover:text-white",
                        "group flex gap-x-3 rounded-md p-2 text-sm font-semibold"
                      )}
                    >
                      <item.icon
                        className={classNames(
                          item.current
                            ? "text-white"
                            : "text-indigo-200 group-hover:text-white",
                          "size-6 shrink-0"
                        )}
                      />
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </li>
          </ul>
        </nav>
      </div>

      <div className="lg:pl-72">
        <div className="sticky top-0 z-40 flex h-16 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:px-6 lg:px-8">
          <button
            type="button"
            onClick={() => setSidebarOpen(true)}
            className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
          >
            <span className="sr-only">Open sidebar</span>
            <Bars3Icon className="size-6" />
          </button>
          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <form className="grid flex-1 grid-cols-1">
              <input
                name="search"
                type="search"
                placeholder="Search"
                aria-label="Search"
                className="col-start-1 row-start-1 block w-full bg-white pl-8 text-sm text-gray-900 outline-none placeholder:text-gray-400"
              />
              <MagnifyingGlassIcon className="pointer-events-none col-start-1 row-start-1 size-5 self-center text-gray-400" />
            </form>
            <div className="flex items-center gap-x-4 lg:gap-x-6">
              <button type="button" className="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500">
                <span className="sr-only">View notifications</span>
                <BellIcon className="size-6" />
              </button>
              <Menu as="div" className="relative">
                <MenuButton className="-m-1.5 flex items-center p-1.5">
                  <span className="sr-only">Open user menu</span>
                  <img
                    src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    alt=""
                    className="size-8 rounded-full bg-gray-50"
                  />
                  <span className="hidden lg:flex lg:items-center">
                    <span className="ml-4 text-sm font-semibold text-gray-900">
                      {userEmail || "Guest"}
                    </span>
                    <ChevronDownIcon className="ml-2 size-5 text-gray-400" />
                  </span>
                </MenuButton>
                <MenuItems className="absolute right-0 z-10 mt-2.5 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
                  {userNavigation.map((item) => (
                    <MenuItem key={item.name}>
                      <a
                        href={item.href}
                        onClick={item.onClick || undefined}
                        className="block px-3 py-1 text-sm text-gray-900 hover:bg-gray-50"
                      >
                        {item.name}
                      </a>
                    </MenuItem>
                  ))}
                </MenuItems>
              </Menu>
            </div>
          </div>
        </div>

        <main className="py-10">
          <div className="px-4 sm:px-6 lg:px-8">
            <h1 className="text-2xl font-bold text-gray-900">
              Welcome, {userEmail === "guest@forkast.ai" ? "Guest" : userEmail} 👋
            </h1>

            <p className="mt-2 text-gray-600">
              This is your Forkast dashboard.
            </p>

            <GroceryForm />

            {/* 🔘 Button to Show Recommendations */}
            <div className="mt-6">
              <button
                onClick={handleFetchRecommendations}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition"
              >
                Show Results
              </button>
            </div>

            {/* 🧾 Display Results */}
            {showResults && (
              
  <div className="">
    
    {showResults && (
  <div className="mt-6 displayresults grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    {recommendations.map((item, index) => (
      <div
        key={index}
        className={classNames(
          "max-w-sm rounded overflow-hidden shadow-lg bg-white transition-transform transform hover:scale-105",
          index % 2 === 0 ? "border-primary border-2" : "border-gray-300"
        )}
      >

        <div className="px-6 py-4">
          <div className={classNames(
            "font-bold text-xl mb-2",
            index % 2 === 0 ? "text-primary" : "text-gray-800"
          )}>
            {item.recipe_name}
          </div>
          <p className="text-sm text-gray-600">Ingredients:</p>
          <ul className="list-disc list-inside text-sm text-gray-800">
            {JSON.parse(item.ingredients).map((ingredient, i) => (
              <li key={i}>{ingredient}</li>
            ))}
          </ul>
          <p className="mt-2 text-sm font-medium text-gray-700">
            Similarity Score: {item.similarity_score.toFixed(3)}
          </p>
        </div>
        <div className="px-6 pt-4 pb-2">
          <span className="inline-block text-white rounded-full px-3 py-1 text-sm font-semibold mr-2 mb-2 bg-primary">
            #recipe
          </span>
          <span className="inline-block text-white rounded-full px-3 py-1 text-sm font-semibold mr-2 mb-2 bg-primary">
            #food
          </span>
          <span className="inline-block text-white rounded-full px-3 py-1 text-sm font-semibold mr-2 mb-2 bg-primary">
            #ingredients
          </span>
        </div>
      </div>
    ))}
  </div>
)}

  </div>
)}

          </div>
        </main>
      </div>
    </div>
  );
}
