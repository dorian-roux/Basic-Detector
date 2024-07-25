// ------------------------- //
// COMPONENTS | NF_CUSTOM404 //
// ------------------------- //

// Client-Side Rendering //
"use client"; 

// Imports //
// - Packages - //
import { usePathname } from 'next/navigation';


// Function | Custom 404 //
export default function Custom404() {
    // Get the Previous URL //
    let previousURL = usePathname().split('/').slice(0, -1).join('/')
    if ( previousURL === '' ) { previousURL = '/' }

    // Redirect to the Previous URL //
    if ( typeof window !== 'undefined' ) { window.location.href = previousURL }

    // No Render from this Component //
    return null;
};