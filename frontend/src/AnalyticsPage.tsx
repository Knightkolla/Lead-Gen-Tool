import React from 'react';
import { Box, Typography, Paper, Button, styled, useTheme, Stack, Chip } from '@mui/material';
import { ArrowBack as ArrowBackIcon, Dashboard as DashboardIcon, TrendingUp as TrendingUpIcon, TrendingDown as TrendingDownIcon } from '@mui/icons-material';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title } from 'chart.js';
import { Pie, Line } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title);

// Reusing GlassmorphismPaper from App.tsx for consistent styling
const GlassmorphismPaper = styled(Paper)(({ theme }) => ({
  background: theme.palette.mode === 'dark' ? 'rgba(25, 25, 25, 0.7)' : 'rgba(255, 255, 255, 0.7)',
  backdropFilter: 'blur(10px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: theme.shape.borderRadius === 4 ? '16px' : theme.shape.borderRadius,
  boxShadow: theme.palette.mode === 'dark' ? '0px 8px 30px rgba(0, 0, 0, 0.6)' : '0px 8px 30px rgba(0, 0, 0, 0.1)',
  padding: theme.spacing(3),
  transition: 'box-shadow 0.3s ease-in-out',
  '&:hover': {
    boxShadow: theme.palette.mode === 'dark' ? '0px 12px 40px rgba(0, 0, 0, 0.8)' : '0px 12px 40px rgba(0, 0, 0, 0.2)',
  },
}));

interface AnalyticsPageProps {
  onBack: () => void;
  darkMode: boolean;
}

interface TopLead {
  name: string;
  score: number;
  trend: 'up' | 'down';
  change: string;
}

// Sample data for the charts
const pieChartData = {
  labels: ['High Potential', 'Medium Potential', 'Low Potential'],
  datasets: [
    {
      data: [35, 45, 20],
      backgroundColor: ['#4169E1', '#B8860B', '#FFBF00'],
      borderColor: ['#4169E1', '#B8860B', '#FFBF00'],
      borderWidth: 1,
    },
  ],
};

const projectionData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Actual Leads',
      data: [30, 45, 35, 50, 40, 55],
      borderColor: '#4169E1',
      backgroundColor: 'rgba(65, 105, 225, 0.1)',
      tension: 0.4,
    },
    {
      label: 'Projection',
      data: [35, 40, 45, 50, 55, 60],
      borderColor: '#B8860B',
      backgroundColor: 'rgba(184, 134, 11, 0.1)',
      tension: 0.4,
      borderDash: [5, 5],
    },
  ],
};

const topLeads: TopLead[] = [
  { name: 'Tech Corp', score: 9.2, trend: 'up', change: '+12%' },
  { name: 'Innovate Inc', score: 8.8, trend: 'up', change: '+8%' },
  { name: 'Future Systems', score: 8.5, trend: 'down', change: '-3%' },
  { name: 'Smart Solutions', score: 8.3, trend: 'up', change: '+5%' },
];

const AnalyticsPage: React.FC<AnalyticsPageProps> = ({ onBack, darkMode }) => {
  const theme = useTheme();

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: theme.palette.text.primary,
        },
      },
    },
  };

  const lineChartOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: theme.palette.divider,
        },
        ticks: {
          color: theme.palette.text.primary,
        },
      },
      x: {
        grid: {
          color: theme.palette.divider,
        },
        ticks: {
          color: theme.palette.text.primary,
        },
      },
    },
  };

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
        Back to Dashboard
      </Button>

      <GlassmorphismPaper sx={{ flexGrow: 1, overflowY: 'auto' }}>
        <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 4 }}>
          <DashboardIcon sx={{ fontSize: 32, color: 'primary.main' }} />
          <Typography variant="h4">
            Analytics Dashboard
          </Typography>
        </Stack>

        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4, mt: 4 }}>
          {/* Top Leads Section */}
          <Box sx={{ flex: '1 1 300px' }}>
            <GlassmorphismPaper>
              <Typography variant="h6" gutterBottom>
                Top Leads of the Week
              </Typography>
              <Stack spacing={2}>
                {topLeads.map((lead, index) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Typography variant="body1">
                      {lead.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                        {lead.score}
                      </Typography>
                      <Chip
                        icon={lead.trend === 'up' ? <TrendingUpIcon /> : <TrendingDownIcon />}
                        label={lead.change}
                        size="small"
                        color={lead.trend === 'up' ? 'success' : 'error'}
                        sx={{ height: 24 }}
                      />
                    </Box>
                  </Box>
                ))}
              </Stack>
            </GlassmorphismPaper>
          </Box>

          {/* Leads Pie Chart */}
          <Box sx={{ flex: '1 1 400px', minHeight: 300 }}>
            <GlassmorphismPaper>
              <Typography variant="h6" gutterBottom>
                Leads Distribution
              </Typography>
              <Box sx={{ width: '100%', height: 250 }}>
                <Pie data={pieChartData} options={chartOptions} />
              </Box>
            </GlassmorphismPaper>
          </Box>

          {/* Lead Projection Graph */}
          <Box sx={{ flex: '1 1 600px', minHeight: 300 }}>
            <GlassmorphismPaper>
              <Typography variant="h6" gutterBottom>
                Lead Projection (Monthly)
              </Typography>
              <Box sx={{ width: '100%', height: 250 }}>
                <Line data={projectionData} options={lineChartOptions} />
              </Box>
            </GlassmorphismPaper>
          </Box>
        </Box>
      </GlassmorphismPaper>
    </Box>
  );
};

export default AnalyticsPage; 