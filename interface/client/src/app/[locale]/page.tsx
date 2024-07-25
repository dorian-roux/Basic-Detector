// --------------------- //
// LOCALE | LANDING PAGE //
// --------------------- //

// - Client-Side Rendering - //
"use client"; 

// - Imports - //
// -- Packages and Components -- //
import { redirect } from 'next/navigation';

// - Function | Locale Landing Page - //
export default function LocaleLandingPage() {
  redirect('/basic-detector');
};