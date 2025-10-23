/**
 * Mobile-Responsive Elite Dashboard
 * 
 * This component provides a comprehensive, mobile-first dashboard that addresses
 * common user feedback about accessibility, simplicity, and mobile support.
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
  Fab,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Drawer,
  AppBar,
  Toolbar,
  Badge,
  Avatar,
  Menu,
  MenuItem,
  Chip,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  useTheme,
  useMediaQuery,
  Skeleton,
  Alert,
  Snackbar,
  LinearProgress,
} from '@mui/material';

import {
  Menu as MenuIcon,
  Add as AddIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  Dashboard as DashboardIcon,
  Workflow as WorkflowIcon,
  Analytics as AnalyticsIcon,
  People as PeopleIcon,
  SmartToy as AIIcon,
  Security as SecurityIcon,
  Help as HelpIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  TrendingUp as TrendingUpIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
  Speed as SpeedIcon,
  AttachMoney as MoneyIcon,
  Close as CloseIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

// Custom hooks
import { useAuth } from '../../hooks/useAuth';
import { useWorkflows } from '../../hooks/useWorkflows';
import { useNotifications } from '../../hooks/useNotifications';

// Types
interface QuickAction {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
  color?: string;
}

interface DashboardMetric {
  title: string;
  value: string | number;
  change?: number;
  icon: React.ReactNode;
  color: string;
  subtitle?: string;
}

interface RecentActivity {
  id: string;
  type: 'workflow_execution' | 'template_used' | 'team_invite' | 'system_update';
  title: string;
  description: string;
  timestamp: string;
  status?: 'success' | 'error' | 'warning' | 'info';
  user?: string;
}

const MobileEliteDashboard: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));
  
  // Hooks
  const { user, isAuthenticated } = useAuth();
  const { workflows, isLoading: workflowsLoading } = useWorkflows();
  const { notifications, unreadCount } = useNotifications();
  
  // State
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [speedDialOpen, setSpeedDialOpen] = useState(false);
  const [userMenuAnchor, setUserMenuAnchor] = useState<null | HTMLElement>(null);
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [refreshing, setRefreshing] = useState(false);
  const [snackbar, setSnackbar] = useState<{open: boolean; message: string; severity: 'success' | 'error' | 'info'}>({
    open: false,
    message: '',
    severity: 'info'
  });

  // Mock data (would come from API)
  const [metrics, setMetrics] = useState<DashboardMetric[]>([
    {
      title: 'Active Workflows',
      value: 12,
      change: 8.5,
      icon: <WorkflowIcon />,
      color: theme.palette.primary.main,
      subtitle: '3 running now'
    },
    {
      title: 'Success Rate',
      value: '94.2%',
      change: 2.1,
      icon: <SuccessIcon />,
      color: theme.palette.success.main,
      subtitle: 'Last 30 days'
    },
    {
      title: 'Time Saved',
      value: '24.5h',
      change: 15.3,
      icon: <SpeedIcon />,
      color: theme.palette.warning.main,
      subtitle: 'This week'
    },
    {
      title: 'Cost Savings',
      value: '$2,340',
      change: 22.7,
      icon: <MoneyIcon />,
      color: theme.palette.info.main,
      subtitle: 'This month'
    }
  ]);

  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>([
    {
      id: '1',
      type: 'workflow_execution',
      title: 'Customer Onboarding completed',
      description: 'New customer Alice Johnson processed successfully',
      timestamp: '2 minutes ago',
      status: 'success',
      user: 'System'
    },
    {
      id: '2',
      type: 'template_used',
      title: 'Invoice Processing template used',
      description: 'Template applied for vendor payment workflow',
      timestamp: '15 minutes ago',
      status: 'info',
      user: 'Bob Smith'
    },
    {
      id: '3',
      type: 'workflow_execution',
      title: 'Data Backup failed',
      description: 'Database backup encountered connection error',
      timestamp: '1 hour ago',
      status: 'error',
      user: 'System'
    },
    {
      id: '4',
      type: 'team_invite',
      title: 'New team member joined',
      description: 'Carol Davis accepted invitation to Marketing team',
      timestamp: '3 hours ago',
      status: 'success',
      user: 'Carol Davis'
    }
  ]);

  // Quick actions for speed dial
  const quickActions: QuickAction[] = [
    {
      icon: <WorkflowIcon />,
      label: 'New Workflow',
      onClick: () => handleQuickAction('new_workflow'),
      color: theme.palette.primary.main
    },
    {
      icon: <AIIcon />,
      label: 'AI Assistant',
      onClick: () => handleQuickAction('ai_assistant'),
      color: theme.palette.secondary.main
    },
    {
      icon: <AnalyticsIcon />,
      label: 'Quick Report',
      onClick: () => handleQuickAction('quick_report'),
      color: theme.palette.info.main
    },
    {
      icon: <HelpIcon />,
      label: 'Get Help',
      onClick: () => handleQuickAction('help'),
      color: theme.palette.warning.main
    }
  ];

  // Navigation items
  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
    { id: 'workflows', label: 'Workflows', icon: <WorkflowIcon /> },
    { id: 'analytics', label: 'Analytics', icon: <AnalyticsIcon /> },
    { id: 'templates', label: 'Templates', icon: <AIIcon /> },
    { id: 'team', label: 'Team', icon: <PeopleIcon /> },
    { id: 'settings', label: 'Settings', icon: <SettingsIcon /> },
  ];

  // Handlers
  const handleQuickAction = (action: string) => {
    setSpeedDialOpen(false);
    
    switch (action) {
      case 'new_workflow':
        // Navigate to workflow builder
        setSnackbar({ open: true, message: 'Opening workflow builder...', severity: 'info' });
        break;
      case 'ai_assistant':
        // Open AI assistant
        setSnackbar({ open: true, message: 'AI Assistant coming soon!', severity: 'info' });
        break;
      case 'quick_report':
        // Generate quick report
        setSnackbar({ open: true, message: 'Generating report...', severity: 'info' });
        break;
      case 'help':
        // Open help center
        setSnackbar({ open: true, message: 'Opening help center...', severity: 'info' });
        break;
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    setRefreshing(false);
    setSnackbar({ open: true, message: 'Dashboard refreshed!', severity: 'success' });
  };

  const handleUserMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    setUserMenuAnchor(event.currentTarget);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return theme.palette.success.main;
      case 'error': return theme.palette.error.main;
      case 'warning': return theme.palette.warning.main;
      case 'info': return theme.palette.info.main;
      default: return theme.palette.grey[500];
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return <SuccessIcon />;
      case 'error': return <ErrorIcon />;
      case 'warning': return <ScheduleIcon />;
      case 'info': return <AnalyticsIcon />;
      default: return <AnalyticsIcon />;
    }
  };

  // Responsive grid sizing
  const getGridSize = () => {
    if (isMobile) return { xs: 12, sm: 6 };
    if (isTablet) return { xs: 12, sm: 6, md: 3 };
    return { xs: 12, sm: 6, md: 3, lg: 3 };
  };

  return (
    <Box sx={{ flexGrow: 1, bgcolor: 'background.default', minHeight: '100vh' }}>
      {/* App Bar */}
      <AppBar position="sticky" elevation={0} sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Toolbar>
          {isMobile && (
            <IconButton
              edge="start"
              color="inherit"
              onClick={() => setMobileMenuOpen(true)}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            RelayPoint Elite
          </Typography>
          
          <IconButton
            color="inherit"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            <RefreshIcon />
          </IconButton>
          
          <IconButton color="inherit">
            <Badge badgeContent={unreadCount} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
          
          <IconButton
            color="inherit"
            onClick={handleUserMenuClick}
            sx={{ ml: 1 }}
          >
            <Avatar sx={{ width: 32, height: 32 }}>
              {user?.name?.charAt(0) || 'D'}
            </Avatar>
          </IconButton>
        </Toolbar>
        
        {refreshing && <LinearProgress />}
      </AppBar>

      {/* Mobile Navigation Drawer */}
      <Drawer
        anchor="left"
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        sx={{ '& .MuiDrawer-paper': { width: 280 } }}
      >
        <Box sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Navigation
          </Typography>
          <List>
            {navigationItems.map((item) => (
              <ListItemButton
                key={item.id}
                selected={selectedTab === item.id}
                onClick={() => {
                  setSelectedTab(item.id);
                  setMobileMenuOpen(false);
                }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* User Menu */}
      <Menu
        anchorEl={userMenuAnchor}
        open={Boolean(userMenuAnchor)}
        onClose={() => setUserMenuAnchor(null)}
      >
        <MenuItem onClick={() => setUserMenuAnchor(null)}>Profile</MenuItem>
        <MenuItem onClick={() => setUserMenuAnchor(null)}>Settings</MenuItem>
        <Divider />
        <MenuItem onClick={() => setUserMenuAnchor(null)}>Logout</MenuItem>
      </Menu>

      {/* Main Content */}
      <Box sx={{ p: isMobile ? 2 : 3 }}>
        {/* Welcome Section */}
        <Box sx={{ mb: 3 }}>
          <Typography variant={isMobile ? "h5" : "h4"} gutterBottom>
            Welcome back, {user?.name?.split(' ')[0] || 'Debalent'}! 👋
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Here's what's happening with your workflows today.
          </Typography>
        </Box>

        {/* Metrics Cards */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {metrics.map((metric, index) => (
            <Grid item {...getGridSize()} key={index}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box>
                      <Typography variant="h4" sx={{ color: metric.color, fontWeight: 'bold' }}>
                        {metric.value}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {metric.title}
                      </Typography>
                      {metric.subtitle && (
                        <Typography variant="caption" color="text.secondary">
                          {metric.subtitle}
                        </Typography>
                      )}
                    </Box>
                    <Box sx={{ color: metric.color }}>
                      {metric.icon}
                    </Box>
                  </Box>
                  
                  {metric.change && (
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      <TrendingUpIcon 
                        color={metric.change > 0 ? "success" : "error"} 
                        fontSize="small" 
                      />
                      <Typography
                        variant="caption"
                        sx={{ 
                          color: metric.change > 0 ? 'success.main' : 'error.main',
                          ml: 0.5 
                        }}
                      >
                        {Math.abs(metric.change)}% from last period
                      </Typography>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Recent Activity */}
        <Grid container spacing={3}>
          <Grid item xs={12} lg={8}>
            <Card>
              <CardHeader 
                title="Recent Activity" 
                action={
                  <Button size="small" startIcon={<AnalyticsIcon />}>
                    View All
                  </Button>
                }
              />
              <CardContent sx={{ p: 0 }}>
                <List>
                  {recentActivities.map((activity, index) => (
                    <React.Fragment key={activity.id}>
                      <ListItem>
                        <ListItemIcon sx={{ color: getStatusColor(activity.status || 'info') }}>
                          {getStatusIcon(activity.status || 'info')}
                        </ListItemIcon>
                        <ListItemText
                          primary={activity.title}
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                {activity.description}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {activity.timestamp} • {activity.user}
                              </Typography>
                            </Box>
                          }
                        />
                        {activity.status && (
                          <Chip
                            label={activity.status}
                            size="small"
                            color={activity.status === 'success' ? 'success' : 
                                   activity.status === 'error' ? 'error' : 'default'}
                            variant="outlined"
                          />
                        )}
                      </ListItem>
                      {index < recentActivities.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Quick Actions Card */}
          <Grid item xs={12} lg={4}>
            <Card sx={{ height: '100%' }}>
              <CardHeader title="Quick Actions" />
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<WorkflowIcon />}
                      onClick={() => handleQuickAction('new_workflow')}
                    >
                      New Workflow
                    </Button>
                  </Grid>
                  <Grid item xs={6}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<AIIcon />}
                      onClick={() => handleQuickAction('ai_assistant')}
                    >
                      AI Help
                    </Button>
                  </Grid>
                  <Grid item xs={6}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<AnalyticsIcon />}
                      onClick={() => handleQuickAction('quick_report')}
                    >
                      Reports
                    </Button>
                  </Grid>
                  <Grid item xs={6}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<HelpIcon />}
                      onClick={() => handleQuickAction('help')}
                    >
                      Help
                    </Button>
                  </Grid>
                </Grid>

                <Divider sx={{ my: 2 }} />

                <Typography variant="subtitle2" gutterBottom>
                  Popular Templates
                </Typography>
                <List dense>
                  <ListItemButton>
                    <ListItemText primary="Customer Onboarding" secondary="Most used" />
                  </ListItemButton>
                  <ListItemButton>
                    <ListItemText primary="Invoice Processing" secondary="High efficiency" />
                  </ListItemButton>
                  <ListItemButton>
                    <ListItemText primary="Lead Qualification" secondary="New" />
                  </ListItemButton>
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>

      {/* Floating Action Button / Speed Dial */}
      <SpeedDial
        ariaLabel="Quick Actions"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
        open={speedDialOpen}
        onClose={() => setSpeedDialOpen(false)}
        onOpen={() => setSpeedDialOpen(true)}
      >
        {quickActions.map((action) => (
          <SpeedDialAction
            key={action.label}
            icon={action.icon}
            tooltipTitle={action.label}
            onClick={action.onClick}
          />
        ))}
      </SpeedDial>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default MobileEliteDashboard;