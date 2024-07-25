// ----------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | TRANSITION_EFFECT //
// ----------------------------------------------- //

// Client-Side Rendering //
"use client"; 


// Imports //
// - Packages - //
import React from 'react'
import { motion } from 'framer-motion'


// Function | Transition Effect //
export default function TransitionEffect(){
    // Return //
    return (
    <>  
    <div id='transition-effect'>
        <motion.div 
            className='fixed top-0 bottom-0 right-full w-screen h-screen z-30'
            initial={{x:"100%", width:"100%"}}
            animate={{x:"0%", width:"0%"}}
            exit={{x:["0%", "100%"], width:["0%", "100%"]}}
            transition={{duration: 0.25}}
        />
        <motion.div 
            className='fixed top-0 bottom-0 right-full w-screen h-screen z-20 bg-light'
            initial={{x:"100%", width:"100%"}}
            animate={{x:"0%", width:"0%"}}
            transition={{delay:0.2, duration: 0.5, ease:"easeInOut"}}
        />
        <motion.div 
            className='fixed top-0 bottom-0 right-full w-screen h-screen z-10 bg-dark'
            initial={{x:"100%", width:"100%"}}
            animate={{x:"0%", width:"0%"}}
            transition={{delay:0.4, duration: 0.5, ease:"easeInOut"}}
        />
    </div>
    </>
  );
};