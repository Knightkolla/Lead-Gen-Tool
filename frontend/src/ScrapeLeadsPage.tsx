import React, { useState, useMemo } from 'react'
import { Box, TextField, Button, Typography, CircularProgress, Snackbar, Alert, IconButton, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import { styled } from '@mui/material/styles'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import Paper from '@mui/material/Paper'
import type { SxProps, Theme } from '@mui/material/styles' // Import SxProps and Theme

// Custom styled Paper for glassmorphism effect (copied from App.tsx for consistency)
const GlassmorphismPaper = styled(Paper)(({ theme }) => ({
  background: theme.palette.mode === 'dark' ? 'rgba(25, 25, 25, 0.7)' : 'rgba(255, 255, 255, 0.7)',
  backdropFilter: 'blur(10px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: theme.shape.borderRadius === 4 ? '16px' : theme.shape.borderRadius, // Rounded 2xl borders
  boxShadow: theme.palette.mode === 'dark' ? '0px 8px 30px rgba(0, 0, 0, 0.6)' : '0px 8px 30px rgba(0, 0, 0, 0.1)',
  padding: theme.spacing(3),
  transition: 'box-shadow 0.3s ease-in-out',
  '&:hover': {
    boxShadow: theme.palette.mode === 'dark' ? '0px 12px 40px rgba(0, 0, 0, 0.8)' : '0px 12px 40px rgba(0, 0, 0, 0.2)',
  },
}))

interface ScrapeLeadsPageProps {
  onBack: () => void;
  darkMode: boolean;
  onScrapeSuccess: () => void; // Callback to trigger search after successful scrape
}

interface ScrapedLead {
  name: string;
  industry: string;
  location: string;
  website: string;
  description?: string;
  contactInfo?: string;
}

const ScrapeLeadsPage: React.FC<ScrapeLeadsPageProps> = ({ onBack, darkMode, onScrapeSuccess }) => {
  const [industry, setIndustry] = useState<string>('')
  const [location, setLocation] = useState<string>('')
  const [isScraping, setIsScraping] = useState<boolean>(false)
  const [scrapedLeads, setScrapedLeads] = useState<ScrapedLead[]>([])
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'info' | 'warning';
  }>({ open: false, message: '', severity: 'info' });

  const memoizedMainBoxSx: SxProps<Theme> = useMemo(
    () => ({
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      width: '100vw',
      overflow: 'hidden',
      backgroundColor: darkMode ? '#1a1a2e' : '#F6F6F6',
      p: 4,
    }),
    [darkMode]
  );

  const handleScrape = async () => {
    setIsScraping(true)
    try {
      const response = await fetch('http://localhost:8000/api/scrape_leads', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ industry, location }),
      })

      if (!response.ok) {
        throw new Error('Failed to scrape leads')
      }

      const data = await response.json()
      setScrapedLeads(data) // Store the scraped leads
      setSnackbar({ open: true, message: `Scraped ${data.length} new leads!`, severity: 'success' });
      onScrapeSuccess(); // Trigger search in App.tsx to refresh data

    } catch (error) {
      console.error('Error scraping leads:', error)
      setSnackbar({ open: true, message: 'Failed to scrape leads. Please try again.', severity: 'error' });
    } finally {
      setIsScraping(false)
    }
  }

  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  return (
    <Box
      sx={memoizedMainBoxSx}
    >
      <Button
        variant="outlined"
        startIcon={<ArrowBackIcon />}
        onClick={onBack}
        sx={{ mb: 3, alignSelf: 'flex-start' }}
      >
        Back to Dashboard
      </Button>

      <GlassmorphismPaper sx={{ flexGrow: 1, overflowY: 'auto' }}>
        <Typography variant="h4" gutterBottom>
          Scrape New Leads
        </Typography>
        <Typography variant="body1" gutterBottom sx={{ mb: 3 }}>
          Enter industry and location to scrape for new B2B leads.
          The scraped leads will be added to your database and visible in the search dashboard.
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 3 }}>
          <TextField
            label="Industry (e.g., Technology)"
            value={industry}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setIndustry(e.target.value)}
            fullWidth
            size="small"
          />
          <TextField
            label="Location (e.g., New York)"
            value={location}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLocation(e.target.value)}
            fullWidth
            size="small"
            sx={{ mt: 2 }} // Add margin-top for separation
          />
          <Button
            variant="contained"
            onClick={handleScrape}
            disabled={isScraping}
            sx={{ minWidth: 120, mt: 2 }} // Add margin-top for alignment
          >
            {isScraping ? <CircularProgress size={24} color="inherit" /> : 'Scrape Leads'}
          </Button>
        </Box>

        {/* Display scraped leads in a table */}
        {scrapedLeads.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Scraped Leads
            </Typography>
            <TableContainer component={Paper} sx={{ mt: 2 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Company Name</TableCell>
                    <TableCell>Industry</TableCell>
                    <TableCell>Location</TableCell>
                    <TableCell>Website</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell>Contact Info</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {scrapedLeads.map((lead, index) => (
                    <TableRow key={index}>
                      <TableCell>{lead.name}</TableCell>
                      <TableCell>{lead.industry}</TableCell>
                      <TableCell>{lead.location}</TableCell>
                      <TableCell>
                        <a href={lead.website} target="_blank" rel="noopener noreferrer">
                          {lead.website}
                        </a>
                      </TableCell>
                      <TableCell>{lead.description || 'N/A'}</TableCell>
                      <TableCell>{lead.contactInfo || 'N/A'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}
      </GlassmorphismPaper>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity={snackbar.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  )
}

export default ScrapeLeadsPage 