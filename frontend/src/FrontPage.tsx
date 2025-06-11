import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, TorusKnot } from '@react-three/drei'
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import { Box, Typography, Button } from '@mui/material'

const FrontPage: React.FC = () => {
  const navigate = useNavigate()

  const handleGetStarted = () => {
    navigate('/app')
  }

  return (
    <Box sx={{ height: '100vh', width: '100vw', position: 'relative' }}>
      {/* 3D Background */}
      <Box sx={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}>
        <Canvas camera={{ position: [0, 0, 5] }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <TorusKnot args={[1, 0.3, 128, 32]}>
            <meshStandardMaterial color="#4169E1" />
          </TorusKnot>
          <OrbitControls enableZoom={false} />
          <EffectComposer>
            <Bloom intensity={1.5} luminanceThreshold={0.1} />
          </EffectComposer>
        </Canvas>
      </Box>

      {/* Content */}
      <Box
        sx={{
          position: 'relative',
          zIndex: 1,
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          textAlign: 'center',
          px: 2,
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          Welcome to Our Platform
        </Typography>
        <Typography variant="h5" gutterBottom sx={{ mb: 4, maxWidth: '600px' }}>
          Discover powerful tools and insights to enhance your business
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={handleGetStarted}
          sx={{
            bgcolor: 'primary.main',
            '&:hover': {
              bgcolor: 'primary.dark',
            },
          }}
        >
          Get Started
        </Button>
      </Box>
    </Box>
  )
}

export default FrontPage 