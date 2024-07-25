// ------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | ICONS / FLAGS //
// ------------------------------------------- //

// Imports //
import * as React from "react";

// - Flags - //
// -- ENGLISH Flag -- //
export const IcEN = ({ className, ...rest }: {className: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 36 36" {...rest} className={`${className}`}>
        <path fill="#00247d" d="M0 9.059V13h5.628zM4.664 31H13v-5.837zM23 25.164V31h8.335zM0 23v3.941L5.63 23zM31.337 5H23v5.837zM36 26.942V23h-5.631zM36 13V9.059L30.371 13zM13 5H4.664L13 10.837z"></path>
        <path fill="#cf1b2b" d="m25.14 23l9.712 6.801a3.977 3.977 0 0 0 .99-1.749L28.627 23zM13 23h-2.141l-9.711 6.8c.521.53 1.189.909 1.938 1.085L13 23.943zm10-10h2.141l9.711-6.8a3.988 3.988 0 0 0-1.937-1.085L23 12.057zm-12.141 0L1.148 6.2a3.994 3.994 0 0 0-.991 1.749L7.372 13z"></path>
        <path fill="#eee" d="M36 21H21v10h2v-5.836L31.335 31H32a3.99 3.99 0 0 0 2.852-1.199L25.14 23h3.487l7.215 5.052c.093-.337.158-.686.158-1.052v-.058L30.369 23H36zM0 21v2h5.63L0 26.941V27c0 1.091.439 2.078 1.148 2.8l9.711-6.8H13v.943l-9.914 6.941c.294.07.598.116.914.116h.664L13 25.163V31h2V21zM36 9a3.983 3.983 0 0 0-1.148-2.8L25.141 13H23v-.943l9.915-6.942A4.001 4.001 0 0 0 32 5h-.663L23 10.837V5h-2v10h15v-2h-5.629L36 9.059zM13 5v5.837L4.664 5H4a3.985 3.985 0 0 0-2.852 1.2l9.711 6.8H7.372L.157 7.949A3.968 3.968 0 0 0 0 9v.059L5.628 13H0v2h15V5z"></path>
        <path fill="#cf1b2b" d="M21 15V5h-6v10H0v6h15v10h6V21h15v-6z"></path>
    </svg>
);

// -- FRENCH Flag -- //
export const IcFR = ({ className, ...rest }: {className: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 36 36" {...rest} className={`${className}`}>
        <path fill="#ed2939" d="M36 27a4 4 0 0 1-4 4h-8V5h8a4 4 0 0 1 4 4z"></path>
        <path fill="#002495" d="M4 5a4 4 0 0 0-4 4v18a4 4 0 0 0 4 4h8V5z"></path>
        <path fill="#eee" d="M12 5h12v26H12z"></path>
    </svg>
);

// -- SPANISH Flag -- //
export const IcES = ({ className, ...rest }: {className: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 36 36" {...rest} className={`${className}`}>
        <path fill="#c60a1d" d="M36 27a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V9a4 4 0 0 1 4-4h28a4 4 0 0 1 4 4z"></path>
        <path fill="#ffc400" d="M0 12h36v12H0z"></path>
        <path fill="#ea596e" d="M9 17v3a3 3 0 1 0 6 0v-3z"></path>
        <path fill="#f4a2b2" d="M12 16h3v3h-3z"></path>
        <path fill="#dd2e44" d="M9 16h3v3H9z"></path>
        <ellipse cx={12} cy={14.5} fill="#ea596e" rx={3} ry={1.5}></ellipse>
        <ellipse cx={12} cy={13.75} fill="#ffac33" rx={3} ry={0.75}></ellipse>
        <path fill="#99aab5" d="M7 16h1v7H7zm9 0h1v7h-1z"></path>
        <path fill="#66757f" d="M6 22h3v1H6zm9 0h3v1h-3zm-8-7h1v1H7zm9 0h1v1h-1z"></path>
    </svg>
);
