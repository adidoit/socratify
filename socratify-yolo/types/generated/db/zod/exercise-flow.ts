import { z } from 'zod';

/**
 * Exercise Flow Configuration Types
 * 
 * Shared types for flexible exercise routing configuration between mobile and web clients.
 * Designed to prevent issues through strong typing, backward compatibility, 
 * and clear handling of branching logic and edge cases.
 */

/**
 * Represents a condition that can be evaluated for branching logic
 */
export const BranchConditionSchema = z.object({
  condition: z.string().describe('The condition type (e.g., "ready", "needMore", "score", "default")'),
  value: z.union([z.string(), z.number()]).optional().describe('Optional value for comparison (e.g., for "score >= 80")'),
  next: z.string().describe('The step ID to navigate to if this condition is met'),
});
export type BranchCondition = z.infer<typeof BranchConditionSchema>;

/**
 * Represents navigation configuration for a step
 */
export const NavigationConfigSchema = z.object({
  allowSkip: z.boolean().optional().describe('Whether this step can be skipped'),
  requiresCompletion: z.boolean().optional().describe('Whether this step must be completed before proceeding'),
  canGoBack: z.boolean().optional().describe('Whether user can navigate back from this step'),
  autoAdvance: z.boolean().optional().describe('Whether to automatically advance after completion'),
  autoAdvanceDelay: z.number().int().min(0).optional().describe('Delay in milliseconds before auto-advancing'),
});
export type NavigationConfig = z.infer<typeof NavigationConfigSchema>;

/**
 * Represents a single step in the exercise flow
 */
export const ExerciseStepSchema = z.object({
  id: z.string().describe('Unique identifier for this step (e.g., "context-0-intro")'),
  path: z.string().describe('The route path suffix (e.g., "(context)/context-0-intro")'),
  progress: z.number().min(0).max(100).describe('Progress percentage (0-100) for this step'),
  title: z.string().optional().describe('Display title for this step'),
  description: z.string().optional().describe('Description of what happens in this step'),
  
  // Navigation configuration
  navigation: NavigationConfigSchema.optional(),
  
  // Branching logic
  branches: z.array(BranchConditionSchema).optional().describe('Conditional branching logic for this step'),
  
  // Default next step (if no branches match)
  next: z.string().optional().describe('Default next step ID'),
  
  // Step metadata
  isOptional: z.boolean().optional().describe('Whether this step is optional'),
  estimatedDuration: z.number().int().min(0).optional().describe('Estimated duration in seconds'),
  stepType: z.enum(['intro', 'context', 'debate', 'debrief', 'final']).optional().describe('Type of step for UI styling'),
});
export type ExerciseStep = z.infer<typeof ExerciseStepSchema>;

/**
 * Flow step configuration for specific step types
 */
export const FlowStepConfigSchema = z.object({
  totalSteps: z.number().int().min(1).describe('Total number of steps in this flow'),
  currentIndex: z.number().int().min(0).describe('Current step index (0-based)'),
  canSkip: z.boolean().optional().describe('Whether this step can be skipped'),
  showProgress: z.boolean().optional().describe('Whether to show progress indicator'),
  enableSwipe: z.boolean().optional().describe('Whether swipe navigation is enabled'),
});
export type FlowStepConfig = z.infer<typeof FlowStepConfigSchema>;

/**
 * Complete exercise flow configuration
 */
export const ExerciseFlowConfigSchema = z.object({
  // Flow identification
  exerciseType: z.string().describe('The exercise type this flow is for'),
  version: z.string().optional().describe('Version of this flow configuration'),
  
  // Flow structure
  steps: z.array(ExerciseStepSchema).describe('All steps in this exercise flow'),
  entryPoint: z.string().describe('ID of the first step in the flow'),
  exitPoints: z.array(z.string()).optional().describe('IDs of steps that can end the flow'),
  
  // Flow metadata
  estimatedTotalDuration: z.number().int().min(0).optional().describe('Total estimated duration in seconds'),
  difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
  
  // Flow configuration
  allowRestart: z.boolean().optional().describe('Whether users can restart the flow'),
  saveProgress: z.boolean().optional().describe('Whether to save progress automatically'),
  
  // Validation settings
  strictValidation: z.boolean().optional().describe('Whether to use strict step validation'),
  fallbackBehavior: z.enum(['error', 'skip', 'default']).optional().describe('How to handle invalid steps'),
});
export type ExerciseFlowConfig = z.infer<typeof ExerciseFlowConfigSchema>;

/**
 * Flow step configuration result
 */
export const FlowConfigResultSchema = z.object({
  isValid: z.boolean(),
  currentStep: ExerciseStepSchema.optional(),
  nextStep: ExerciseStepSchema.optional(),
  flowConfig: FlowStepConfigSchema.optional(),
  error: z.string().optional(),
  warnings: z.array(z.string()).optional(),
});
export type FlowConfigResult = z.infer<typeof FlowConfigResultSchema>;

/**
 * Flow validation result
 */
export const FlowValidationResultSchema = z.object({
  isValid: z.boolean(),
  errors: z.array(z.string()),
  warnings: z.array(z.string()),
  suggestions: z.array(z.string()).optional(),
});
export type FlowValidationResult = z.infer<typeof FlowValidationResultSchema>;

/**
 * Navigation state for flow tracking
 */
export const FlowNavigationStateSchema = z.object({
  currentStepId: z.string(),
  previousStepId: z.string().optional(),
  completedStepIds: z.array(z.string()),
  availableStepIds: z.array(z.string()),
  canGoBack: z.boolean(),
  canGoForward: z.boolean(),
  isComplete: z.boolean(),
  progress: z.number().min(0).max(100),
});
export type FlowNavigationState = z.infer<typeof FlowNavigationStateSchema>;