/**
 * Conditional Node Component
 */

import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Card, CardContent, Typography, Box, IconButton } from '@mui/material';
import { BranchingScenario as ConditionalIcon, Settings as SettingsIcon } from '@mui/icons-material';

import { WorkflowNodeData } from '../EliteWorkflowBuilder';

const ConditionalNode: React.FC<NodeProps<WorkflowNodeData>> = ({ data, selected }) => {
  return (
    <>
      <Handle type="target" position={Position.Top} />
      
      <Card
        elevation={selected ? 8 : 2}
        sx={{
          minWidth: 180,
          border: selected ? '2px solid #1976d2' : 'none',
          bgcolor: 'warning.light',
        }}
      >
        <CardContent sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <ConditionalIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="subtitle2" sx={{ flexGrow: 1 }}>
              {data.label}
            </Typography>
            <IconButton size="small">
              <SettingsIcon fontSize="small" />
            </IconButton>
          </Box>
          
          <Typography variant="caption" color="text.secondary">
            {data.description}
          </Typography>
        </CardContent>
      </Card>
      
      <Handle type="source" position={Position.Bottom} id="true" style={{ left: '25%' }} />
      <Handle type="source" position={Position.Bottom} id="false" style={{ left: '75%' }} />
    </>
  );
};

export default ConditionalNode;