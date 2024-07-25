// ------------------------------------------- //
// COMPONENTS / BASIC-DETECTOR | HOOKS / UTILS //
// ------------------------------------------- //

// Constant //
// - Return Value from Key(s) - //
export const GetValueFromKeys = (content: any, key: string, splitVar: string = '/') => {
    if (content === undefined || content === null || key === undefined || key === null) return ('')
    for (const k of key.split(splitVar)){
      if (Object.keys(content).includes(k)){
        content = content[k]
      }else{
        return ('')
      };
    };
    return content
};

// Push to URL //
export const pushToURL = (locationURL: string) => {window.location.href = locationURL;};