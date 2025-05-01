'use client';

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { memo } from 'react';
import type { UseChatHelpers } from '@ai-sdk/react';

interface SuggestedActionsProps {
  chatId: string;
  append: UseChatHelpers['append'];
}

function PureSuggestedActions({ chatId, append }: SuggestedActionsProps) {
  const suggestedActions = [
    {title: '📊 Generate a ppt on PCA',
      label: 'using R',
      action: 'Generate R code that creates a PowerPoint presentation about Principal Component Analysis. The code should generate slides covering PCA concepts, implementation, and visualization examples.',
    },
    {
      title: '🧠 Write a simple',
      label: 'neural network in R?',
      action: 'Write a simple neural network in R?',
    },
    {
      title: '🔍 Explain what is ',
      label: `naive bayes`,
      action: `Explain what is naive bayes`,
    },

    {
      title: '🌊 How does a',
      label: 'diffusion model work?',
      action: 'How does a diffusion model work?',
    },
  ];

  return (
    <div
      data-testid="suggested-actions"
      className="grid sm:grid-cols-2 gap-2 w-full"
    >
      {suggestedActions.map((suggestedAction, index) => (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          transition={{ delay: 0.05 * index }}
          key={`suggested-action-${suggestedAction.title}-${index}`}
          className={index > 1 ? 'hidden sm:block' : 'block'}
        >
          <Button
            variant="ghost"
            onClick={async () => {
              window.history.replaceState({}, '', `/chat/${chatId}`);

              append({
                role: 'user',
                content: suggestedAction.action,
              });
            }}
            className="text-left items-center border-none rounded-xl px-4 py-3.5 text-md flex-1 gap-1 sm:flex-col w-full h-auto justify-start"
          >
            <span className="font-light text-center">{suggestedAction.title}  {suggestedAction.label}</span>
            {/* <span className="text-muted-foreground text-center">
              {suggestedAction.label}
            </span> */}
          </Button>
        </motion.div>
      ))}
    </div>
  );
}

export const SuggestedActions = memo(PureSuggestedActions, () => true);
