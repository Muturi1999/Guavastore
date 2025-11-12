'use client';

import { InputHTMLAttributes, FC } from 'react';
import { cn } from '@/lib/utils';  

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const Input: FC<InputProps> = ({ className, ...props }) => {
  return (
    <input
      className={cn(
        'border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
        className
      )}
      {...props}
    />
  );
};
