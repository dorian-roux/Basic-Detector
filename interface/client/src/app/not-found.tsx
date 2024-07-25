// ---------------- //
// ROOT | NOT FOUND //
// ---------------- //

// Client-Side Rendering //
'use client';


// Imports //
// - Packages and Components - //
import Error from 'next/error';


// Function | Root Not Found //
export default function NotFound() {
  return (
    <Error statusCode={404} />
  );
};