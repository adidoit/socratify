import { z } from 'zod';
import { BaseGoalSynthesisRequestSchema, BaseGoalSynthesisResponseSchema, SkillCategoriesSchema } from './goal-synthesis-common';

/**
 * Goal Synthesis V2 API Types
 * 
 * Enhanced goal synthesis API with structured skill categories and states
 */

/**
 * Request schema for Goal Synthesis V2
 */
export const GoalSynthesisV2RequestSchema = BaseGoalSynthesisRequestSchema;
export type GoalSynthesisV2Request = z.infer<typeof GoalSynthesisV2RequestSchema>;

/**
 * Response schema for Goal Synthesis V2
 */
export const GoalSynthesisV2ResponseSchema = BaseGoalSynthesisResponseSchema.extend({
  skillCategories: SkillCategoriesSchema.describe(
    'Skills organized into three categories: hard skills (with industry knowledge), fluid skills (critical thinking), and soft skills (communication)'
  ),
  selectedSkills: z
    .array(z.string())
    .describe(
      'Most critical skills selected from across all categories based on their fit with the user\'s goal'
    ),
});
export type GoalSynthesisV2Response = z.infer<typeof GoalSynthesisV2ResponseSchema>;

// Re-export types from common for convenience
export type { SkillCategories } from './goal-synthesis-common';
export { SkillCategoriesSchema } from './goal-synthesis-common';