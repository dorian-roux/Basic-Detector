// ----------------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | PAGES / LAYOUT / FOOTER //
// ----------------------------------------------------- //

// Client-Side Rendering //
"use client"; 

// Imports //
// - Packages - //
import { motion } from 'framer-motion'
import Link from 'next/link'

// - Components - //
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import { SynthesizePaths } from  '@/components/basic-detector/Navigation';

// - Styles - //
import '@/styles/basic-detector/layout.scss';


// Function | Footer //
export default function Footer({contentFooter}: {contentFooter: any}) {
    // States & Variables //
    const { websiteURL } = SynthesizePaths()
    
    // Return //
    return (
        <footer id="md-footer">
            <div className='parent-container'>
                <span>{new Date().getFullYear()} &copy; {GetValueFromKeys(contentFooter, "Copyright")}.</span>
                <div className='child-container'>
                    <p>{GetValueFromKeys(contentFooter, "Build")}</p>
                    <motion.div className='link-website-container' whileHover={{y: -2}} whileTap={{scale: 0.9}}>
                        <Link href={websiteURL} className='link'>
                            {GetValueFromKeys(contentFooter, "Author")}
                        </Link>    
                    </motion.div>
                </div>
            </div>
        </footer>
    );
};