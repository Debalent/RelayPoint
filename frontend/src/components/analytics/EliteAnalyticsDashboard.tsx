/**
 * Elite Analytics Dashboard
 * 
 * Advanced analytics and insights for RelayPoint workflows
 * with real-time metrics, AI-powered insights, and executive reporting
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Typography,
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Avatar,
  Divider,
  Alert,
  LinearProgress,
} from '@mui/material';

import {
  Analytics as AnalyticsIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Speed as SpeedIcon,
  Timer as TimerIcon,
  AttachMoney as MoneyIcon,
  Person as PersonIcon,
  Workflow as WorkflowIcon,
  SmartToy as AIIcon,
  Error as ErrorIcon,
  CheckCircle as SuccessIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';

import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RechartsData,
} from 'recharts';

// Types
interface MetricCard {
  title: string;
  value: string | number;
  change: number;
  icon: React.ReactNode;
  color: string;
}

interface WorkflowExecution {
  id: string;
  name: string;
  status: 'completed' | 'failed' | 'running';
  duration: number;
  cost: number;
  timestamp: string;
  user: string;
}

interface AIUsageData {
  model: string;
  requests: number;
  tokens: number;
  cost: number;
  averageResponseTime: number;
}

interface TeamPerformance {
  user: string;
  workflowsCreated: number;
  workflowsExecuted: number;
  successRate: number;
  avgExecutionTime: number;
}

const EliteAnalyticsDashboard: React.FC = () => {
  // State management
  const [timeRange, setTimeRange] = useState('7d');
  const [isLoading, setIsLoading] = useState(true);
  const [metrics, setMetrics] = useState<MetricCard[]>([]);
  const [executionData, setExecutionData] = useState<any[]>([]);
  const [aiUsageData, setAIUsageData] = useState<AIUsageData[]>([]);
  const [recentExecutions, setRecentExecutions] = useState<WorkflowExecution[]>([]);
  const [teamPerformance, setTeamPerformance] = useState<TeamPerformance[]>([]);

  // Mock data (would be replaced with real API calls)
  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock metrics
      setMetrics([
        {
          title: 'Total Workflows',
          value: 1247,
          change: 12.5,
          icon: <WorkflowIcon />,
          color: '#1976d2'
        },
        {
          title: 'Success Rate',
          value: '94.2%',
          change: 2.1,
          icon: <SuccessIcon />,
          color: '#2e7d32'
        },
        {
          title: 'Avg Execution Time',
          value: '2.4s',
          change: -8.3,
          icon: <SpeedIcon />,
          color: '#ed6c02'
        },
        {
          title: 'Total Cost Saved',
          value: '$12,430',
          change: 24.7,
          icon: <MoneyIcon />,
          color: '#9c27b0'
        },
        {
          title: 'AI Requests',
          value: 8942,
          change: 18.2,
          icon: <AIIcon />,
          color: '#00695c'
        },
        {
          title: 'Active Users',
          value: 234,
          change: 5.8,
          icon: <PersonIcon />,
          color: '#d32f2f'
        }
      ]);

      // Mock execution trend data
      setExecutionData([
        { date: '2024-01-01', executions: 45, successful: 42, failed: 3 },
        { date: '2024-01-02', executions: 52, successful: 49, failed: 3 },
        { date: '2024-01-03', executions: 38, successful: 36, failed: 2 },
        { date: '2024-01-04', executions: 64, successful: 61, failed: 3 },
        { date: '2024-01-05', executions: 71, successful: 68, failed: 3 },
        { date: '2024-01-06', executions: 56, successful: 53, failed: 3 },
        { date: '2024-01-07', executions: 83, successful: 79, failed: 4 },
      ]);

      // Mock AI usage data
      setAIUsageData([
        { model: 'GPT-4 Turbo', requests: 3245, tokens: 1284320, cost: 38.52, averageResponseTime: 1.2 },
        { model: 'Claude 3 Sonnet', requests: 1876, tokens: 934580, cost: 14.02, averageResponseTime: 0.8 },
        { model: 'Gemini Pro', requests: 2193, tokens: 876430, cost: 0.88, averageResponseTime: 1.5 },
        { model: 'GPT-3.5 Turbo', requests: 1633, tokens: 653200, cost: 1.31, averageResponseTime: 0.6 },
      ]);

      // Mock recent executions
      setRecentExecutions([
        {
          id: 'exec-001',
          name: 'Customer Onboarding Flow',
          status: 'completed',
          duration: 2.3,
          cost: 0.45,
          timestamp: '2024-01-07T10:30:00Z',
          user: 'Alice Johnson'
        },
        {
          id: 'exec-002',
          name: 'Invoice Processing Pipeline',
          status: 'running',
          duration: 0,
          cost: 0,
          timestamp: '2024-01-07T10:28:00Z',
          user: 'Bob Smith'
        },
        {
          id: 'exec-003',
          name: 'Data Analysis Workflow',
          status: 'completed',
          duration: 45.2,
          cost: 2.31,
          timestamp: '2024-01-07T10:25:00Z',
          user: 'Carol Davis'
        },
        {
          id: 'exec-004',
          name: 'Email Campaign Automation',
          status: 'failed',
          duration: 12.1,
          cost: 0.89,
          timestamp: '2024-01-07T10:20:00Z',
          user: 'David Wilson'
        }
      ]);

      // Mock team performance
      setTeamPerformance([
        { user: 'Alice Johnson', workflowsCreated: 23, workflowsExecuted: 156, successRate: 96.2, avgExecutionTime: 3.4 },
        { user: 'Bob Smith', workflowsCreated: 18, workflowsExecuted: 142, successRate: 94.1, avgExecutionTime: 2.8 },
        { user: 'Carol Davis', workflowsCreated: 31, workflowsExecuted: 203, successRate: 97.5, avgExecutionTime: 4.1 },
        { user: 'David Wilson', workflowsCreated: 15, workflowsExecuted: 98, successRate: 91.8, avgExecutionTime: 2.1 },
      ]);

      setIsLoading(false);
    };

    loadDashboardData();
  }, [timeRange]);

  // Utility functions
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    if (seconds < 3600) return `${(seconds / 60).toFixed(1)}m`;
    return `${(seconds / 3600).toFixed(1)}h`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'running': return 'primary';
      default: return 'default';
    }
  };

  // Chart colors
  const colors = ['#1976d2', '#2e7d32', '#ed6c02', '#9c27b0', '#00695c', '#d32f2f'];

  if (isLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>Analytics Dashboard</Typography>
        <LinearProgress />
        <Typography variant="body2" sx={{ mt: 2 }}>Loading analytics data...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <AnalyticsIcon /> Elite Analytics Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={timeRange}
              label="Time Range"
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <MenuItem value="1d">Last Day</MenuItem>
              <MenuItem value="7d">Last 7 Days</MenuItem>
              <MenuItem value="30d">Last 30 Days</MenuItem>
              <MenuItem value="90d">Last 90 Days</MenuItem>
            </Select>
          </FormControl>
          
          <Button startIcon={<RefreshIcon />} onClick={() => window.location.reload()}>
            Refresh
          </Button>
          
          <Button startIcon={<DownloadIcon />} variant="outlined">
            Export
          </Button>
        </Box>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Box>
                    <Typography variant="h4" sx={{ color: metric.color, fontWeight: 'bold' }}>
                      {metric.value}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {metric.title}
                    </Typography>
                  </Box>
                  <Avatar sx={{ bgcolor: metric.color }}>
                    {metric.icon}
                  </Avatar>
                </Box>
                
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  {metric.change > 0 ? <TrendingUpIcon color="success" /> : <TrendingDownIcon color="error" />}
                  <Typography
                    variant="caption"
                    sx={{ color: metric.change > 0 ? 'success.main' : 'error.main', ml: 0.5 }}
                  >
                    {Math.abs(metric.change)}% from last period
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* Execution Trends */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardHeader title="Workflow Execution Trends" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={executionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="successful"
                    stackId="1"
                    stroke="#2e7d32"
                    fill="#2e7d32"
                    name="Successful"
                  />
                  <Area
                    type="monotone"
                    dataKey="failed"
                    stackId="1"
                    stroke="#d32f2f"
                    fill="#d32f2f"
                    name="Failed"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Model Usage */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardHeader title="AI Model Usage" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={aiUsageData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="requests"
                    label={(entry) => entry.model}
                  >
                    {aiUsageData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Bottom Row */}
      <Grid container spacing={3}>
        {/* Recent Executions */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardHeader 
              title="Recent Workflow Executions"
              action={
                <IconButton>
                  <FilterIcon />
                </IconButton>
              }
            />
            <CardContent sx={{ p: 0 }}>
              <List>
                {recentExecutions.map((execution, index) => (
                  <React.Fragment key={execution.id}>
                    <ListItem>
                      <ListItemIcon>
                        {execution.status === 'completed' && <SuccessIcon color="success" />}
                        {execution.status === 'failed' && <ErrorIcon color="error" />}
                        {execution.status === 'running' && <TimerIcon color="primary" />}
                      </ListItemIcon>
                      <ListItemText
                        primary={execution.name}
                        secondary={
                          <Box>
                            <Typography variant="caption" component="span">
                              by {execution.user} • {formatDuration(execution.duration)}
                              {execution.cost > 0 && ` • ${formatCurrency(execution.cost)}`}
                            </Typography>
                          </Box>
                        }
                      />
                      <Chip
                        label={execution.status}
                        size="small"
                        color={getStatusColor(execution.status)}
                      />
                    </ListItem>
                    {index < recentExecutions.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Team Performance */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardHeader title="Team Performance" />
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={teamPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="user" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="workflowsCreated" fill="#1976d2" name="Created" />
                  <Bar dataKey="workflowsExecuted" fill="#2e7d32" name="Executed" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* AI Insights Alert */}
      <Alert 
        severity="info" 
        sx={{ mt: 3 }}
        icon={<AIIcon />}
        action={
          <Button color="inherit" size="small">
            View Details
          </Button>
        }
      >
        <Typography variant="subtitle2">AI Insight</Typography>
        Your team's workflow efficiency has improved by 23% this week. Consider scaling the "Customer Onboarding Flow" 
        pattern to other departments for maximum impact.
      </Alert>
    </Box>
  );
};

export default EliteAnalyticsDashboard;