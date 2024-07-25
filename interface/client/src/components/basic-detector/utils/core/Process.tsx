// ---------------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | UTILS / CORE / PROCESS //
// ---------------------------------------------------- //

// Client-Side Rendering //
"use client"; 


// Imports //
// - Packages - //
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// - Components - //
import { backendURL } from '@/components/basic-detector/config';
import { AnimatedCircle, AnimatedProgressBar } from '@/components/basic-detector/utils/core/Animations';
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import { IcUploadIcon } from '@/components/basic-detector/icons/Main';



const ProcessVideo = ({contentProcessing, progression}: {contentProcessing: any, progression: number}) => {
    if (progression === 0) {   
        // Phase #1 - Transmit the Video to the Server
        return <AnimatedCircle text={GetValueFromKeys(contentProcessing, 'Upload')} />
    } else if (progression > 0 && progression < 100) {  
        // Phase #2 - Perform the Frame Detection
        return <AnimatedProgressBar text={GetValueFromKeys(contentProcessing, 'Compute')} progress={progression} />
    }else{
        // Phase #3 - Construct the Output Video and Transmit it to the Client
        return <AnimatedCircle text={GetValueFromKeys(contentProcessing, 'Build')} />
    };
};



interface ProcessProps {
    contentCore: any;
    weights: any;
    listIpts: any;
    setListIpts: any;
    setListOutpts: any;
    isFinished: any;
    setIsFinished: any;
}

// Function | Core //
export default function Process({contentCore, weights, listIpts, setListIpts, setListOutpts, isFinished, setIsFinished}: ProcessProps) {
    // Variables //
    const [isProcessing, setIsProcessing] = useState<boolean>(false);
    const [crntProcessFile, setCrntProcessFile] = useState<string>('');
    const [startVideoProcess, setStartVideoProcess] = useState<boolean>(false);
    const [prgsVideo, setPrgsVideo] = useState<number>(0);
        

    // Use Effect //
    useEffect(() => {
        // -- Perform the Video Detection -- //
        const performVideoDetection = async (file: any) => {
            const formData = new FormData();
            formData.append('video', file);
            try {
                const response = await axios.post(`${backendURL}/source/video/launch-process`, {'weights': weights}, {headers: {'Content-Type': 'application/json'}});
                if (response.status !== 200) { return undefined };
                // Run the JOB Process
                const jobId = response.data.job_id;
                const runProcess = async () => { await axios.post(`${backendURL}/source/video/run-process/${jobId}`, formData, {headers: {'Content-Type': 'multipart/form-data'}}); };
                runProcess(); // Start the process

                // Check the progress
                return new Promise((resolve, reject) => {
                    const interval = setInterval(async () => {
                        try {
                            const respRP = await fetch(`${backendURL}/source/video/get-progress/${jobId}`);
                            const resultRP = await respRP.json();
                            if (resultRP.progress) {
                                setPrgsVideo(resultRP.progress);
                                if (resultRP.progress === 101) {
                                    const responseRes = await fetch(`${backendURL}/source/video/result-process/${jobId}`, {headers: {'Content-Type': 'multipart/form-data'}});
                                    const blob = await responseRes.blob();
                                    const url = URL.createObjectURL(blob);
                                    clearInterval(interval);
                                    resolve(url);
                                }
                            }
                        } catch (error) {
                            clearInterval(interval);
                            reject(error);
                        }
                    }, 1000);
                });
            } catch (error) {
                return undefined;
            };            
        };

        // -- Perform the Image Detection -- //
        const performImageDetection = async (file: any) => {
            const formData = new FormData();
            formData.append('image', file);
            formData.append('weights', JSON.stringify(weights));
            try {
                const response = await axios.post(`${backendURL}/source/image/run-process`, formData, {headers: {'Content-Type': 'multipart/form-data'}, responseType: 'blob'});
                if (response.status !== 200) { 
                    return undefined;
                }
                const blob = response.data;
                const url = URL.createObjectURL(blob);
                return url;
            } catch (error) {
                return undefined;
            }
        };

        // -- Handle Files -- //
        const handleFiles = async () => {
            if (listIpts && listIpts.length > 0) {
                const results = [];
                setIsProcessing(true);
                for (const file of listIpts) {
                    setCrntProcessFile(file.name);
                    let result;
                    if (file.type.includes('video')) {  // Video
                        setStartVideoProcess(true);
                        result = await performVideoDetection(file);
                        setStartVideoProcess(false);
                        setPrgsVideo(0);
                    } else {
                        result = await performImageDetection(file);
                    }
                    results.push(result);
                }
                setIsProcessing(false);
                setListOutpts(results);
                setIsFinished(true);
            };
        };
        if (!isFinished){
            handleFiles();
        };
    }, [listIpts, isFinished]);
   

    // Handlers //
    // - Drag Over - //
    const handleDragOver = (e: React.DragEvent<HTMLLabelElement>) => {
        e.preventDefault();
    };

    // - File Drop - //
    const handleDrop = (e: React.DragEvent<HTMLLabelElement>) => {
        e.preventDefault();
        if (isProcessing) { return; };
        const transferFiles = e.dataTransfer.files;
        if (transferFiles){
            setListIpts(Array.from(transferFiles));
            setListOutpts([]);
            setIsFinished(false);
        };
    };

    // - File Change - //
    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (isProcessing) { return; };
        const transferFiles = e.target.files;
        if (transferFiles){
            setListIpts(Array.from(transferFiles));
            setListOutpts([]);
            setIsFinished(false);
        };
    };

    // Return //    
    return (
        <>
        <div id="processing">
            <div className="upload-files">  {/* Upload Container */}
                <label className="dropzone" htmlFor="dropzone-file" aria-disabled={isProcessing} onDrop={handleDrop} onDragOver={handleDragOver}>
                    <div className="content">
                        <IcUploadIcon className='icon-upload' />
                        {isProcessing ? (
                            <React.Fragment>
                                <p className="main" dangerouslySetInnerHTML={{__html: GetValueFromKeys(contentCore, "Upload/Waiting")}}/>
                            </React.Fragment>
                        ) : (
                            <React.Fragment>
                                <p className="main" dangerouslySetInnerHTML={{__html: GetValueFromKeys(contentCore, "Upload/Title")}}/>
                                <p className="sub mb-1" dangerouslySetInnerHTML={{__html: GetValueFromKeys(contentCore, "Upload/Subtitle1")}}/>                                 
                                <p className="sub italic" dangerouslySetInnerHTML={{__html: GetValueFromKeys(contentCore, "Upload/Subtitle2")}}/>                                 
                            </React.Fragment>
                        )}
                    </div>
                    <input id="dropzone-file" disabled={isProcessing} className="hidden" type="file" accept="video/*,image/*" multiple onChange={(e) => handleFileChange(e)} />
                </label>
            </div>
            {isProcessing && (  // If Processing
                <div className="processing-prgrs">  {/* Processing Container */}
                    <p className="p-prgrs-title">
                        {GetValueFromKeys(contentCore, 'Processing/File')}
                        <span className='p-prgrs-t-filename'>{crntProcessFile}</span>
                    </p>
                    <hr className='p-prgrs-divider'/>
                    {startVideoProcess && <ProcessVideo contentProcessing={GetValueFromKeys(contentCore, 'Processing/Video')} progression={prgsVideo}/>}
                </div>
            )}   
        </div>     
        </>
    );
};