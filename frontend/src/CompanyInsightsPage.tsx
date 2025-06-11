import React from 'react';
import { Box, Typography, Paper, Button, styled } from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import type { SxProps, Theme } from '@mui/material/styles';

// Reusing GlassmorphismPaper from App.tsx for consistent styling
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
}));

interface Company {
  name: string;
  industry: string;
  location: string;
  employeeCount: number;
  revenue: string;
  website: string;
  description?: string;
  contactInfo?: string;
  probabilityScore?: number;
  rank?: number;
  insightsSummary?: string;
}

interface CompanyInsightsPageProps {
  company: Company;
  onBack: () => void;
  darkMode: boolean;
}

const CompanyInsightsPage: React.FC<CompanyInsightsPageProps> = ({ company, onBack, darkMode }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        width: '100vw',
        overflow: 'hidden',
        background: darkMode
          ? 'linear-gradient(135deg, #1a1a2e 0%, #151525 100%)'
          : 'linear-gradient(135deg, #F6F6F6 0%, #E0E0E0 100%)',
        p: 4,
      }}
    >
      <Button
        variant="outlined"
        startIcon={<ArrowBackIcon />}
        onClick={onBack}
        sx={{ mb: 3, alignSelf: 'flex-start' }}
      >
        Back to Search Results
      </Button>

      <GlassmorphismPaper sx={{ flexGrow: 1, overflowY: 'auto' }}>
        <Typography variant="h4" gutterBottom>
          {company.name} Insights
        </Typography>

        <Typography variant="h6" sx={{ mt: 3, mb: 1 }}>
          Company Details
        </Typography>
        <Box>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Industry: {company.industry}</Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Location: {company.location}</Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Employees: {company.employeeCount}</Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Revenue: {company.revenue}</Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>
            Website: <a href={company.website} target="_blank" rel="noopener noreferrer">{company.website}</a>
          </Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Description: {company.description || 'N/A'}</Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Contact Info: {company.contactInfo || 'N/A'}</Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Probability Score: {company.probabilityScore?.toFixed(1) || 'N/A'}</Typography>
          <Typography variant="body1" sx={{ mb: 0.5 }}>Rank: {company.rank || 'N/A'}</Typography>
        </Box>

        <Typography variant="h6" sx={{ mt: 3, mb: 1 }}>
          Insights Summary
        </Typography>
        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
          {company.insightsSummary || 'No insights available.'}
        </Typography>
      </GlassmorphismPaper>
    </Box>
  );
};

export default CompanyInsightsPage; 