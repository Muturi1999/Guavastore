'use client';

import { ButtonHTMLAttributes, FC } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
}

export const Button: FC<ButtonProps> = ({ children, className, ...props }) => {
  return (
    <button
      className={cn(
        'px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500',
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};
