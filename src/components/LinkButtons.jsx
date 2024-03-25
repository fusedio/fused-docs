/**
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import React from 'react';
import Link from '@docusaurus/Link';
import TagGitHub from '@site/src/components/TagGitHub'


const LinkButtons = ({githubUrl, colabUrl}) => {
  return (
    <div className="link-buttons">
      <br></br>
      <Link to={colabUrl}><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></Link>
      
      <div></div>
      
      <Link to={githubUrl}><TagGitHub color="#444444">Open in GitHub</TagGitHub></Link>
    </div>
  );
};

export default LinkButtons;