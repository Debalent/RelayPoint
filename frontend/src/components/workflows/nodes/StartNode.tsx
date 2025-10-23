/**
 * Start Node Component
 */

import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { PlayArrow as PlayIcon } from '@mui/icons-material';

const StartNode: React.FC<NodeProps> = ({ selected }) => {
  return (
    <>
      <Card
        elevation={selected ? 8 : 2}
        sx={{
          minWidth: 120,
          border: selected ? '2px solid #1976d2' : 'none',
          bgcolor: 'success.main',
          color: 'white',
        }}
      >
        <CardContent sx={{ p: 2, textAlign: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <PlayIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle2">Start</Typography>
          </Box>
        </CardContent>
      </Card>
      
      <Handle type="source" position={Position.Bottom} />
    </>
  );
};

export default StartNode;