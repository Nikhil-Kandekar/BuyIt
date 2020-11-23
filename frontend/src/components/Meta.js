import React from 'react'
import { Helmet } from 'react-helmet'
import favicon from "../favicon.ico";
const Meta = ({ title, description, keywords }) => {
  return (
    <Helmet>
      <title>{title}</title>
      <meta name='description' content={description} />
      <meta name='keyword' content={keywords} />
      <link rel="icon" type="image/png" href={favicon} sizes="16x16" />
    </Helmet>
  )
}

Meta.defaultProps = {
  title: 'Welcome To Buy It',
  description: 'We sell the best products for cheap',
  keywords: 'electronics, buy electronics, cheap electroincs',
}

export default Meta