/**
 * HTTP Request Node Component
 */

import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import {
  Card,
  CardContent,
  Typography,
  Box,
  IconButton,
  Chip,
} from '@mui/material';
import {
  Http as HttpIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

import { WorkflowNodeData } from '../EliteWorkflowBuilder';

const HttpRequestNode: React.FC<NodeProps<WorkflowNodeData>> = ({ data, selected }) => {
  const getMethodColor = (method: string) => {
    switch (method?.toUpperCase()) {
      case 'GET': return 'success';
      case 'POST': return 'primary';
      case 'PUT': return 'warning';
      case 'DELETE': return 'error';
      default: return 'default';
    }
  };

  return (
    <>
      <Handle type="target" position={Position.Top} />
      
      <Card
        elevation={selected ? 8 : 2}
        sx={{
          minWidth: 200,
          border: selected ? '2px solid #1976d2' : 'none',
        }}
      >
        <CardContent sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <HttpIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="subtitle2" sx={{ flexGrow: 1 }}>
              {data.label}
            </Typography>
            <IconButton size="small">
              <SettingsIcon fontSize="small" />
            </IconButton>
          </Box>
          
          <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
            {data.description}
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Chip
              label={data.config?.method || 'GET'}
              size="small"
              color={getMethodColor(data.config?.method)}
            />
            <Chip
              label={data.status || 'idle'}
              size="small"
              variant="outlined"
            />
          </Box>
        </CardContent>
      </Card>
      
      <Handle type="source" position={Position.Bottom} />
    </>
  );
};

export default HttpRequestNode;