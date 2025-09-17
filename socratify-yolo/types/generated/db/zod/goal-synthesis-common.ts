import { z } from 'zod';

/**
 * Common Goal Synthesis Types
 * 
 * Shared schemas used across Goal Synthesis V1 and V2 APIs
 */

/**
 * Valid skill states for Goal Synthesis
 */
export const SkillStateSchema = z.enum(['selected', 'unselected', 'disabled']).describe(
  'selected = chosen for user\'s goal, unselected = available but not chosen, disabled = Socratify cannot help with this'
);
export type SkillState = z.infer<typeof SkillStateSchema>;

/**
 * Individual skill with name and state
 */
export const SkillSchema = z.object({
  name: z.string().describe('The skill name'),
  state: SkillStateSchema,
});
export type Skill = z.infer<typeof SkillSchema>;

/**
 * Categorized skills structure for V2
 */
export const SkillCategoriesSchema = z.object({
  hardSkills: z
    .array(SkillSchema)
    .describe('Hard skills including industry/business knowledge skills Socratify can help with. Technical implementation skills should be disabled.'),
  fluidSkills: z
    .array(SkillSchema)
    .describe('Fluid skills focused on critical thinking, first principles reasoning, creative problem solving - Socratify\'s core strength.'),
  softSkills: z
    .array(SkillSchema)
    .describe('Soft skills focused on verbal communication, articulation, influence - skills developed through discussion and debate.'),
});
export type SkillCategories = z.infer<typeof SkillCategoriesSchema>;

/**
 * Professional classification flags used in both V1 and V2
 */
export const ProfessionalClassificationSchema = z.object({
  serviceProfessional: z
    .boolean()
    .describe(
      'Whether the user is a service professional (consultant, banker, lawyer, etc.) who serves clients across industries and lacks sufficient information about their industry preferences'
    ),
  functionalExpert: z
    .boolean()
    .describe(
      'Whether the user is a functional expert with deep domain expertise (software engineer, designer, doctor, teacher, etc.) who could benefit from complementary business skills'
    ),
});
export type ProfessionalClassification = z.infer<typeof ProfessionalClassificationSchema>;

/**
 * Base request schema for goal synthesis APIs
 */
export const BaseGoalSynthesisRequestSchema = z.object({
  userGoal: z.string().describe('Predefined goal option: "Get a job", "Change jobs", "Get promoted", etc.'),
  userGoalInputText: z.string().describe('Free-text user input describing their specific goal'),
  isAudioInput: z.boolean().optional().describe('true if input is audio'),
  userGoalInputAudio: z.string().optional().describe('base64 audio data if isAudioInput is true'),
});
export type BaseGoalSynthesisRequest = z.infer<typeof BaseGoalSynthesisRequestSchema>;

/**
 * Base response schema with common fields
 */
export const BaseGoalSynthesisResponseSchema = ProfessionalClassificationSchema.extend({
  userShortGoal: z
    .string()
    .describe('A short (25 characters or less) title that captures the user\'s goal'),
  userGoalParagraph: z
    .string()
    .describe('A synthesized paragraph (120-200 characters) that crisply defines the user\'s goal'),
  futureCompany: z
    .string()
    .describe('A company that the user would like to work for in the future if they mentioned one clearly'),
  logoUrl: z
    .string()
    .describe('Company logo URL if found, else empty string'),
});
export type BaseGoalSynthesisResponse = z.infer<typeof BaseGoalSynthesisResponseSchema>;