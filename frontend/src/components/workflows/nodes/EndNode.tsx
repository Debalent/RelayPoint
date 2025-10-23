/**
 * End Node Component
 */

import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { Stop as StopIcon } from '@mui/icons-material';

const EndNode: React.FC<NodeProps> = ({ selected }) => {
  return (
    <>
      <Handle type="target" position={Position.Top} />
      
      <Card
        elevation={selected ? 8 : 2}
        sx={{
          minWidth: 120,
          border: selected ? '2px solid #1976d2' : 'none',
          bgcolor: 'error.main',
          color: 'white',
        }}
      >
        <CardContent sx={{ p: 2, textAlign: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <StopIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle2">End</Typography>
          </Box>
        </CardContent>
      </Card>
    </>
  );
};

export default EndNode;