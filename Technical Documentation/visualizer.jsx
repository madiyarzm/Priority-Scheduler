import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const ComplexityVisualization = () => {
  const [data, setData] = useState([]);
  const [isAnimating, setIsAnimating] = useState(false);
  const [currentSize, setCurrentSize] = useState(1);

  useEffect(() => {
    if (isAnimating && currentSize <= 50) {
      const timer = setTimeout(() => {
        const newDataPoint = {
          n: currentSize,
          sorting: (currentSize * Math.log2(currentSize)).toFixed(2),
          priorityQueue: Math.log2(currentSize).toFixed(2),
        };
        setData(prev => [...prev, newDataPoint]);
        setCurrentSize(prev => prev + 1);
      }, 100);
      return () => clearTimeout(timer);
    } else {
      setIsAnimating(false);
    }
  }, [isAnimating, currentSize]);

  const startVisualization = () => {
    setData([]);
    setCurrentSize(1);
    setIsAnimating(true);
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Time Complexity Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <Button 
            onClick={startVisualization}
            disabled={isAnimating}
          >
            {isAnimating ? 'Visualizing...' : 'Start Visualization'}
          </Button>
        </div>

        <div className="mb-8">
          <LineChart width={700} height={400} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="n" 
              label={{ value: 'Number of Elements (n)', position: 'bottom' }} 
            />
            <YAxis 
              label={{ value: 'Operations', angle: -90, position: 'insideLeft' }} 
            />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="sorting" 
              name="Sorting O(n log n)" 
              stroke="#8884d8" 
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey="priorityQueue" 
              name="Priority Queue O(log n)" 
              stroke="#82ca9d" 
              strokeWidth={2}
            />
          </LineChart>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="p-4 bg-purple-50 rounded">
            <h3 className="font-bold text-purple-700 mb-2">Sorting O(n log n)</h3>
            <p>Requires resorting entire list when new tasks arrive</p>
            <p className="mt-2">Current operations: {data[data.length - 1]?.sorting || 0}</p>
          </div>
          <div className="p-4 bg-green-50 rounded">
            <h3 className="font-bold text-green-700 mb-2">Priority Queue O(log n)</h3>
            <p>Only needs to rebalance heap for new insertions</p>
            <p className="mt-2">Current operations: {data[data.length - 1]?.priorityQueue || 0}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ComplexityVisualization;