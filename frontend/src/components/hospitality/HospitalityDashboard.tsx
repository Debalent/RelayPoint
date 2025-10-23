import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Avatar,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  Alert,
  Fab,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Badge,
  AppBar,
  Toolbar,
  BottomNavigation,
  BottomNavigationAction,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Snackbar
} from '@mui/material';
import {
  Hotel as HotelIcon,
  CleaningServices as CleaningIcon,
  Build as MaintenanceIcon,
  Restaurant as RestaurantIcon,
  EventSeat as EventIcon,
  AdminPanelSettings as AdminIcon,
  Notifications as NotificationsIcon,
  Mic as MicIcon,
  MicOff as MicOffIcon,
  Translate as TranslateIcon,
  Accessibility as AccessibilityIcon,
  Phone as PhoneIcon,
  Chat as ChatIcon,
  Assignment as TaskIcon,
  People as PeopleIcon,
  Schedule as ScheduleIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Send as SendIcon,
  VolumeUp as VolumeUpIcon,
  TextIncrease as TextIncreaseIcon,
  Contrast as ContrastIcon
} from '@mui/icons-material';
import { useTheme } from '@mui/material/styles';
import { styled } from '@mui/material/styles';

// Types from our hospitality config
interface HospitalityTask {
  id: string;
  title: string;
  description: string;
  role: string;
  priority: 'urgent' | 'high' | 'medium' | 'low';
  status: 'pending' | 'in_progress' | 'completed' | 'escalated';
  department: string;
  guestRoom?: string;
  guestName?: string;
  estimatedDuration?: number;
  createdAt: string;
  dueAt?: string;
  shift: string;
  guestImpact: boolean;
}

interface DepartmentAlert {
  id: string;
  message: string;
  fromDepartment: string;
  toDepartment: string;
  priority: 'urgent' | 'high' | 'medium' | 'low';
  alertType: string;
  createdAt: string;
  escalationCount: number;
}

// Styled components for accessibility
const AccessibleCard = styled(Card)<{ highContrast?: boolean; largeText?: boolean }>(
  ({ theme, highContrast, largeText }) => ({
    marginBottom: theme.spacing(2),
    backgroundColor: highContrast ? '#000000' : undefined,
    color: highContrast ? '#FFFFFF' : undefined,
    fontSize: largeText ? '1.2rem' : undefined,
    touchAction: 'manipulation', // Better mobile experience
    minHeight: '64px', // Adequate touch target
    '& .MuiCardContent-root': {
      padding: largeText ? theme.spacing(3) : theme.spacing(2)
    }
  })
);

const AccessibleButton = styled(Button)<{ largeText?: boolean }>(
  ({ theme, largeText }) => ({
    minHeight: '44px', // Mobile touch target
    fontSize: largeText ? '1.1rem' : undefined,
    padding: largeText ? theme.spacing(2, 3) : undefined
  })
);

// Language support
const translations = {
  en: {
    dashboard: 'Dashboard',
    tasks: 'Tasks',
    alerts: 'Alerts',
    communication: 'Communication',
    shiftHandoff: 'Shift Handoff',
    urgent: 'Urgent',
    high: 'High',
    medium: 'Medium',
    low: 'Low',
    pending: 'Pending',
    inProgress: 'In Progress',
    completed: 'Completed',
    escalated: 'Escalated',
    startTask: 'Start Task',
    completeTask: 'Complete Task',
    needHelp: 'Need Help',
    voiceNote: 'Voice Note',
    translate: 'Translate',
    accessibility: 'Accessibility',
    largeText: 'Large Text',
    highContrast: 'High Contrast',
    screenReader: 'Screen Reader',
    guestWaiting: 'Guest Waiting',
    maintenanceNeeded: 'Maintenance Needed',
    housekeepingRequired: 'Housekeeping Required',
    frontDesk: 'Front Desk',
    housekeeping: 'Housekeeping',
    maintenance: 'Maintenance',
    banquetEvents: 'Banquet & Events',
    barRestaurant: 'Bar & Restaurant',
    management: 'Management'
  },
  es: {
    dashboard: 'Panel',
    tasks: 'Tareas',
    alerts: 'Alertas',
    communication: 'Comunicación',
    shiftHandoff: 'Cambio de Turno',
    urgent: 'Urgente',
    high: 'Alto',
    medium: 'Medio',
    low: 'Bajo',
    pending: 'Pendiente',
    inProgress: 'En Progreso',
    completed: 'Completado',
    escalated: 'Escalado',
    startTask: 'Iniciar Tarea',
    completeTask: 'Completar Tarea',
    needHelp: 'Necesito Ayuda',
    voiceNote: 'Nota de Voz',
    translate: 'Traducir',
    accessibility: 'Accesibilidad',
    largeText: 'Texto Grande',
    highContrast: 'Alto Contraste',
    screenReader: 'Lector de Pantalla',
    guestWaiting: 'Huésped Esperando',
    maintenanceNeeded: 'Mantenimiento Necesario',
    housekeepingRequired: 'Limpieza Requerida',
    frontDesk: 'Recepción',
    housekeeping: 'Limpieza',
    maintenance: 'Mantenimiento',
    banquetEvents: 'Banquetes y Eventos',
    barRestaurant: 'Bar y Restaurante',
    management: 'Gerencia'
  },
  fr: {
    dashboard: 'Tableau de Bord',
    tasks: 'Tâches',
    alerts: 'Alertes',
    communication: 'Communication',
    shiftHandoff: 'Changement d\'Équipe',
    urgent: 'Urgent',
    high: 'Élevé',
    medium: 'Moyen',
    low: 'Bas',
    pending: 'En Attente',
    inProgress: 'En Cours',
    completed: 'Terminé',
    escalated: 'Escaladé',
    startTask: 'Commencer la Tâche',
    completeTask: 'Terminer la Tâche',
    needHelp: 'Besoin d\'Aide',
    voiceNote: 'Note Vocale',
    translate: 'Traduire',
    accessibility: 'Accessibilité',
    largeText: 'Texte Large',
    highContrast: 'Contraste Élevé',
    screenReader: 'Lecteur d\'Écran',
    guestWaiting: 'Client en Attente',
    maintenanceNeeded: 'Maintenance Nécessaire',
    housekeepingRequired: 'Ménage Requis',
    frontDesk: 'Réception',
    housekeeping: 'Ménage',
    maintenance: 'Maintenance',
    banquetEvents: 'Banquets et Événements',
    barRestaurant: 'Bar et Restaurant',
    management: 'Direction'
  }
};

const HospitalityDashboard: React.FC = () => {
  // State management
  const [language, setLanguage] = useState<'en' | 'es' | 'fr'>('en');
  const [accessibility, setAccessibility] = useState({
    largeText: false,
    highContrast: false,
    screenReader: false,
    voiceCommands: false
  });
  const [currentUser, setCurrentUser] = useState({
    role: 'front_desk',
    department: 'front_desk',
    name: 'Staff Member',
    shift: 'morning'
  });
  const [tasks, setTasks] = useState<HospitalityTask[]>([]);
  const [alerts, setAlerts] = useState<DepartmentAlert[]>([]);
  const [bottomNavValue, setBottomNavValue] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' as 'success' | 'error' | 'warning' | 'info' });
  
  // Voice recognition
  const recognition = useRef<any>(null);
  const theme = useTheme();
  const t = translations[language];

  // Initialize voice recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      recognition.current = new SpeechRecognition();
      recognition.current.continuous = false;
      recognition.current.interimResults = false;
      recognition.current.lang = language === 'es' ? 'es-ES' : language === 'fr' ? 'fr-FR' : 'en-US';
      
      recognition.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        handleVoiceCommand(transcript);
        setIsRecording(false);
      };
      
      recognition.current.onerror = () => {
        setIsRecording(false);
        showSnackbar('Voice recognition error', 'error');
      };
    }
  }, [language]);

  // Sample data loading
  useEffect(() => {
    loadSampleData();
  }, [currentUser.role]);

  const loadSampleData = () => {
    // Sample tasks based on survey feedback scenarios
    const sampleTasks: HospitalityTask[] = [
      {
        id: '1',
        title: 'Guest Checkout - Room 312',
        description: 'Process checkout for Smith family, check for damages',
        role: 'front_desk',
        priority: 'high',
        status: 'pending',
        department: 'front_desk',
        guestRoom: '312',
        guestName: 'Smith Family',
        estimatedDuration: 15,
        createdAt: new Date().toISOString(),
        shift: 'morning',
        guestImpact: true
      },
      {
        id: '2',
        title: 'Maintenance Request - AC Unit Room 205',
        description: 'Guest reports AC not working properly',
        role: 'maintenance',
        priority: 'urgent',
        status: 'escalated',
        department: 'maintenance',
        guestRoom: '205',
        estimatedDuration: 45,
        createdAt: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        shift: 'morning',
        guestImpact: true
      },
      {
        id: '3',
        title: 'Event Setup - Wedding Reception',
        description: 'Set up ballroom for 150 guests, coordinate with catering',
        role: 'banquet_event',
        priority: 'high',
        status: 'in_progress',
        department: 'banquet_events',
        estimatedDuration: 120,
        createdAt: new Date().toISOString(),
        shift: 'morning',
        guestImpact: true
      }
    ];

    const sampleAlerts: DepartmentAlert[] = [
      {
        id: '1',
        message: 'Guest in room 312 requesting early checkout assistance',
        fromDepartment: 'housekeeping',
        toDepartment: 'front_desk',
        priority: 'high',
        alertType: 'guest_request',
        createdAt: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
        escalationCount: 1
      },
      {
        id: '2',
        message: 'Low towel inventory - need restocking ASAP',
        fromDepartment: 'housekeeping',
        toDepartment: 'management',
        priority: 'medium',
        alertType: 'inventory_low',
        createdAt: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        escalationCount: 0
      }
    ];

    setTasks(sampleTasks.filter(task => task.role === currentUser.role || task.department === currentUser.department));
    setAlerts(sampleAlerts);
  };

  const handleVoiceCommand = (transcript: string) => {
    const command = transcript.toLowerCase();
    
    if (command.includes('complete') || command.includes('done') || command.includes('finish')) {
      // Complete first pending task
      const pendingTask = tasks.find(task => task.status === 'pending');
      if (pendingTask) {
        handleTaskAction(pendingTask.id, 'complete');
        showSnackbar(`Task "${pendingTask.title}" marked as completed`, 'success');
      }
    } else if (command.includes('help') || command.includes('assistance')) {
      sendQuickMessage('need_assistance');
    } else if (command.includes('urgent') || command.includes('emergency')) {
      sendQuickMessage('guest_waiting');
    } else {
      // Add as voice note to first active task
      const activeTask = tasks.find(task => task.status === 'in_progress');
      if (activeTask) {
        showSnackbar('Voice note added to task', 'success');
      }
    }
  };

  const startVoiceRecording = () => {
    if (recognition.current && accessibility.voiceCommands) {
      setIsRecording(true);
      recognition.current.start();
    }
  };

  const handleTaskAction = (taskId: string, action: 'start' | 'complete' | 'escalate') => {
    setTasks(prev => prev.map(task => {
      if (task.id === taskId) {
        switch (action) {
          case 'start':
            return { ...task, status: 'in_progress' as const };
          case 'complete':
            return { ...task, status: 'completed' as const };
          case 'escalate':
            return { ...task, status: 'escalated' as const };
          default:
            return task;
        }
      }
      return task;
    }));
  };

  const sendQuickMessage = (messageType: string) => {
    const messages = {
      need_assistance: t.needHelp,
      guest_waiting: t.guestWaiting,
      maintenance_needed: t.maintenanceNeeded,
      housekeeping_required: t.housekeepingRequired
    };
    
    const message = messages[messageType] || messageType;
    // In real implementation, this would send to backend
    showSnackbar(`Message sent: ${message}`, 'success');
  };

  const showSnackbar = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setSnackbar({ open: true, message, severity });
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'urgent': return <ErrorIcon color="error" />;
      case 'high': return <WarningIcon color="warning" />;
      case 'medium': return <InfoIcon color="info" />;
      case 'low': return <InfoIcon color="action" />;
      default: return <InfoIcon />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'error';
      case 'high': return 'warning'; 
      case 'medium': return 'info';
      case 'low': return 'default';
      default: return 'default';
    }
  };

  const getDepartmentIcon = (department: string) => {
    switch (department) {
      case 'front_desk': return <HotelIcon />;
      case 'housekeeping': return <CleaningIcon />;
      case 'maintenance': return <MaintenanceIcon />;
      case 'banquet_events': return <EventIcon />;
      case 'bar_restaurant': return <RestaurantIcon />;
      case 'management': return <AdminIcon />;
      default: return <TaskIcon />;
    }
  };

  const TaskCard: React.FC<{ task: HospitalityTask }> = ({ task }) => (
    <AccessibleCard 
      highContrast={accessibility.highContrast}
      largeText={accessibility.largeText}
      aria-label={`Task: ${task.title}, Priority: ${task.priority}, Status: ${task.status}`}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Box display="flex" alignItems="center" gap={1}>
            {getDepartmentIcon(task.department)}
            <Typography 
              variant={accessibility.largeText ? "h6" : "subtitle1"} 
              fontWeight="bold"
            >
              {task.title}
            </Typography>
          </Box>
          <Box display="flex" gap={1}>
            <Chip 
              icon={getPriorityIcon(task.priority)}
              label={t[task.priority]}
              color={getPriorityColor(task.priority) as any}
              size={accessibility.largeText ? "medium" : "small"}
            />
            <Chip 
              label={t[task.status]}
              variant="outlined"
              size={accessibility.largeText ? "medium" : "small"}
            />
          </Box>
        </Box>

        <Typography 
          variant={accessibility.largeText ? "body1" : "body2"} 
          color="text.secondary" 
          mb={2}
        >
          {task.description}
        </Typography>

        {task.guestRoom && (
          <Box display="flex" alignItems="center" gap={1} mb={1}>
            <HotelIcon fontSize="small" />
            <Typography variant="caption">
              Room: {task.guestRoom} {task.guestName && `| Guest: ${task.guestName}`}
            </Typography>
          </Box>
        )}

        {task.estimatedDuration && (
          <Box display="flex" alignItems="center" gap={1} mb={2}>
            <ScheduleIcon fontSize="small" />
            <Typography variant="caption">
              Est. Duration: {task.estimatedDuration} minutes
            </Typography>
          </Box>
        )}

        <Box display="flex" gap={1} flexWrap="wrap">
          {task.status === 'pending' && (
            <AccessibleButton
              largeText={accessibility.largeText}
              variant="contained"
              color="primary"
              size="small"
              onClick={() => handleTaskAction(task.id, 'start')}
              aria-label={`Start task: ${task.title}`}
            >
              {t.startTask}
            </AccessibleButton>
          )}
          
          {task.status === 'in_progress' && (
            <AccessibleButton
              largeText={accessibility.largeText}
              variant="contained"
              color="success"
              size="small"
              onClick={() => handleTaskAction(task.id, 'complete')}
              aria-label={`Complete task: ${task.title}`}
            >
              {t.completeTask}
            </AccessibleButton>
          )}

          <AccessibleButton
            largeText={accessibility.largeText}
            variant="outlined"
            size="small"
            onClick={() => sendQuickMessage('need_assistance')}
            aria-label={`Get help with task: ${task.title}`}
          >
            {t.needHelp}
          </AccessibleButton>

          {accessibility.voiceCommands && (
            <IconButton
              color={isRecording ? "error" : "default"}
              onClick={startVoiceRecording}
              aria-label="Add voice note"
              size={accessibility.largeText ? "large" : "medium"}
            >
              {isRecording ? <MicOffIcon /> : <MicIcon />}
            </IconButton>
          )}
        </Box>
      </CardContent>
    </AccessibleCard>
  );

  const AlertCard: React.FC<{ alert: DepartmentAlert }> = ({ alert }) => (
    <AccessibleCard 
      highContrast={accessibility.highContrast}
      largeText={accessibility.largeText}
      aria-label={`Alert from ${alert.fromDepartment}: ${alert.message}`}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="between" mb={1}>
          <Chip 
            icon={getPriorityIcon(alert.priority)}
            label={`${alert.fromDepartment} → ${alert.toDepartment}`}
            color={getPriorityColor(alert.priority) as any}
            size={accessibility.largeText ? "medium" : "small"}
          />
          {alert.escalationCount > 0 && (
            <Badge badgeContent={alert.escalationCount} color="error">
              <WarningIcon />
            </Badge>
          )}
        </Box>
        <Typography 
          variant={accessibility.largeText ? "body1" : "body2"}
          fontWeight="medium"
        >
          {alert.message}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {new Date(alert.createdAt).toLocaleTimeString()}
        </Typography>
      </CardContent>
    </AccessibleCard>
  );

  return (
    <Box sx={{ pb: 7 }}> {/* Bottom navigation padding */}
      {/* Top App Bar */}
      <AppBar position="sticky" color="primary">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            RelayPoint Hospitality
          </Typography>
          
          {/* Language Selector */}
          <FormControl size="small" sx={{ mr: 1, minWidth: 60 }}>
            <Select
              value={language}
              onChange={(e) => setLanguage(e.target.value as 'en' | 'es' | 'fr')}
              sx={{ color: 'white', '& .MuiOutlinedInput-notchedOutline': { borderColor: 'white' } }}
              aria-label="Select language"
            >
              <MenuItem value="en">EN</MenuItem>
              <MenuItem value="es">ES</MenuItem>
              <MenuItem value="fr">FR</MenuItem>
            </Select>
          </FormControl>

          {/* Accessibility Menu */}
          <IconButton
            color="inherit"
            onClick={() => setDrawerOpen(true)}
            aria-label="Accessibility settings"
          >
            <AccessibilityIcon />
          </IconButton>

          {/* Alerts Badge */}
          <IconButton color="inherit" aria-label={`${alerts.length} new alerts`}>
            <Badge badgeContent={alerts.length} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box sx={{ p: 2 }}>
        {/* Dashboard View */}
        {bottomNavValue === 0 && (
          <Box>
            <Typography 
              variant={accessibility.largeText ? "h4" : "h5"} 
              gutterBottom
              color={accessibility.highContrast ? "white" : "primary"}
            >
              {t.dashboard} - {t[currentUser.department]}
            </Typography>
            
            {/* Quick Stats */}
            <Box display="flex" gap={2} mb={3} flexWrap="wrap">
              <Card sx={{ flex: 1, minWidth: 120 }}>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="primary">{tasks.filter(t => t.status === 'pending').length}</Typography>
                  <Typography variant="caption">{t.pending}</Typography>
                </CardContent>
              </Card>
              <Card sx={{ flex: 1, minWidth: 120 }}>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="warning.main">{tasks.filter(t => t.status === 'in_progress').length}</Typography>
                  <Typography variant="caption">{t.inProgress}</Typography>
                </CardContent>
              </Card>
              <Card sx={{ flex: 1, minWidth: 120 }}>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h4" color="error.main">{alerts.length}</Typography>
                  <Typography variant="caption">{t.alerts}</Typography>
                </CardContent>
              </Card>
            </Box>

            {/* Recent Tasks */}
            <Typography variant={accessibility.largeText ? "h6" : "subtitle1"} gutterBottom>
              Your Tasks
            </Typography>
            {tasks.slice(0, 3).map(task => (
              <TaskCard key={task.id} task={task} />
            ))}
          </Box>
        )}

        {/* Tasks View */}
        {bottomNavValue === 1 && (
          <Box>
            <Typography variant={accessibility.largeText ? "h5" : "h6"} gutterBottom>
              {t.tasks}
            </Typography>
            {tasks.map(task => (
              <TaskCard key={task.id} task={task} />
            ))}
          </Box>
        )}

        {/* Alerts View */}
        {bottomNavValue === 2 && (
          <Box>
            <Typography variant={accessibility.largeText ? "h5" : "h6"} gutterBottom>
              {t.alerts}
            </Typography>
            {alerts.map(alert => (
              <AlertCard key={alert.id} alert={alert} />
            ))}
          </Box>
        )}

        {/* Communication View */}
        {bottomNavValue === 3 && (
          <Box>
            <Typography variant={accessibility.largeText ? "h5" : "h6"} gutterBottom>
              {t.communication}
            </Typography>
            
            <Box display="grid" gridTemplateColumns="repeat(auto-fit, minmax(150px, 1fr))" gap={2}>
              <AccessibleButton
                largeText={accessibility.largeText}
                variant="contained"
                fullWidth
                onClick={() => sendQuickMessage('guest_waiting')}
                aria-label="Send guest waiting alert"
              >
                {t.guestWaiting}
              </AccessibleButton>
              <AccessibleButton
                largeText={accessibility.largeText}
                variant="contained"
                fullWidth
                onClick={() => sendQuickMessage('maintenance_needed')}
                aria-label="Request maintenance"
              >
                {t.maintenanceNeeded}
              </AccessibleButton>
              <AccessibleButton
                largeText={accessibility.largeText}
                variant="contained"
                fullWidth
                onClick={() => sendQuickMessage('housekeeping_required')}
                aria-label="Request housekeeping"
              >
                {t.housekeepingRequired}
              </AccessibleButton>
              <AccessibleButton
                largeText={accessibility.largeText}
                variant="contained"
                fullWidth
                onClick={() => sendQuickMessage('need_assistance')}
                aria-label="Request assistance"
              >
                {t.needHelp}
              </AccessibleButton>
            </Box>
          </Box>
        )}
      </Box>

      {/* Speed Dial for Quick Actions */}
      <SpeedDial
        ariaLabel="Quick actions"
        sx={{ position: 'fixed', bottom: 80, right: 16 }}
        icon={<SpeedDialIcon />}
      >
        <SpeedDialAction
          icon={<MicIcon />}
          tooltipTitle={t.voiceNote}
          onClick={startVoiceRecording}
        />
        <SpeedDialAction
          icon={<ChatIcon />}
          tooltipTitle={t.communication}
          onClick={() => setBottomNavValue(3)}
        />
        <SpeedDialAction
          icon={<NotificationsIcon />}
          tooltipTitle={t.alerts}
          onClick={() => setBottomNavValue(2)}
        />
      </SpeedDial>

      {/* Bottom Navigation */}
      <BottomNavigation
        value={bottomNavValue}
        onChange={(event, newValue) => setBottomNavValue(newValue)}
        sx={{ 
          position: 'fixed', 
          bottom: 0, 
          left: 0, 
          right: 0,
          '& .MuiBottomNavigationAction-label': {
            fontSize: accessibility.largeText ? '0.875rem' : '0.75rem'
          }
        }}
      >
        <BottomNavigationAction 
          label={t.dashboard} 
          icon={<HotelIcon />} 
          aria-label="Dashboard"
        />
        <BottomNavigationAction 
          label={t.tasks} 
          icon={<Badge badgeContent={tasks.filter(t => t.status === 'pending').length} color="error"><TaskIcon /></Badge>} 
          aria-label={`Tasks (${tasks.filter(t => t.status === 'pending').length} pending)`}
        />
        <BottomNavigationAction 
          label={t.alerts} 
          icon={<Badge badgeContent={alerts.length} color="error"><NotificationsIcon /></Badge>} 
          aria-label={`Alerts (${alerts.length} new)`}
        />
        <BottomNavigationAction 
          label={t.communication} 
          icon={<ChatIcon />} 
          aria-label="Communication"
        />
      </BottomNavigation>

      {/* Accessibility Settings Drawer */}
      <Drawer
        anchor="right"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <Box sx={{ width: 300, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            {t.accessibility}
          </Typography>
          <Divider sx={{ mb: 2 }} />
          
          <List>
            <ListItem>
              <ListItemIcon><TextIncreaseIcon /></ListItemIcon>
              <ListItemText primary={t.largeText} />
              <Switch
                checked={accessibility.largeText}
                onChange={(e) => setAccessibility(prev => ({ ...prev, largeText: e.target.checked }))}
                aria-label="Toggle large text"
              />
            </ListItem>
            
            <ListItem>
              <ListItemIcon><ContrastIcon /></ListItemIcon>
              <ListItemText primary={t.highContrast} />
              <Switch
                checked={accessibility.highContrast}
                onChange={(e) => setAccessibility(prev => ({ ...prev, highContrast: e.target.checked }))}
                aria-label="Toggle high contrast"
              />
            </ListItem>
            
            <ListItem>
              <ListItemIcon><VolumeUpIcon /></ListItemIcon>
              <ListItemText primary={t.screenReader} />
              <Switch
                checked={accessibility.screenReader}
                onChange={(e) => setAccessibility(prev => ({ ...prev, screenReader: e.target.checked }))}
                aria-label="Toggle screen reader support"
              />
            </ListItem>
            
            <ListItem>
              <ListItemIcon><MicIcon /></ListItemIcon>
              <ListItemText primary="Voice Commands" />
              <Switch
                checked={accessibility.voiceCommands}
                onChange={(e) => setAccessibility(prev => ({ ...prev, voiceCommands: e.target.checked }))}
                aria-label="Toggle voice commands"
              />
            </ListItem>
          </List>
        </Box>
      </Drawer>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
        message={snackbar.message}
      />
    </Box>
  );
};

export default HospitalityDashboard;