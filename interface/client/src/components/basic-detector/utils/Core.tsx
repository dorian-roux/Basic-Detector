// ------------------------------------------ //
// COMPONENTS / BASIC-DETECTOR | UTILS / CORE //
// ------------------------------------------ //

// Client-Side Rendering //
"use client"; 


// Imports //
// - Packages - //
import React, { useState } from 'react';
import { useLocale } from 'next-intl';
import { motion } from 'framer-motion';

// - Components - //
import { GetValueFromKeys } from '@/components/basic-detector/hooks/Utils';
import { IcColorPicker, IcDownload, IcRefresh } from '@/components/basic-detector/icons/Main';
import Process from '@/components/basic-detector/utils/core/Process';


// Function | Core //
export default function Core({contentCore, weights, setWeights}: {contentCore: any, weights: any, setWeights: any}) {
    // Variables //
    const locale = useLocale();
    const [listInputs, setListInputs] = useState<any>([]);
    const [listOutputs, setListOutputs] = useState<any>([]);
    const [isProcessingFinished, setIsProcessingFinished] = useState<boolean>(false);
    const [focucIdc, setFocusIdc] = useState<number>(0);
    
    const [displayOpts, setDisplayOpts] = useState(Object.keys(GetValueFromKeys(contentCore, 'Results/DisplayOptions/List')).reduce((acc: any, key: string, index: number) => (acc[key] = index === 1, acc), {}));
    const [slctCategories, setSlctCategories] = useState<string[]>([]);
    

    // Handlers //
    // - Handle Display Options Change - //
    const handleDisplayOpts = (key: string) => {
        let newDisplayOpts: {[key: string]: boolean;} = {...displayOpts}
        for (const iKey in newDisplayOpts) {newDisplayOpts[iKey] = false;};
        newDisplayOpts[key] = true;
        setDisplayOpts(newDisplayOpts);
    };
    
    // - Handle Category Change - //
    const handleCategoryChange = (category: string) => {
        if (category === 'all'){
            if (slctCategories.length === Object.keys(weights).length) { setSlctCategories([]); }
            else { 
                const allCategories = Object.values(weights).map((ctgs: any) => ctgs.NAME);
                setSlctCategories(allCategories); 
            };
            return;
        };
        setSlctCategories((prevSelectedCategories) =>
            prevSelectedCategories.includes(category)
                ? prevSelectedCategories.filter((c) => c !== category)
                : [...prevSelectedCategories, category]
        );
    };
    
    // - Handle Color Modification - //
      const handleColorModification = (index: any, value: any) => {
        const aKey = Object.keys(weights)[index];
        const newWeights = {...weights, [aKey]: {...weights[aKey], COLOR: transformHexToRGB(value)}};
        setWeights(newWeights);
    };

    // Constants // 
    // - Transform Hex to RGB - //
    const transformHexToRGB = (hex: string) => { const hexValue = hex.replace('#', ''); return [parseInt(hexValue.substring(0, 2), 16), parseInt(hexValue.substring(2, 4), 16), parseInt(hexValue.substring(4, 6), 16)]; };
   
    // - Transform RGB to Hex - //
    const transformRGBToHex = (rgb: number[]) => { return '#' + rgb.map((c) => c.toString(16).padStart(2, '0')).join(''); };
        
    // - Get Filtered Weights - //
    const filterWeights = (weights: any, slctCategories: any) => {
        if (slctCategories.length === 0) { return weights; }
        return Object.fromEntries(Object.entries(weights).filter(([_, value]) => slctCategories.includes(GetValueFromKeys(value, 'NAME'))));
    };

    // - Filtered Weights - //
    const filteredWeights = filterWeights(weights, slctCategories);


    // Return //
    return (
        <div id="video-file-container">
            <div className='parent-container items-stretch'>   
                {/* SideBar */}
                <div className="sidebar">
                    {weights && Object.values(weights).length > 0 && (
                        <div className='detection-option'>
                            <p className='dopt-title'>{GetValueFromKeys(contentCore, 'Sidebar/Detection/Title')}</p>
                            <div className='dopt-content'>
                                <React.Fragment>
                                    <div key={"all"} className="dopt-item">
                                        <input type="checkbox" id={`category-${"all".toLocaleLowerCase()}`} value={"all"} checked={slctCategories.length == Object.values(weights).length || slctCategories.length === 0} onChange={() => handleCategoryChange("all")} className="dopt-input"/>
                                        <label htmlFor={`category-${"all".toLocaleLowerCase()}`} className="dopt-label dopt-all-label">{GetValueFromKeys(contentCore, 'Sidebar/Detection/Buttons/All')}</label>
                                    </div>
                                    {Object.values(weights).map((ctgs: any, index: number) => (                             
                                        <div key={index} className="dopt-item">
                                            <motion.div whileHover={{scale: 0.90, transition:{duration: 0.5}}}  className='color-container'>
                                                <input type="color" name={`ipt-tag-color-${index}`} id={`ipt-tag-color-${index}`} className='color-ipt' value={transformRGBToHex(ctgs.COLOR)} onChange={(e) => handleColorModification(index, e.target.value)} />
                                                <IcColorPicker className={`color-ic`} style={{fill: `rgb(${ctgs.COLOR[0]}, ${ctgs.COLOR[1]}, ${ctgs.COLOR[2]})`}}/>
                                            </motion.div>
                                            <input type="checkbox" id={`category-${index}`} value={ctgs.NAME} checked={slctCategories.includes(ctgs.NAME)} onChange={() => handleCategoryChange(ctgs.NAME)} className="dopt-input"/>
                                            <label htmlFor={`category-${index}`} className="dopt-label">{slctCategories.includes(ctgs.NAME)}{ctgs.NAME}</label>
                                        </div>
                                    ))}
                                </React.Fragment>
                            </div>
                        </div>
                    )}
                </div>
                <div className='separator'/>
                <div className='parent-content'>
                    <Process contentCore={contentCore} weights={filteredWeights} listIpts={listInputs} setListIpts={setListInputs} setListOutpts={setListOutputs} isFinished={isProcessingFinished} setIsFinished={setIsProcessingFinished}/>
                    {isProcessingFinished && (
                        <div className='output-container'>
                            <div className='refresh-container'>  {/* Refresh */}
                                <motion.button whileHover={{ scale: 0.95, transition: { duration: 0.3 } }} whileTap={{ scale: 0.9, transition: { duration: 0.3 } }} onClick={() => setIsProcessingFinished(false)} className='refresh-btn'>
                                    {listInputs.length > 1 ? GetValueFromKeys(contentCore, 'Results/Refresh/Multiple') : GetValueFromKeys(contentCore, 'Results/Refresh/Single')}
                                    <IcRefresh className='icon-refresh'/>
                                </motion.button>
                            </div>
                            {listInputs.length > 1 && (
                                <div className='output-files-ctnr'>
                                    <h3 className='output-fctnr-title'>{GetValueFromKeys(contentCore, 'Results/Files/Title')}</h3>
                                    {listInputs.length > 1 && listInputs.map((input: any, index: number) => (
                                        <motion.p
                                        whileHover={{ scale: .95, transition: { duration: 0.3 } }}
                                        key={index} className={`output-fctnr-item ${focucIdc === index && '!text-lg sm:!text-sm xs:!text-xs font-semibold'}`} onClick={() => setFocusIdc(index)}>
                                            {">"} {input.name}
                                        </motion.p>

                                    ))}
                                </div>
                            )}
                            {listOutputs.length > 0 && listOutputs[focucIdc] && (
                            <React.Fragment>
                                <div className='output-main-opts'>
                                    <div className='output-parent-options'>
                                        <hr className='line-divider'/>
                                        <h3 className='title'>{GetValueFromKeys(contentCore, 'Results/DisplayOptions/Title')}</h3>
                                        <div className='child-options'>
                                            {Object.keys(GetValueFromKeys(contentCore, 'Results/DisplayOptions/List')).map((key) => (
                                                <motion.button whileHover={{ scale: 0.9, transition: { duration: 0.3 } }} whileTap={{ scale: 0.9, transition: { duration: 0.3 } }}
                                                className={`btn ${GetValueFromKeys(displayOpts, key) && '!border-2 !bg-amber-100 dark:!bg-amber-800'}`} key={key} onClick={() => handleDisplayOpts(key)}>
                                                {GetValueFromKeys(contentCore, `Results/DisplayOptions/List/${key}`)}
                                                </motion.button>
                                            ))}
                                        </div>
                                        <hr className='line-divider'/>
                                    </div>    
                                </div>
                                {GetValueFromKeys(displayOpts, 'Original') && (  // Original Only
                                    <div className='original-container'>
                                        <h3>{GetValueFromKeys(contentCore, 'Results/Original/Title')}</h3>
                                        <div className='video-container'>
                                            {listInputs[focucIdc].type.includes('video') ? (
                                                <video controls src={URL.createObjectURL(listInputs[focucIdc])}>
                                                    <source type="video/mp4"/>
                                                    {GetValueFromKeys(contentCore, 'Results/Video/Unavailable')}
                                                </video>
                                            ) : (
                                                <img src={URL.createObjectURL(listInputs[focucIdc])} alt='input'/>
                                            )}
                                        </div>
                                    </div>
                                )}
                                {GetValueFromKeys(displayOpts, 'Detection') && (  // Detection Only
                                    <div className='detection-container'>
                                        <h3>{GetValueFromKeys(contentCore, 'Results/Detection/Title')}</h3>
                                        <div className='video-container'>
                                            {listInputs[focucIdc].type.includes('video') ? (
                                                <video controls src={listOutputs[focucIdc]}>
                                                    <source type="video/mp4"/>
                                                    {GetValueFromKeys(contentCore, 'Results/Video/Unavailable')}
                                                </video>
                                            ) : (
                                                <img src={listOutputs[focucIdc]} alt='output'/>
                                            )}
                                        </div>
                                    </div>
                                )}

                                {/* Download */}
                                <div className='download-container'>
                                    <a href={listOutputs[focucIdc]} download={`${listInputs[focucIdc]?.name.split('.')[0] || GetValueFromKeys(contentCore, 'Results/Download/Filename/Prefix')}-${GetValueFromKeys(contentCore, 'Results/Download/Filename/Suffix')}.${listInputs[focucIdc]?.name.split('.')[1] || 'mp4'}`}>
                                        <motion.button whileHover={{ scale: 0.95, transition: { duration: 0.3 } }} whileTap={{ scale: 0.9, transition: { duration: 0.3 } }} className='download-btn'>
                                            {GetValueFromKeys(contentCore, 'Results/Download/Title')}
                                            <IcDownload className='icon-download'/>
                                        </motion.button>
                                    </a>
                                </div>
                            </React.Fragment>
                        )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};