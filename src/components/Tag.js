import React from 'react';

export default function Tag({children, color, fontColor='#fff'})  {
    return(
    <span
        style={{

            backgroundColor: color,
            borderRadius: '4px',
            color: fontColor,
            padding: '0.2rem 0.5rem',
            fontWeight: 'bold'
        }}>
    {children}
    </span>
    )
    }