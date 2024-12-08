import React from 'react'
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

const About = () => {
  const [loading, setLoading] = React.useState(true);

  return (
    <div>
      {/* {loading && <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}><CircularProgress /></div>
      } */}
     <iframe src="https://gamma.app/embed/moxtxri37ctcay3" onLoad={() => setLoading(false)} style={{ width: '100%', maxWidth: "100%", height: '120vh',  }} allow="fullscreen" title="Welcome to DeepTrace: Authenticity Assured"></iframe>
    </div>
  )
}

export default About;