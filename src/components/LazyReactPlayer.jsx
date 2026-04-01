import React, { useEffect, useRef, useState } from 'react';
import ReactPlayer from 'react-player';

const LazyReactPlayer = ({ className, playing, ...props }) => {
  const [isVisible, setIsVisible] = useState(false);
  const playerRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsVisible(entry.isIntersecting);
      },
      {
        threshold: 0.2,
        rootMargin: '0px',
      }
    );

    if (playerRef.current) {
      observer.observe(playerRef.current);
    }

    return () => {
      if (playerRef.current) {
        observer.unobserve(playerRef.current);
      }
    };
  }, []);

  const shouldPlay = Boolean(playing && isVisible);

  return (
    <div ref={playerRef} className={className}>
      <ReactPlayer
        {...props}
        className={className}
        playing={shouldPlay}
      />
    </div>
  );
};

export default LazyReactPlayer;
