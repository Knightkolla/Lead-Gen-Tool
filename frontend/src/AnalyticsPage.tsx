import React from 'react';
import { Box, Typography, Paper, Button, styled, useTheme, Stack, Chip } from '@mui/material';
import { ArrowBack as ArrowBackIcon, Dashboard as DashboardIcon, TrendingUp as TrendingUpIcon, TrendingDown as TrendingDownIcon } from '@mui/icons-material';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title } from 'chart.js';
import { Pie, Line } from 'react-chartjs-2';
import { API_BASE_URL } from './config';

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

interface AnalyticsData {
  lead_distribution: { [key: string]: number };
  lead_projection: { month: string; actual: number; projection: number }[];
  top_leads: TopLead[];
}

const AnalyticsPage: React.FC<AnalyticsPageProps> = ({ onBack, darkMode }) => {
  const theme = useTheme();
  const [analyticsData, setAnalyticsData] = React.useState<AnalyticsData | null>(null);
  const [loading, setLoading] = React.useState<boolean>(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/api/analytics`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: AnalyticsData = await response.json();
        setAnalyticsData(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  const pieChartData = React.useMemo(() => {
    if (!analyticsData?.lead_distribution) return { labels: [], datasets: [] };
    const labels = Object.keys(analyticsData.lead_distribution);
    const data = Object.values(analyticsData.lead_distribution);
    return {
      labels,
      datasets: [
        {
          data,
          backgroundColor: ['#4169E1', '#B8860B', '#FFBF00'],
          borderColor: ['#4169E1', '#B8860B', '#FFBF00'],
          borderWidth: 1,
        },
      ],
    };
  }, [analyticsData]);

  const projectionData = React.useMemo(() => {
    if (!analyticsData?.lead_projection) return { labels: [], datasets: [] };
    const labels = analyticsData.lead_projection.map(item => item.month);
    const actualData = analyticsData.lead_projection.map(item => item.actual);
    const projectionData = analyticsData.lead_projection.map(item => item.projection);

    return {
      labels,
      datasets: [
        {
          label: 'Actual Leads',
          data: actualData,
          borderColor: '#4169E1',
          backgroundColor: 'rgba(65, 105, 225, 0.1)',
          tension: 0.4,
        },
        {
          label: 'Projection',
          data: projectionData,
          borderColor: '#B8860B',
          backgroundColor: 'rgba(184, 134, 11, 0.1)',
          tension: 0.4,
          borderDash: [5, 5],
        },
      ],
    };
  }, [analyticsData]);

  const topLeads = React.useMemo(() => {
    if (!analyticsData?.top_leads) return [];
    return analyticsData.top_leads;
  }, [analyticsData]);

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