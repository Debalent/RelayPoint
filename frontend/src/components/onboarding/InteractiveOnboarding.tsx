/**
 * Interactive User Onboarding Experience
 * 
 * This component provides a guided, step-by-step onboarding process that addresses
 * common user feedback about complexity and learning curve.
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
  Typography,
  Card,
  CardContent,
  CardActions,
  Grid,
  Avatar,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  RadioGroup,
  Radio,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Paper,
  Divider,
  LinearProgress,
  Fade,
  Slide,
  Zoom,
  useTheme,
  useMediaQuery,
} from '@mui/material';

import {
  CheckCircle as CheckIcon,
  PlayArrow as PlayIcon,
  Settings as SettingsIcon,
  People as PeopleIcon,
  Lightbulb as LightbulbIcon,
  Timeline as TimelineIcon,
  AutoFixHigh as AutoFixIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  TrendingUp as GrowthIcon,
  Favorite as FavoriteIcon,
  Star as StarIcon,
  Rocket as RocketIcon,
  EmojiObjects as IdeaIcon,
  Build as BuildIcon,
  Analytics as AnalyticsIcon,
  SmartToy as AIIcon,
  Group as TeamIcon,
  AccountCircle as ProfileIcon,
  Notifications as NotificationIcon,
  Integration as IntegrationIcon,
  School as LearnIcon,
} from '@mui/icons-material';

// Types
interface OnboardingStep {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  content: React.ReactNode;
  optional?: boolean;
  estimatedTime?: string;
}

interface UserPreferences {
  role: string;
  experience: string;
  goals: string[];
  teamSize: string;
  industry: string;
  useCase: string;
  notifications: boolean;
  tutorials: boolean;
}

interface TemplateRecommendation {
  id: string;
  name: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedSetupTime: string;
  popularityScore: number;
  icon: React.ReactNode;
}

const InteractiveOnboarding: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // State
  const [activeStep, setActiveStep] = useState(0);
  const [completed, setCompleted] = useState<{ [key: number]: boolean }>({});
  const [preferences, setPreferences] = useState<UserPreferences>({
    role: '',
    experience: '',
    goals: [],
    teamSize: '',
    industry: '',
    useCase: '',
    notifications: true,
    tutorials: true,
  });
  const [showWelcome, setShowWelcome] = useState(true);
  const [recommendedTemplates, setRecommendedTemplates] = useState<TemplateRecommendation[]>([]);
  const [selectedTemplates, setSelectedTemplates] = useState<string[]>([]);
  const [progress, setProgress] = useState(0);

  // Template recommendations based on preferences
  const allTemplates: TemplateRecommendation[] = [
    {
      id: 'customer-onboarding',
      name: 'Customer Onboarding',
      description: 'Automate new customer welcome process with email sequences and task assignments',
      category: 'Customer Success',
      difficulty: 'beginner',
      estimatedSetupTime: '15 minutes',
      popularityScore: 95,
      icon: <TeamIcon />
    },
    {
      id: 'invoice-processing',
      name: 'Invoice Processing',
      description: 'Streamline vendor payments with automated approval workflows',
      category: 'Finance',
      difficulty: 'intermediate',
      estimatedSetupTime: '30 minutes',
      popularityScore: 87,
      icon: <AnalyticsIcon />
    },
    {
      id: 'lead-qualification',
      name: 'Lead Qualification',
      description: 'Score and route leads automatically based on custom criteria',
      category: 'Sales',
      difficulty: 'intermediate',
      estimatedSetupTime: '25 minutes',
      popularityScore: 92,
      icon: <GrowthIcon />
    },
    {
      id: 'employee-onboarding',
      name: 'Employee Onboarding',
      description: 'Create comprehensive new hire workflows with document collection',
      category: 'HR',
      difficulty: 'beginner',
      estimatedSetupTime: '20 minutes',
      popularityScore: 89,
      icon: <PeopleIcon />
    },
    {
      id: 'support-tickets',
      name: 'Support Ticket Routing',
      description: 'Automatically categorize and assign support requests',
      category: 'Customer Support',
      difficulty: 'advanced',
      estimatedSetupTime: '45 minutes',
      popularityScore: 84,
      icon: <SettingsIcon />
    },
    {
      id: 'content-approval',
      name: 'Content Approval',
      description: 'Manage content review and approval processes',
      category: 'Marketing',
      difficulty: 'beginner',
      estimatedSetupTime: '15 minutes',
      popularityScore: 78,
      icon: <StarIcon />
    }
  ];

  // Calculate progress
  useEffect(() => {
    const totalSteps = onboardingSteps.length;
    const completedSteps = Object.keys(completed).length;
    setProgress((completedSteps / totalSteps) * 100);
  }, [completed]);

  // Update recommendations based on preferences
  useEffect(() => {
    const filtered = allTemplates.filter(template => {
      // Filter based on role and industry
      if (preferences.role === 'sales' && template.category === 'Sales') return true;
      if (preferences.role === 'marketing' && template.category === 'Marketing') return true;
      if (preferences.role === 'hr' && template.category === 'HR') return true;
      if (preferences.role === 'finance' && template.category === 'Finance') return true;
      if (preferences.role === 'support' && template.category === 'Customer Support') return true;
      
      // Show popular templates for beginners
      if (preferences.experience === 'beginner' && template.popularityScore > 85) return true;
      
      // Show all templates if no specific role selected
      if (!preferences.role) return template.popularityScore > 80;
      
      return false;
    });
    
    setRecommendedTemplates(filtered.slice(0, 4));
  }, [preferences]);

  // Welcome Component
  const WelcomeStep = () => (
    <Box textAlign="center" sx={{ py: 4 }}>
      <Avatar
        sx={{ 
          width: 80, 
          height: 80, 
          mx: 'auto', 
          mb: 3,
          bgcolor: 'primary.main',
          fontSize: '2rem'
        }}
      >
        <RocketIcon fontSize="large" />
      </Avatar>
      
      <Typography variant="h4" gutterBottom>
        Welcome to RelayPoint Elite! 🎉
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto', mb: 4 }}>
        We're excited to help you automate your workflows and boost productivity. 
        This quick setup will personalize your experience and get you started with templates 
        that match your needs.
      </Typography>
      
      <Grid container spacing={2} justifyContent="center" sx={{ mb: 4 }}>
        <Grid item xs={6} sm={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <SpeedIcon color="primary" />
            <Typography variant="caption" display="block">
              Save 10+ hours/week
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <AIIcon color="primary" />
            <Typography variant="caption" display="block">
              AI-Powered
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <SecurityIcon color="primary" />
            <Typography variant="caption" display="block">
              Enterprise Security
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <IntegrationIcon color="primary" />
            <Typography variant="caption" display="block">
              100+ Integrations
            </Typography>
          </Paper>
        </Grid>
      </Grid>
      
      <Typography variant="body2" color="text.secondary">
        ⏱️ This should take about 5 minutes
      </Typography>
    </Box>
  );

  // Profile Setup Component
  const ProfileStep = () => (
    <Box sx={{ py: 2 }}>
      <Typography variant="h6" gutterBottom>
        Tell us about yourself
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        This helps us recommend the best workflows for your needs.
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>What's your primary role?</InputLabel>
            <Select
              value={preferences.role}
              onChange={(e) => setPreferences(prev => ({ ...prev, role: e.target.value }))}
            >
              <MenuItem value="sales">Sales</MenuItem>
              <MenuItem value="marketing">Marketing</MenuItem>
              <MenuItem value="hr">Human Resources</MenuItem>
              <MenuItem value="finance">Finance</MenuItem>
              <MenuItem value="operations">Operations</MenuItem>
              <MenuItem value="support">Customer Support</MenuItem>
              <MenuItem value="it">IT/Engineering</MenuItem>
              <MenuItem value="executive">Executive/Management</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>Experience with automation?</InputLabel>
            <Select
              value={preferences.experience}
              onChange={(e) => setPreferences(prev => ({ ...prev, experience: e.target.value }))}
            >
              <MenuItem value="beginner">Just getting started</MenuItem>
              <MenuItem value="intermediate">Some experience</MenuItem>
              <MenuItem value="advanced">Very experienced</MenuItem>
              <MenuItem value="expert">Expert level</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>Team size?</InputLabel>
            <Select
              value={preferences.teamSize}
              onChange={(e) => setPreferences(prev => ({ ...prev, teamSize: e.target.value }))}
            >
              <MenuItem value="solo">Just me</MenuItem>
              <MenuItem value="small">2-10 people</MenuItem>
              <MenuItem value="medium">11-50 people</MenuItem>
              <MenuItem value="large">51-200 people</MenuItem>
              <MenuItem value="enterprise">200+ people</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>Industry</InputLabel>
            <Select
              value={preferences.industry}
              onChange={(e) => setPreferences(prev => ({ ...prev, industry: e.target.value }))}
            >
              <MenuItem value="technology">Technology</MenuItem>
              <MenuItem value="healthcare">Healthcare</MenuItem>
              <MenuItem value="finance">Financial Services</MenuItem>
              <MenuItem value="education">Education</MenuItem>
              <MenuItem value="retail">Retail/E-commerce</MenuItem>
              <MenuItem value="manufacturing">Manufacturing</MenuItem>
              <MenuItem value="consulting">Consulting</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>
    </Box>
  );

  // Goals Selection Component
  const GoalsStep = () => {
    const goalOptions = [
      { id: 'efficiency', label: 'Increase team efficiency', icon: <SpeedIcon /> },
      { id: 'costs', label: 'Reduce operational costs', icon: <AnalyticsIcon /> },
      { id: 'errors', label: 'Minimize human errors', icon: <CheckIcon /> },
      { id: 'scaling', label: 'Scale operations', icon: <GrowthIcon /> },
      { id: 'compliance', label: 'Improve compliance', icon: <SecurityIcon /> },
      { id: 'customer', label: 'Enhance customer experience', icon: <FavoriteIcon /> },
      { id: 'data', label: 'Better data insights', icon: <AnalyticsIcon /> },
      { id: 'integration', label: 'Connect existing tools', icon: <IntegrationIcon /> },
    ];

    const handleGoalToggle = (goalId: string) => {
      setPreferences(prev => ({
        ...prev,
        goals: prev.goals.includes(goalId)
          ? prev.goals.filter(g => g !== goalId)
          : [...prev.goals, goalId]
      }));
    };

    return (
      <Box sx={{ py: 2 }}>
        <Typography variant="h6" gutterBottom>
          What are your main goals?
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Select all that apply. This helps us prioritize features for you.
        </Typography>
        
        <Grid container spacing={2}>
          {goalOptions.map((goal) => (
            <Grid item xs={12} sm={6} md={4} key={goal.id}>
              <Card
                sx={{
                  cursor: 'pointer',
                  border: preferences.goals.includes(goal.id) ? 2 : 1,
                  borderColor: preferences.goals.includes(goal.id) 
                    ? 'primary.main' 
                    : 'divider',
                  bgcolor: preferences.goals.includes(goal.id) 
                    ? 'primary.50' 
                    : 'background.paper',
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: 'primary.main',
                    transform: 'translateY(-2px)',
                  }
                }}
                onClick={() => handleGoalToggle(goal.id)}
              >
                <CardContent sx={{ textAlign: 'center', py: 3 }}>
                  <Box sx={{ color: 'primary.main', mb: 1 }}>
                    {goal.icon}
                  </Box>
                  <Typography variant="body2" fontWeight="medium">
                    {goal.label}
                  </Typography>
                  {preferences.goals.includes(goal.id) && (
                    <Chip
                      icon={<CheckIcon />}
                      label="Selected"
                      size="small"
                      color="primary"
                      sx={{ mt: 1 }}
                    />
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  };

  // Template Selection Component
  const TemplatesStep = () => (
    <Box sx={{ py: 2 }}>
      <Typography variant="h6" gutterBottom>
        Recommended workflow templates
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Based on your profile, here are some templates to get you started quickly.
      </Typography>
      
      <Grid container spacing={2}>
        {recommendedTemplates.map((template) => (
          <Grid item xs={12} sm={6} key={template.id}>
            <Card
              sx={{
                cursor: 'pointer',
                border: selectedTemplates.includes(template.id) ? 2 : 1,
                borderColor: selectedTemplates.includes(template.id) 
                  ? 'primary.main' 
                  : 'divider',
                transition: 'all 0.2s',
                '&:hover': {
                  borderColor: 'primary.main',
                  transform: 'translateY(-2px)',
                }
              }}
              onClick={() => {
                setSelectedTemplates(prev =>
                  prev.includes(template.id)
                    ? prev.filter(id => id !== template.id)
                    : [...prev, template.id]
                );
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2, width: 40, height: 40 }}>
                    {template.icon}
                  </Avatar>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {template.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {template.description}
                    </Typography>
                  </Box>
                  {selectedTemplates.includes(template.id) && (
                    <CheckIcon color="primary" />
                  )}
                </Box>
                
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', alignItems: 'center' }}>
                  <Chip
                    label={template.category}
                    size="small"
                    variant="outlined"
                  />
                  <Chip
                    label={template.difficulty}
                    size="small"
                    color={
                      template.difficulty === 'beginner' ? 'success' :
                      template.difficulty === 'intermediate' ? 'warning' : 'error'
                    }
                  />
                  <Typography variant="caption" color="text.secondary">
                    {template.estimatedSetupTime}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {selectedTemplates.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <IdeaIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
          <Typography variant="body2" color="text.secondary">
            You can always explore templates later in the Template Library
          </Typography>
        </Box>
      )}
    </Box>
  );

  // Preferences Component
  const PreferencesStep = () => (
    <Box sx={{ py: 2 }}>
      <Typography variant="h6" gutterBottom>
        Final preferences
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Set up your notification and learning preferences.
      </Typography>
      
      <List>
        <ListItem>
          <FormControlLabel
            control={
              <Checkbox
                checked={preferences.notifications}
                onChange={(e) => setPreferences(prev => ({ 
                  ...prev, 
                  notifications: e.target.checked 
                }))}
              />
            }
            label="Receive workflow notifications and updates"
          />
        </ListItem>
        
        <ListItem>
          <FormControlLabel
            control={
              <Checkbox
                checked={preferences.tutorials}
                onChange={(e) => setPreferences(prev => ({ 
                  ...prev, 
                  tutorials: e.target.checked 
                }))}
              />
            }
            label="Show helpful tips and tutorials"
          />
        </ListItem>
      </List>
      
      <Paper sx={{ p: 3, mt: 3, bgcolor: 'primary.50' }}>
        <Typography variant="subtitle2" gutterBottom>
          🎯 Your personalized setup summary:
        </Typography>
        <Typography variant="body2" color="text.secondary">
          • Role: {preferences.role || 'Not specified'}<br />
          • Experience: {preferences.experience || 'Not specified'}<br />
          • Team size: {preferences.teamSize || 'Not specified'}<br />
          • Selected goals: {preferences.goals.length} goals<br />
          • Templates to install: {selectedTemplates.length} templates
        </Typography>
      </Paper>
    </Box>
  );

  // Define onboarding steps
  const onboardingSteps: OnboardingStep[] = [
    {
      id: 'welcome',
      title: 'Welcome',
      description: 'Let\'s get you started',
      icon: <RocketIcon />,
      content: <WelcomeStep />,
      estimatedTime: '1 min'
    },
    {
      id: 'profile',
      title: 'Profile Setup',
      description: 'Tell us about yourself',
      icon: <ProfileIcon />,
      content: <ProfileStep />,
      estimatedTime: '2 min'
    },
    {
      id: 'goals',
      title: 'Your Goals',
      description: 'What do you want to achieve?',
      icon: <GrowthIcon />,
      content: <GoalsStep />,
      estimatedTime: '1 min'
    },
    {
      id: 'templates',
      title: 'Choose Templates',
      description: 'Select workflow templates',
      icon: <BuildIcon />,
      content: <TemplatesStep />,
      estimatedTime: '2 min'
    },
    {
      id: 'preferences',
      title: 'Preferences',
      description: 'Final setup',
      icon: <SettingsIcon />,
      content: <PreferencesStep />,
      estimatedTime: '1 min'
    }
  ];

  // Handlers
  const handleNext = () => {
    setCompleted(prev => ({ ...prev, [activeStep]: true }));
    setActiveStep(prev => prev + 1);
  };

  const handleBack = () => {
    setActiveStep(prev => prev - 1);
  };

  const handleComplete = () => {
    // Save preferences and redirect to dashboard
    console.log('Onboarding completed with preferences:', preferences);
    console.log('Selected templates:', selectedTemplates);
    
    // Here you would typically:
    // 1. Send data to backend
    // 2. Install selected templates
    // 3. Redirect to dashboard
    alert('Welcome to RelayPoint Elite! Your workspace is being set up...');
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      {/* Progress Bar */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="h5">Setup Progress</Typography>
          <Typography variant="body2" color="text.secondary">
            {Math.round(progress)}% Complete
          </Typography>
        </Box>
        <LinearProgress variant="determinate" value={progress} sx={{ height: 6, borderRadius: 3 }} />
      </Box>

      {/* Stepper */}
      <Stepper 
        activeStep={activeStep} 
        orientation={isMobile ? "vertical" : "horizontal"}
        sx={{ mb: 4 }}
      >
        {onboardingSteps.map((step, index) => (
          <Step key={step.id} completed={completed[index]}>
            <StepLabel
              icon={step.icon}
              optional={
                step.estimatedTime && (
                  <Typography variant="caption">{step.estimatedTime}</Typography>
                )
              }
            >
              {step.title}
            </StepLabel>
            {isMobile && (
              <StepContent>
                <Typography variant="body2" color="text.secondary">
                  {step.description}
                </Typography>
              </StepContent>
            )}
          </Step>
        ))}
      </Stepper>

      {/* Step Content */}
      <Card sx={{ minHeight: 400 }}>
        <CardContent>
          {activeStep < onboardingSteps.length ? (
            <Fade in={true} key={activeStep}>
              <Box>
                {onboardingSteps[activeStep].content}
              </Box>
            </Fade>
          ) : (
            <Box textAlign="center" sx={{ py: 4 }}>
              <CheckIcon sx={{ fontSize: 64, color: 'success.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                All set! 🎉
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                Your workspace is ready. Let's start building amazing workflows!
              </Typography>
              <Button
                variant="contained"
                size="large"
                startIcon={<RocketIcon />}
                onClick={handleComplete}
              >
                Enter RelayPoint Elite
              </Button>
            </Box>
          )}
        </CardContent>
        
        {activeStep < onboardingSteps.length && (
          <CardActions sx={{ justifyContent: 'space-between', p: 3 }}>
            <Button
              onClick={handleBack}
              disabled={activeStep === 0}
              variant="outlined"
            >
              Back
            </Button>
            
            <Button
              onClick={handleNext}
              variant="contained"
              endIcon={activeStep === onboardingSteps.length - 1 ? <CheckIcon /> : <PlayIcon />}
            >
              {activeStep === onboardingSteps.length - 1 ? 'Complete Setup' : 'Continue'}
            </Button>
          </CardActions>
        )}
      </Card>
    </Box>
  );
};

export default InteractiveOnboarding;