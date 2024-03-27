/**
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import React from 'react';
import Link from '@docusaurus/Link';


const LinkButtons = ({githubUrl, colabUrl}) => {
  return (
    <div className="link-buttons" style={{ textAlign: 'right' }}>
      <br></br>
      <Link to={colabUrl}><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></Link>
         {" "}
      <Link to={githubUrl}><img src="https://badgen.net/static/GitHub/Open/blue?icon=github" alt="Open in GitHub"/></Link>
    
    </div>
  );
};

export default LinkButtons;