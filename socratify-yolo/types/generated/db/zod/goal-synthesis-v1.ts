import { z } from 'zod';
import { BaseGoalSynthesisRequestSchema, BaseGoalSynthesisResponseSchema } from './goal-synthesis-common';

/**
 * Goal Synthesis V1 API Types
 * 
 * Original goal synthesis API with simple skill list structure
 */

/**
 * Request schema for Goal Synthesis V1
 */
export const GoalSynthesisV1RequestSchema = BaseGoalSynthesisRequestSchema;
export type GoalSynthesisV1Request = z.infer<typeof GoalSynthesisV1RequestSchema>;

/**
 * Response schema for Goal Synthesis V1
 */
export const GoalSynthesisV1ResponseSchema = BaseGoalSynthesisResponseSchema.extend({
  possibleSkills: z
    .array(z.string())
    .describe(
      'A list of maximum 5 skills that would support the user achieving the goal as defined in the userGoalParagraph. These should be mutually exclusive and not overlapping in meaning.'
    ),
  selectedSkills: z
    .array(z.string())
    .describe(
      'A maximum of 2 skills out of the possibleSkills that are pre-selected based on their fit with the user\'s goal'
    ),
});
export type GoalSynthesisV1Response = z.infer<typeof GoalSynthesisV1ResponseSchema>;