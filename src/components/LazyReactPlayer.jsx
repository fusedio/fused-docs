import React from 'react';

const LazyReactPlayer = ({ url, loop, controls = true, muted = true, wrapperStyle, ...props }) => {
  return (
    <div className="video__wrapper" style={wrapperStyle}>
      <video
        src={url}
        preload="metadata"
        controls={controls}
        muted={muted}
        loop={loop}
        playsInline
        style={{ width: '100%', height: '100%', display: 'block' }}
      />
    </div>
  );
};

export default LazyReactPlayer;
