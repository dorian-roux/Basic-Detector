// -------------------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | HOOKS / USE_THEME_SWITCHER //
// -------------------------------------------------------- //

// Client-Side Rendering //
"use client"; 

// Imports //
// - Packages - //
import { useEffect, useState } from 'react'


// Function | Use Theme Switcher //
export default function UseThemeSwitcher() {
    // Variables & States //
    const preferDarkQuery = '(prefers-color-scheme: dark)';    
    const [mode, setMode] = useState("")
    
    // UseEffect //
    // - Handle Theme Change - //
    useEffect(() => {
        const mediaQuery = window.matchMedia(preferDarkQuery);
        const userPreference = window.localStorage.getItem('theme');
        const handleThemeChange = () => {
            if (userPreference) {
                let check = userPreference === "dark" ? "dark" : "light";
                setMode(check);
                if (check === "dark") { document.documentElement.classList.add("dark"); } 
                else { document.documentElement.classList.remove("dark"); } 
            }else {
                let check = mediaQuery.matches ? "dark" : "light";
                setMode(check);
                window.localStorage.setItem('theme', check);
                if (check === "dark") { document.documentElement.classList.add("dark"); } 
                else { document.documentElement.classList.remove("dark"); }
            };
        };

        handleThemeChange();
        mediaQuery.addEventListener('change', handleThemeChange);
        return () => mediaQuery.removeEventListener('change', handleThemeChange);
    }, [])

    // - Mode Change - //
    useEffect(() => {
        if (mode === "dark") {
            window.localStorage.setItem('theme', "dark");
            document.documentElement.classList.add("dark");
        };
        if (mode === "light"){
            window.localStorage.setItem('theme', "light");
            document.documentElement.classList.remove("dark");
        };
    }, [mode])

    // Return //
    return [mode, setMode] as const;
};