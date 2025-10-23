/**
 * AI Task Node Component
 * 
 * Custom ReactFlow node for AI-powered operations
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
  SmartToy as AIIcon,
  Settings as SettingsIcon,
  PlayArrow as PlayIcon,
} from '@mui/icons-material';

import { WorkflowNodeData } from '../EliteWorkflowBuilder';

const AITaskNode: React.FC<NodeProps<WorkflowNodeData>> = ({ data, selected }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'primary';
      case 'completed': return 'success';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  return (
    <>
      <Handle
        type="target"
        position={Position.Top}
        style={{ background: '#555' }}
      />
      
      <Card
        elevation={selected ? 8 : 2}
        sx={{
          minWidth: 200,
          border: selected ? '2px solid #1976d2' : 'none',
          borderRadius: 2,
        }}
      >
        <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <AIIcon color="primary" sx={{ mr: 1 }} />
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
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Chip
              label={data.status || 'idle'}
              size="small"
              color={getStatusColor(data.status || 'idle')}
              variant="outlined"
            />
            
            {data.config?.model && (
              <Typography variant="caption" color="text.secondary">
                {data.config.model}
              </Typography>
            )}
          </Box>
        </CardContent>
      </Card>
      
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: '#555' }}
      />
    </>
  );
};

export default AITaskNode;