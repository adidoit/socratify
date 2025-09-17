import { z } from 'zod';
import { BaseGoalSynthesisRequestSchema, BaseGoalSynthesisResponseSchema } from './goal-synthesis-common';

/**
 * Goal Synthesis V3 API Types
 * 
 * V3 focuses on structured skill generation with target proficiency levels
 * for better integration with skill tracking and exercise selection
 */

/**
 * Proficiency levels matching database enums
 */
export const ProficiencyLevelSchema = z.enum([
  'BEGINNER',
  'APPRENTICE', 
  'PRACTITIONER',
  'EXPERT',
  'TOP_10'
]);
export type ProficiencyLevel = z.infer<typeof ProficiencyLevelSchema>;

/**
 * Skill categories
 */
export const SkillCategorySchema = z.enum(['HARD', 'FLUID', 'SOFT']);
export type SkillCategory = z.infer<typeof SkillCategorySchema>;

/**
 * Structured skill with proficiency and metadata for V3
 */
export const StructuredSkillSchema = z.object({
  name: z.string().describe('The skill name (2-4 words, specific and granular)'),
  category: SkillCategorySchema.describe('The skill category'),
  targetProficiency: ProficiencyLevelSchema.describe('The target proficiency level for this skill'),
  definition: z.string().describe('Clear definition of what this skill entails'),
  rationale: z.string().describe('Why this skill is important for the user\'s goal'),
});
export type StructuredSkill = z.infer<typeof StructuredSkillSchema>;

/**
 * Later development skill (simplified)
 */
export const LaterDevelopmentSkillSchema = z.object({
  name: z.string().describe('The skill name'),
});
export type LaterDevelopmentSkill = z.infer<typeof LaterDevelopmentSkillSchema>;

/**
 * Request schema for Goal Synthesis V3
 */
export const GoalSynthesisV3RequestSchema = BaseGoalSynthesisRequestSchema;
export type GoalSynthesisV3Request = z.infer<typeof GoalSynthesisV3RequestSchema>;

/**
 * Response schema for Goal Synthesis V3
 */
export const GoalSynthesisV3ResponseSchema = BaseGoalSynthesisResponseSchema.extend({
  initialSkills: z
    .array(StructuredSkillSchema)
    .length(3)
    .describe('Exactly 3 initial focus skills with full metadata'),
  laterDevelopmentSkills: z
    .array(LaterDevelopmentSkillSchema)
    .min(3)
    .max(7)
    .describe('3-7 later development skills (name only)'),
});
export type GoalSynthesisV3Response = z.infer<typeof GoalSynthesisV3ResponseSchema>;