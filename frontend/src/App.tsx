import React, { useState, useMemo } from 'react'
import { ThemeProvider, createTheme, styled } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import Box from '@mui/material/Box'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import Avatar from '@mui/material/Avatar'
import Tooltip from '@mui/material/Tooltip'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'
import Stack from '@mui/material/Stack'
import useMediaQuery from '@mui/material/useMediaQuery'
import Switch from '@mui/material/Switch'
import FormControlLabel from '@mui/material/FormControlLabel'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, CircularProgress, Snackbar, Alert } from '@mui/material'
import type { SxProps, Theme } from '@mui/material/styles'
import { motion } from 'framer-motion' // Import motion
import { API_BASE_URL } from './config'
import LogoutIcon from '@mui/icons-material/Logout'

import CompanyInsightsPage from './CompanyInsightsPage' // Import the new component
import AnalyticsPage from './AnalyticsPage'; // Import the new AnalyticsPage component
import ScrapeLeadsPage from './ScrapeLeadsPage' // Import the new ScrapeLeadsPage component

import '@fontsource/inter' // Import Inter font

// Custom styled Paper for glassmorphism effect
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

interface SearchParams {
  companyName: string
  industry: string
  location: string
  minEmployees: string
  maxEmployees: string
}

interface Company {
  name: string
  industry: string
  location: string
  employeeCount: number
  revenue: string
  website: string
  description?: string
  contactInfo?: string
  probabilityScore?: number
  rank?: number
  insightsSummary?: string // New field for company insights
}

interface InsightsResponse {
  insightsSummary: string;
}

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)')
  const [darkMode, setDarkMode] = useState(prefersDarkMode)
  const [searchParams, setSearchParams] = useState<SearchParams>({
    companyName: '',
    industry: '',
    location: '',
    minEmployees: '',
    maxEmployees: '',
  })
  const [searchResults, setSearchResults] = useState<Company[]>([])
  const [enrichingCompany, setEnrichingCompany] = useState<string | null>(null)
  const [selectedCompanyForInsights, setSelectedCompanyForInsights] = useState<Company | null>(null)
  const [showAnalyticsPage, setShowAnalyticsPage] = useState<boolean>(false)
  const [activeView, setActiveView] = useState<'dashboard' | 'insights' | 'analytics' | 'scrape'>('dashboard') // New state to manage active view
  const [sendingToCrm, setSendingToCrm] = useState<string | null>(null) // New state for CRM loading
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'info' | 'warning';
  }>({
    open: false,
    message: '',
    severity: 'info'
  });

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: darkMode ? 'dark' : 'light',
          primary: {
            main: '#4169E1', // Royal Blue
          },
          secondary: {
            main: '#B8860B', // Muted Gold
          },
          background: {
            default: darkMode ? '#1a1a2e' : '#F6F6F6', // Dark background for dark mode, Off-white for light
            paper: darkMode ? 'rgba(25, 25, 25, 0.7)' : 'rgba(255, 255, 255, 0.7)', // For glassmorphism effect
          },
          warning: {
            main: '#FFBF00', // Amber for Alert/CTA
          },
          success: {
            main: '#2ECC71', // Green for Success
          },
        },
        typography: {
          fontFamily: ['Inter', 'sans-serif'].join(','),
          h4: {
            fontWeight: 700,
            fontSize: '2.5rem',
          },
          h6: {
            fontWeight: 600,
          },
        },
        shape: {
          borderRadius: 16, // Base for 2xl rounded borders
        },
        components: {
          MuiCssBaseline: {
            styleOverrides: {
              body: {
                background: darkMode
                  ? 'linear-gradient(135deg, #1a1a2e 0%, #151525 100%)'
                  : 'linear-gradient(135deg, #F6F6F6 0%, #E0E0E0 100%)',
              },
            },
          },
          MuiPaper: {
            styleOverrides: {
              root: {
                borderRadius: '16px', // Apply 2xl border radius to all Paper components by default
                boxShadow: darkMode ? '0px 4px 20px rgba(0, 0, 0, 0.5)' : '0px 4px 20px rgba(0, 0, 0, 0.1)', // Subtle shadow
              },
            },
          },
          MuiButton: {
            styleOverrides: {
              root: {
                textTransform: 'none',
                borderRadius: '12px', // More rounded buttons
              },
            },
          },
          MuiTextField: {
            styleOverrides: {
              root: {
                '& .MuiOutlinedInput-root': {
                  borderRadius: '12px',
                },
              },
            },
          },
        },
      }),
    [darkMode],
  )

  const memoizedMainBoxSx: SxProps<Theme> = useMemo(
    () => ({
      display: 'flex',
      height: '100vh',
      width: '100vw',
      overflow: 'hidden',
      bgcolor: theme.palette.background.default,
    }),
    [theme.palette.background.default],
  );

  const backgroundGradient = darkMode
    ? 'linear-gradient(135deg, #1a1a2e 0%, #151525 100%)'
    : 'linear-gradient(135deg, #F6F6F6 0%, #E0E0E0 100%)';

  const mainBoxStyle = { background: backgroundGradient };

  const handleThemeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDarkMode(event.target.checked)
  }

  const handleSearch = async () => {
    try {
      // Create a copy of searchParams and handle empty employee fields
      const searchData = {
        ...searchParams,
        minEmployees: searchParams.minEmployees ? parseInt(searchParams.minEmployees) : null,
        maxEmployees: searchParams.maxEmployees ? parseInt(searchParams.maxEmployees) : null,
      };

      const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchData),
      })

      if (!response.ok) {
        throw new Error('Search failed')
      }

      const searchDataResponse = await response.json()
      console.log('Search API response data:', searchDataResponse)
      // Sort results by probabilityScore in descending order and assign rank
      const sortedResults = searchDataResponse.sort(
        (a: Company, b: Company) => (b.probabilityScore || 0) - (a.probabilityScore || 0),
      )
      const rankedResults = sortedResults.map((company: Company, index: number) => ({
        ...company,
        rank: index + 1, // Assign rank based on sorted order
      }))
      setSearchResults(rankedResults)
    } catch (error) {
      console.error('Error searching companies:', error)
      setSnackbar({
        open: true,
        message: 'Failed to search companies. Please try again.',
        severity: 'error'
      })
    }
  }

  const handleInputChange = (field: keyof SearchParams) => (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setSearchParams((prev) => ({ ...prev, [field]: event.target.value }))
  }

  const handleEnrich = async (company: Company) => {
    setEnrichingCompany(company.name) // Set company being enriched for loading state
    try {
      const response = await fetch(`${API_BASE_URL}/api/enrich`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ companyName: company.name }), // Send company name for enrichment
      })

      if (!response.ok) {
        throw new Error('Lead enrichment failed')
      }

      const enrichedCompanyData = await response.json() as Company;

      // Update the specific company in the search results with enriched data
      setSearchResults((prevResults) =>
        prevResults
          .map((c) => (c.name === company.name ? { ...c, ...enrichedCompanyData } : c))
          .sort((a: Company, b: Company) => (b.probabilityScore || 0) - (a.probabilityScore || 0)),
      )
    } catch (error) {
      console.error('Error enriching company:', error)
    } finally {
      setEnrichingCompany(null) // Clear loading state
    }
  }

  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  const handleAddToCrm = async (company: Company) => {
    setSendingToCrm(company.name)
    try {
      const formattedWebsite = company.website && !/^https?:\/\//i.test(company.website)
        ? `https://${company.website}`
        : company.website;
      const finalWebsite = formattedWebsite && formattedWebsite.length > 0 ? formattedWebsite : null; // Ensure null for empty string

      // Basic parsing of location string into city, state, country
      let city = null;
      let state = null;
      let country = null;

      if (company.location) {
        const locationParts = company.location.split(', ').map(part => part.trim());
        if (locationParts.length >= 1) {
          city = locationParts[0];
        }
        if (locationParts.length >= 2) {
          state = locationParts[1];
        }
        if (locationParts.length >= 3) {
          country = locationParts[2];
        }
      }

      // Basic parsing for first_name, last_name, and email from contactInfo
      let firstName = null;
      let lastName = null;
      let email = null;

      if (company.contactInfo) {
        const contactParts = company.contactInfo.split(/\s|,/g).filter(Boolean); // Split by space or comma, remove empty strings
        if (contactParts.length > 0) {
          // Attempt to extract email first
          const emailMatch = contactParts.find(part => part.includes('@'));
          if (emailMatch) {
            email = emailMatch; // Use the first part that looks like an email
            // Try to derive name from remaining parts if email is separated
            const nameParts = contactParts.filter(part => part !== emailMatch);
            if (nameParts.length > 0) firstName = nameParts[0];
            if (nameParts.length > 1) lastName = nameParts[1];
          } else {
            // If no email, assume the parts are names
            firstName = contactParts[0];
            if (contactParts.length > 1) lastName = contactParts[1];
          }
        }
      }

      const crmLeadData = {
        company_name: company.name,
        first_name: firstName,
        last_name: lastName,
        email: email,
        phone: null, // Assuming phone is not directly available from Company for now
        website: finalWebsite, // Use the processed website
        industry: company.industry || null,
        city: city,
        state: state,
        country: country,
        employee_count: company.employeeCount || null,
        revenue: company.revenue || null,
        description: company.description || null,
        contact_info: company.contactInfo || null,
        // You can map other fields from 'company' to 'CrmLead' as needed
      };

      const response = await fetch(`${API_BASE_URL}/api/crm/lead`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(crmLeadData),
      });

      if (!response.ok) {
        throw new Error('Failed to add to CRM');
      }

      const result = await response.json();
      console.log('Added to CRM successfully:', result);
      setSnackbar({
        open: true,
        message: `Successfully added ${company.name} to CRM!`,
        severity: 'success'
      });
    } catch (error) {
      console.error('Error adding to CRM:', error);
      setSnackbar({
        open: true,
        message: `Failed to add ${company.name} to CRM. Please try again.`,
        severity: 'error'
      });
    } finally {
      setSendingToCrm(null);
    }
  };

  const handleInsights = async (company: Company) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/insights`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company }), // Send the full company object for insights
      })

      if (!response.ok) {
        throw new Error('Failed to get insights')
      }

      const insightsData: InsightsResponse = await response.json();

      // Update the company in the search results with the new insights
      setSearchResults((prevResults) =>
        prevResults.map((c) =>
          c.name === company.name ? { ...c, insightsSummary: insightsData.insightsSummary } : c,
        ),
      )

      // Set the selected company to display insights page
      setSelectedCompanyForInsights({ ...company, insightsSummary: insightsData.insightsSummary })
      setActiveView('insights') // Set active view to insights
    } catch (error) {
      console.error('Error fetching insights:', error)
    }
  }

  const handleBackToSearch = () => {
    setSelectedCompanyForInsights(null) // Clear selected company to go back to search
    setActiveView('dashboard') // Set active view back to dashboard
  }

  const handleNavigateToAnalytics = () => {
    setShowAnalyticsPage(true); // Show analytics page
    setSelectedCompanyForInsights(null); // Ensure insights page is hidden
    setActiveView('analytics'); // Set active view to analytics
  }

  const handleBackToDashboard = () => {
    setShowAnalyticsPage(false); // Hide analytics page, go back to search dashboard
    setActiveView('dashboard'); // Set active view to dashboard
  }

  const handleNavigateToScrapeLeads = () => {
    setActiveView('scrape'); // Set active view to scrape
  }

  // Move the conditional rendering to the end
  if (activeView === 'insights') {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <CompanyInsightsPage
          company={selectedCompanyForInsights!}
          onBack={handleBackToSearch}
          darkMode={darkMode}
        />
      </ThemeProvider>
    )
  }

  if (activeView === 'analytics') {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AnalyticsPage
          onBack={handleBackToDashboard}
          darkMode={darkMode}
        />
      </ThemeProvider>
    )
  }

  if (activeView === 'scrape') {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <ScrapeLeadsPage
          onBack={handleBackToDashboard}
          darkMode={darkMode}
          onScrapeSuccess={handleSearch} // Trigger search after successful scrape
        />
      </ThemeProvider>
    )
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={memoizedMainBoxSx} style={mainBoxStyle}>
        {/* Minimal Sidebar */}
        <Box
          sx={{
            width: { xs: '0', md: '80px' }, // Collapsed on mobile, minimal on desktop
            bgcolor: 'background.paper',
            borderRight: '1px solid rgba(255, 255, 255, 0.1)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            py: 3,
            transition: 'width 0.3s ease-in-out',
          }}
        >
          {/* Placeholder for sidebar content, e.g., icons */}
          <IconButton sx={{ mb: 2 }} onClick={() => setActiveView('dashboard')}> {/* Dashboard Button */}
            <Box sx={{ width: 40, height: 40, bgcolor: 'primary.main', borderRadius: '8px' }} />
          </IconButton>
          <IconButton sx={{ mb: 2 }} onClick={handleNavigateToAnalytics}> {/* Analytics Button */}
            <Box sx={{ width: 40, height: 40, bgcolor: 'secondary.main', borderRadius: '8px' }} />
          </IconButton>
          <IconButton sx={{ mb: 2 }} onClick={handleNavigateToScrapeLeads}> {/* Scrape Leads Button */}
            <Box sx={{ width: 40, height: 40, bgcolor: 'warning.main', borderRadius: '8px' }} />
          </IconButton>
        </Box>

        {/* Main Content Area */}
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
          {/* Top Bar */}
          <AppBar
            position="static"
            elevation={0}
            sx={{ bgcolor: 'background.paper', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}
          >
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'text.primary' }}>
                Company Search Dashboard
              </Typography>
              <FormControlLabel
                control={<Switch checked={darkMode} onChange={handleThemeChange} />}
                label="Dark Mode"
                labelPlacement="start"
                sx={{ color: 'text.primary', mr: 2 }}
              />
              <Tooltip title="User Profile">
                <IconButton sx={{ p: 0 }}>
                  <Avatar alt="User Name" src="/static/images/avatar/2.jpg" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Logout">
                <IconButton sx={{ ml: 2 }} color="error" onClick={() => { localStorage.removeItem('loggedIn'); window.location.reload(); }}>
                  <LogoutIcon />
                </IconButton>
              </Tooltip>
            </Toolbar>
          </AppBar>

          {/* Search Section */}
          <Box sx={{ p: 4, flexGrow: 1 }}>
            <Grid container spacing={4}>
              {/* Search Form */}
              <Grid item xs={12}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <GlassmorphismPaper>
                    <Typography variant="h6" gutterBottom>
                      Company Search
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                      <TextField
                        label="Company Name"
                        value={searchParams.companyName}
                        onChange={handleInputChange('companyName')}
                        size="small"
                      />
                      <TextField
                        label="Industry"
                        value={searchParams.industry}
                        onChange={handleInputChange('industry')}
                        size="small"
                      />
                      <TextField
                        label="Location"
                        value={searchParams.location}
                        onChange={handleInputChange('location')}
                        size="small"
                      />
                      <TextField
                        label="Min Employees"
                        type="number"
                        value={searchParams.minEmployees}
                        onChange={handleInputChange('minEmployees')}
                        size="small"
                      />
                      <TextField
                        label="Max Employees"
                        type="number"
                        value={searchParams.maxEmployees}
                        onChange={handleInputChange('maxEmployees')}
                        size="small"
                      />
                      <Button variant="contained" onClick={handleSearch}>
                        Search
                      </Button>
                    </Box>
                  </GlassmorphismPaper>
                </motion.div>
              </Grid>

              {/* Search Results */}
              {searchResults.length > 0 && (
                <Grid item xs={12}>
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                  >
                    <GlassmorphismPaper>
                      <Typography variant="h6" gutterBottom>
                        Search Results
                      </Typography>
                      <TableContainer>
                        <Table>
                          <TableHead>
                            <TableRow>
                              <TableCell>Company Name</TableCell>
                              <TableCell>Industry</TableCell>
                              <TableCell>Location</TableCell>
                              <TableCell>Employee Count</TableCell>
                              <TableCell>Revenue</TableCell>
                              <TableCell>Website</TableCell>
                              <TableCell>Description</TableCell>
                              <TableCell>Contact Info</TableCell>
                              <TableCell>Score (1-10)</TableCell>
                              <TableCell>Rank</TableCell>
                              <TableCell>Action</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {searchResults.map((company, index) => (
                              <motion.tr
                                key={index}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.3, delay: index * 0.05 }}
                              >
                                <TableCell>{company.name}</TableCell>
                                <TableCell>{company.industry}</TableCell>
                                <TableCell>{company.location}</TableCell>
                                <TableCell>{company.employeeCount}</TableCell>
                                <TableCell>{company.revenue}</TableCell>
                                <TableCell>
                                  <a href={company.website} target="_blank" rel="noopener noreferrer">
                                    {company.website}
                                  </a>
                                </TableCell>
                                <TableCell>{company.description || 'N/A'}</TableCell>
                                <TableCell>{company.contactInfo || 'N/A'}</TableCell>
                                <TableCell>{company.probabilityScore?.toFixed(1) || 'N/A'}</TableCell>
                                <TableCell>{company.rank || 'N/A'}</TableCell>
                                <TableCell>
                                  <Stack direction="row" spacing={1}>
                                    <Stack direction="column" spacing={1}>
                                      <Button
                                        variant="outlined"
                                        size="small"
                                        onClick={() => handleEnrich(company)}
                                        disabled={enrichingCompany === company.name}
                                      >
                                        {enrichingCompany === company.name ? <CircularProgress size={20} /> : 'Enrich'}
                                      </Button>
                                      <Button
                                        variant="contained"
                                        size="small"
                                        onClick={() => handleInsights(company)}
                                      >
                                        Insights
                                      </Button>
                                    </Stack>
                                    {/* CRM Action button */}
                                    {sendingToCrm === company.name ? (
                                      <CircularProgress size={20} />
                                    ) : (
                                      <Button
                                        variant="contained"
                                        size="small"
                                        onClick={() => handleAddToCrm(company)}
                                      >
                                        Add to CRM
                                      </Button>
                                    )}
                                  </Stack>
                                </TableCell>
                              </motion.tr>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                    </GlassmorphismPaper>
                  </motion.div>
                </Grid>
              )}

              {/* Stats Overview */}
              <Grid item xs={12} md={6} lg={4}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                >
                  <GlassmorphismPaper>
                    <Typography variant="h6" gutterBottom>
                      Search Statistics
                    </Typography>
                    <Typography variant="h4">{searchResults.length}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Companies Found
                    </Typography>
                  </GlassmorphismPaper>
                </motion.div>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Box>
      
      {/* Add Snackbar at the end of the component, just before closing ThemeProvider */}
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
    </ThemeProvider>
  )
}

export default App