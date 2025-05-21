import React, { useState, useEffect, useRef } from 'react';
import ReactPlayer from 'react-player';

const LazyReactPlayer = (props) => {
  const [isVisible, setIsVisible] = useState(false);
  const playerRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        // When the player comes into view, mark it as visible
        setIsVisible(entry.isIntersecting);
      },
      {
        // Start loading when 20% of the player is visible
        threshold: 0.2,
        // Root margin can be adjusted if needed
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

  // Only play the video when it's visible, regardless of the playing prop
  // This ensures videos don't autoplay until scrolled into view
  const shouldPlay = isVisible;

  return (
    <div ref={playerRef}>
      <ReactPlayer
        {...props}
        playing={shouldPlay}
      />
    </div>
  );
};

export default LazyReactPlayer; 