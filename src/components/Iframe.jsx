import React from 'react';

export default function Iframe({children, url}) {
  return (
    <iframe src={url} height="1050px" width="100%" scrolling="no"></iframe>
  );
}